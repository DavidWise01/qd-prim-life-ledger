#!/usr/bin/env python3
import json, math, os, traceback
from pathlib import Path

import numpy as np
import torch
from ase import Atom
from ase.build import bulk
from ase.filters import FrechetCellFilter
from ase.neighborlist import neighbor_list
from ase.optimize import FIRE
from ase.units import Pascal
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

# User model: one 100-unit Electrum shell = Au79 + Ag21.
HOST_AU = 79
HOST_AG = 21
PRESSURE_CHECKS_ATM = [1000, 500, 0]
FRAME_SCALE_LITERAL = "1.6161x10^-35"

# Four binary signs -> 16 deterministic initial displacement seeds.
TETRA = np.array([
    [ 1.0,  1.0,  1.0],
    [ 1.0, -1.0, -1.0],
    [-1.0,  1.0, -1.0],
    [-1.0, -1.0,  1.0],
], dtype=float)
TETRA /= np.linalg.norm(TETRA[0])

def sign_state(i):
    # i = 0..15. '-' is -1; '+' is +1.
    bits = [(i >> (3-k)) & 1 for k in range(4)]
    signs = np.array([1.0 if b else -1.0 for b in bits])
    disp = (signs[:, None] * TETRA).sum(axis=0) * 0.06
    return {
        "id": i + 1,
        "bits": "".join(str(b) for b in bits),
        "signs": "".join("+" if b else "-" for b in bits),
        "displacement_A": disp.tolist(),
    }

def build_electrum(candidate_symbol, config_id):
    # fcc primitive cell has one lattice site; 5*5*4 = 100 shell atoms.
    atoms = bulk("Au", "fcc").repeat((5, 5, 4))
    assert len(atoms) == 100

    # Deterministic, well-dispersed Au79/Ag21 realization.
    rng = np.random.default_rng(0)
    ag_idx = sorted(rng.choice(len(atoms), size=HOST_AG, replace=False).tolist())
    for idx in ag_idx:
        atoms[idx].symbol = "Ag"

    # Put the added A candidate at a periodic central interstitial seed.
    frac = np.array([0.5, 0.5, 0.5])
    pos = frac @ atoms.cell.array
    ss = sign_state(config_id - 1)
    pos = pos + np.array(ss["displacement_A"], dtype=float)
    atoms.append(Atom(candidate_symbol, position=pos))
    atoms.set_pbc(True)
    return atoms, ss

def host_connected(atoms, cutoff=3.65):
    # Check connectivity of the original 100 Au/Ag shell atoms.
    i, j = neighbor_list("ij", atoms[:100], cutoff)
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

def candidate_coordination(atoms, cutoff=4.0):
    d = atoms.get_distances(100, list(range(100)), mic=True)
    return int(np.sum(np.asarray(d) < cutoff))

def min_pair_distance(atoms):
    d = atoms.get_all_distances(mic=True)
    np.fill_diagonal(d, np.inf)
    return float(np.min(d))

def relax_at_pressure(atoms, calc, pressure_atm):
    atoms.calc = calc
    # ASE scalar_pressure is energy/volume. Positive value applies compression.
    target = pressure_atm * 101325.0 * Pascal
    filt = FrechetCellFilter(atoms, scalar_pressure=target)
    opt = FIRE(filt, logfile=None)
    converged = bool(opt.run(fmax=0.20, steps=60))

    energy = float(atoms.get_potential_energy())
    forces = np.asarray(atoms.get_forces())
    max_force = float(np.max(np.linalg.norm(forces, axis=1)))
    stress = np.asarray(atoms.get_stress(voigt=False))
    finite = bool(
        np.isfinite(energy)
        and np.all(np.isfinite(forces))
        and np.all(np.isfinite(stress))
        and np.isfinite(atoms.get_volume())
    )
    mind = min_pair_distance(atoms)
    coord = candidate_coordination(atoms)
    connected = host_connected(atoms)

    # Structural homeostasis predicate for this tribute run:
    # optimizer converges, quantities finite, no atomic overlap/collapse,
    # Electrum host remains connected, and candidate remains coordinated.
    passed = bool(
        converged and finite and mind > 1.20 and connected and coord > 0
    )
    return {
        "pressure_atm": int(pressure_atm),
        "gravitus_tick": int(1000 - pressure_atm),
        "frame_literal": f"{1000-pressure_atm} x {FRAME_SCALE_LITERAL}",
        "converged": converged,
        "energy_eV": energy,
        "max_force_eV_A": max_force,
        "stress_GPa": (stress / (1e9 * Pascal)).tolist(),
        "volume_A3": float(atoms.get_volume()),
        "min_pair_distance_A": mind,
        "candidate_coordination_lt4A": coord,
        "electrum_host_connected": connected,
        "pass": passed,
    }

def run_trial(name, symbol, z, config_id, calc):
    atoms, ss = build_electrum(symbol, config_id)
    result = {
        "candidate": name,
        "symbol": symbol,
        "atomic_number": z,
        "config": ss,
        "shell": "Au79Ag21 + 1 candidate",
        "shell_atoms": 100,
        "total_atoms": 101,
        "pressure_checks": [],
        "pass": False,
    }
    for pressure in PRESSURE_CHECKS_ATM:
        step = relax_at_pressure(atoms, calc, pressure)
        result["pressure_checks"].append(step)
        print(
            f"{name:10s} cfg={config_id:02d} P={pressure:4d} atm "
            f"conv={step['converged']} homeo={step['pass']} "
            f"fmax={step['max_force_eV_A']:.4f} "
            f"dmin={step['min_pair_distance_A']:.4f} "
            f"coord={step['candidate_coordination_lt4A']}",
            flush=True,
        )
        if not step["pass"]:
            result["failed_pressure_atm"] = pressure
            result["failed_tick"] = 1000 - pressure
            return result
    result["pass"] = True
    result["terminal_pressure_atm"] = 0
    result["terminal_tick"] = 1000
    result["terminal_frame_literal"] = f"1000 x {FRAME_SCALE_LITERAL}"
    return result

def main():
    torch.set_num_threads(max(1, min(4, os.cpu_count() or 1)))
    print("MatterSim A-first-survivor run")
    print("torch", torch.__version__, "cpu_threads", torch.get_num_threads())
    print("shell Au79Ag21; pressures", PRESSURE_CHECKS_ATM)
    calc = MatterSimCalculator(device="cpu")

    ledger = []
    winner = None

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

        candidate_any = False
        for cfg in range(1, 17):
            try:
                trial = run_trial(name, symbol, z, cfg, calc)
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
                print(f"{name} cfg={cfg:02d} ERROR {exc!r}", flush=True)
            ledger.append(trial)
            if trial.get("pass"):
                winner = trial
                candidate_any = True
                break
        if candidate_any:
            break

    payload = {
        "model": "MatterSim-v1 default checkpoint (package default; expected v1.0.0-1M)",
        "device": "cpu",
        "temperature": "0 K geometry relaxation; no finite-T MD",
        "shell_definition": "100-site fcc Electrum host: Au79 Ag21 + one interstitial A candidate",
        "sign_mapping": "16 {-+} states mapped deterministically to four tetrahedral +/- displacement seeds",
        "pressure_protocol": "1000, 500, 0 atm endpoint/midpoint structural checks",
        "pressure_resolution_note": (
            "This is a coarse structural screen. MatterSim-v1 stress errors reported in its model card "
            "are larger than 1-atm increments, so the 1000 symbolic gravitus ticks are logged by the "
            "project ledger but are not claimed as independently resolved physical pressure states."
        ),
        "winner": winner,
        "ledger": ledger,
    }
    path = OUT / "a_winner.json"
    path.write_text(json.dumps(payload, indent=2))
    print("RESULT_JSON", path)
    if winner:
        print(
            "A_WINNER",
            winner["candidate"],
            winner["symbol"],
            "config", winner["config"]["id"],
            "signs", winner["config"]["signs"],
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
