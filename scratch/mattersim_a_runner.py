#!/usr/bin/env python3
import json, math, os, traceback
from pathlib import Path

import numpy as np
import torch
from ase import Atom
from ase.build import bulk
from ase.filters import FrechetCellFilter
from ase.io import write
from ase.neighborlist import neighbor_list
from ase.optimize import FIRE
from ase.units import Pascal, GPa
from mattersim.forcefield import MatterSimCalculator

OUT = Path("scratch/mattersim_a_results")
OUT.mkdir(parents=True, exist_ok=True)

A_CANDIDATES = [
    ("Actinium", "Ac", 89),
    ("Aluminium", "Al", 13),
    ("Americium", "Am", 95),
    ("Antimony", "Sb", 51),
    ("Argon", "Ar", 18),
    ("Arsenic", "As", 33),
    ("Astatine", "At", 85),
]

HOST_AU = 79
HOST_AG = 21
PRESSURE_CHECKS_ATM = [1000, 500, 0]
FRAME_SCALE_LITERAL = "1.6161x10^-35"
PRESSURE_TOL_GPA = 0.25  # comparable to published MatterSim-v1 stress-error scale
FMAX = 0.05
MAX_STEPS = 300

TETRA = np.array([
    [ 1.0,  1.0,  1.0],
    [ 1.0, -1.0, -1.0],
    [-1.0,  1.0, -1.0],
    [-1.0, -1.0,  1.0],
], dtype=float)
TETRA /= np.linalg.norm(TETRA[0])

def sign_state(i):
    bits = [(i >> (3-k)) & 1 for k in range(4)]
    seams = ["+" if b else "-" for b in bits]
    signs = np.array([1.0 if b else -1.0 for b in bits])
    disp = (signs[:, None] * TETRA).sum(axis=0) * 0.06
    expr = f"+++ {seams[0]} --- {seams[1]} +++ {seams[2]} --- {seams[3]} +++"
    return {
        "id": i + 1,
        "bits": "".join(str(b) for b in bits),
        "seams": "".join(seams),
        "expression": expr,
        "displacement_A": disp.tolist(),
    }

def build_electrum():
    atoms = bulk("Au", "fcc").repeat((5, 5, 4))
    assert len(atoms) == 100
    rng = np.random.default_rng(0)
    ag_idx = sorted(rng.choice(len(atoms), size=HOST_AG, replace=False).tolist())
    for idx in ag_idx:
        atoms[idx].symbol = "Ag"
    atoms.set_pbc(True)
    return atoms

def add_candidate(host, candidate_symbol, config_id):
    atoms = host.copy()
    frac = np.array([0.5, 0.5, 0.5])
    pos = frac @ atoms.cell.array
    ss = sign_state(config_id - 1)
    pos = pos + np.array(ss["displacement_A"], dtype=float)
    atoms.append(Atom(candidate_symbol, position=pos))
    atoms.set_pbc(True)
    return atoms, ss

def host_connected(atoms, cutoff=3.8):
    host = atoms[:100]
    i, j = neighbor_list("ij", host, cutoff)
    adj = [[] for _ in range(100)]
    for a, b in zip(i.tolist(), j.tolist()):
        if a != b:
            adj[a].append(b)
            adj[b].append(a)
    seen = {0}
    stack = [0]
    while stack:
        a = stack.pop()
        for b in adj[a]:
            if b not in seen:
                seen.add(b)
                stack.append(b)
    return len(seen) == 100

def candidate_coordination(atoms, cutoff=4.2):
    d = atoms.get_distances(100, list(range(100)), mic=True)
    return int(np.sum(np.asarray(d) < cutoff))

def min_pair_distance(atoms):
    d = atoms.get_all_distances(mic=True)
    np.fill_diagonal(d, np.inf)
    return float(np.min(d))

def stress_metrics(atoms):
    stress = np.asarray(atoms.get_stress(voigt=False))
    stress_gpa = stress / GPa
    internal_pressure_gpa = float(-np.trace(stress_gpa) / 3.0)
    shear_gpa = float(np.sqrt(np.sum((stress_gpa - np.eye(3)*np.trace(stress_gpa)/3.0)**2)))
    return stress_gpa, internal_pressure_gpa, shear_gpa

def relax(atoms, calc, pressure_atm, label):
    atoms.calc = calc
    target_gpa = pressure_atm * 0.000101325
    target = pressure_atm * 101325.0 * Pascal
    filt = FrechetCellFilter(atoms, scalar_pressure=target)
    opt = FIRE(filt, logfile=None)
    converged = bool(opt.run(fmax=FMAX, steps=MAX_STEPS))

    energy = float(atoms.get_potential_energy())
    forces = np.asarray(atoms.get_forces())
    max_force = float(np.max(np.linalg.norm(forces, axis=1)))
    stress_gpa, internal_p, shear = stress_metrics(atoms)
    finite = bool(
        np.isfinite(energy)
        and np.all(np.isfinite(forces))
        and np.all(np.isfinite(stress_gpa))
        and np.isfinite(atoms.get_volume())
    )
    mind = min_pair_distance(atoms)
    coord = candidate_coordination(atoms) if len(atoms) == 101 else None
    connected = host_connected(atoms)
    pressure_error = abs(internal_p - target_gpa)

    passed = bool(
        converged
        and finite
        and max_force <= 0.075
        and mind > 1.20
        and connected
        and pressure_error <= PRESSURE_TOL_GPA
        and (coord is None or coord > 0)
    )
    return {
        "label": label,
        "pressure_atm": int(pressure_atm),
        "target_pressure_GPa": target_gpa,
        "gravitus_tick": int(1000 - pressure_atm),
        "frame_literal": f"{1000-pressure_atm} x {FRAME_SCALE_LITERAL}",
        "converged": converged,
        "energy_eV": energy,
        "max_force_eV_A": max_force,
        "stress_GPa": stress_gpa.tolist(),
        "internal_pressure_GPa": internal_p,
        "pressure_error_GPa": pressure_error,
        "shear_norm_GPa": shear,
        "volume_A3": float(atoms.get_volume()),
        "min_pair_distance_A": mind,
        "candidate_coordination_lt4p2A": coord,
        "electrum_host_connected": connected,
        "pass": passed,
    }

def run_trial(base_host_1000, name, symbol, z, config_id, calc):
    atoms, ss = add_candidate(base_host_1000, symbol, config_id)
    result = {
        "candidate": name,
        "symbol": symbol,
        "atomic_number": z,
        "config": ss,
        "shell": "pre-relaxed 100-site fcc Electrum host Au79Ag21 + 1 interstitial candidate",
        "shell_atoms": 100,
        "total_atoms": 101,
        "pressure_checks": [],
        "pass": False,
    }
    for pressure in PRESSURE_CHECKS_ATM:
        step = relax(atoms, calc, pressure, "candidate")
        result["pressure_checks"].append(step)
        print(
            f"{name:10s} cfg={config_id:02d} P={pressure:4d}atm "
            f"target={step['target_pressure_GPa']:.4f}GPa "
            f"actual={step['internal_pressure_GPa']:.4f}GPa "
            f"err={step['pressure_error_GPa']:.4f} "
            f"conv={step['converged']} homeo={step['pass']} "
            f"fmax={step['max_force_eV_A']:.4f} dmin={step['min_pair_distance_A']:.4f} "
            f"coord={step['candidate_coordination_lt4p2A']}",
            flush=True,
        )
        if not step["pass"]:
            result["failed_pressure_atm"] = pressure
            result["failed_tick"] = 1000 - pressure
            return result, atoms

    result["pass"] = True
    result["terminal_pressure_atm"] = 0
    result["terminal_tick"] = 1000
    result["terminal_frame_literal"] = f"1000 x {FRAME_SCALE_LITERAL}"
    return result, atoms

def main():
    torch.set_num_threads(max(1, min(4, os.cpu_count() or 1)))
    print("MatterSim A-first-survivor run v2")
    print("torch", torch.__version__, "cpu_threads", torch.get_num_threads())
    print("shell Au79Ag21; pressures", PRESSURE_CHECKS_ATM)
    print("pressure tolerance GPa", PRESSURE_TOL_GPA)
    calc = MatterSimCalculator(device="cpu")

    # User rule: start with a homeostatically balanced Electrum bubble at 1000 atm,
    # THEN add one A candidate.
    base_host = build_electrum()
    host_step = relax(base_host, calc, 1000, "electrum-host")
    print(
        "HOST",
        f"target={host_step['target_pressure_GPa']:.4f}GPa",
        f"actual={host_step['internal_pressure_GPa']:.4f}GPa",
        f"err={host_step['pressure_error_GPa']:.4f}",
        f"conv={host_step['converged']}",
        f"homeo={host_step['pass']}",
        flush=True,
    )
    if not host_step["pass"]:
        payload = {"status":"HOST_NOT_HOMEOSTATIC","host":host_step}
        (OUT / "a_winner.json").write_text(json.dumps(payload, indent=2))
        raise SystemExit(3)

    ledger = []
    winner = None
    winner_atoms = None

    for name, symbol, z in A_CANDIDATES:
        if z > 89:
            ledger.append({
                "candidate": name,
                "symbol": symbol,
                "atomic_number": z,
                "status": "SKIP_OUTSIDE_MATTERSIM_FIRST_89",
            })
            print(f"{name:10s} SKIP z={z} outside first-89 model coverage", flush=True)
            continue

        for cfg in range(1, 17):
            try:
                trial, final_atoms = run_trial(base_host, name, symbol, z, cfg, calc)
            except Exception as exc:
                trial = {
                    "candidate": name,
                    "symbol": symbol,
                    "atomic_number": z,
                    "config_id": cfg,
                    "pass": False,
                    "status": "ERROR",
                    "error": repr(exc),
                    "traceback": traceback.format_exc(),
                }
                final_atoms = None
                print(f"{name} cfg={cfg:02d} ERROR {exc!r}", flush=True)
            ledger.append(trial)
            if trial.get("pass"):
                winner = trial
                winner_atoms = final_atoms
                break
        if winner:
            break

    payload = {
        "model": "MatterSim 1.2.5 / mattersim-v1.0.0-1M checkpoint",
        "device": "cpu",
        "temperature": "0 K geometry/cell relaxation; no finite-T MD",
        "homeostatic_host_at_1000atm": host_step,
        "shell_definition": "pre-relaxed 100-site fcc Electrum host: Au79 Ag21 + one interstitial A candidate",
        "sign_mapping": "16 seam states mapped deterministically to four tetrahedral +/- displacement seeds",
        "pressure_protocol": "1000, 500, 0 atm structural checks after pre-relaxing Electrum host at 1000 atm",
        "pressure_tolerance_GPa": PRESSURE_TOL_GPA,
        "pressure_resolution_note": (
            "MatterSim-v1 benchmark stress errors are larger than a 1-atm increment; "
            "therefore this is a coarse physical screen. The project's 1000 gravitus ticks "
            "remain ledger coordinates rather than 1001 independently resolved physical pressure calculations."
        ),
        "winner": winner,
        "ledger": ledger,
    }
    path = OUT / "a_winner.json"
    path.write_text(json.dumps(payload, indent=2))
    if winner_atoms is not None:
        write(OUT / "a_winner.xyz", winner_atoms)
        write(OUT / "a_winner.cif", winner_atoms)

    print("RESULT_JSON", path)
    if winner:
        print(
            "A_WINNER",
            winner["candidate"],
            winner["symbol"],
            "config", winner["config"]["id"],
            "seams", winner["config"]["seams"],
            "expr", winner["config"]["expression"],
            "pressure", "1000->0 atm",
            "terminal", winner["terminal_pressure_atm"],
            "tick", winner["terminal_tick"],
            flush=True,
        )
        raise SystemExit(0)

    print("A_WINNER NONE", flush=True)
    raise SystemExit(2)

if __name__ == "__main__":
    main()
