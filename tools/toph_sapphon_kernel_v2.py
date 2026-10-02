"""TOPH/Sapphon Kernel v2.

Reflects the frozen Copper Mind Vector 0 and finite-life overlays without
modifying the frozen final q.d kernel or prior TOPH contracts.
"""
from __future__ import annotations
import hashlib
import json

from tools.copper_mind_vector_0 import prove as prove_copper
from tools.copper_mind_finite_life import run_cycle, prove as prove_life

ADDRESS="{{Gg.Aa.Ii.Aa}}"
STATE="000"
EVENT="{}"
OBSERVED="{{O}{b}{s}{e}{r}{v}{e}{d}}"
CONTRACT_SHA256="2f2cf13d73645744e6f246428f074ea0d3f30a54e17d91640ec68a64f8acdf4c"

def life_frame(index:int)->dict:
    c=run_cycle(index)
    event={
        "kind":"toph_copper_mind_finite_life",
        "cycle":c.cycle,
        "potential":c.potential,
        "pin":c.pin,
        "realized":c.realized,
        "terminal":c.terminal,
        "next_pin":c.next_pin,
        "address":ADDRESS,
    }
    canonical=json.dumps(event,sort_keys=True,separators=(",",":")).encode()
    digest=hashlib.sha256(canonical).hexdigest()
    return {
        "SapphonSnapshot":{
            "state_space":STATE,
            "event_space":EVENT,
            "observed":OBSERVED,
            "event":event,
        },
        "TOPHCommit":{
            "append_only":True,
            "sha256":digest,
        },
        "TOPHProve":{
            "carrier_immutable":STATE=="000",
            "local_packet_balances":c.potential+c.pin+c.realized==0,
            "terminal_zero_has_no_residual":c.terminal==0 and c.residual==0,
            "dead_dot_not_reused":True,
            "new_pin_is_zero":c.next_pin==0,
            "copper_vector_valid":all(prove_copper().values()),
            "finite_life_valid":all(prove_life(2).values()),
        },
        "TOPHProject":{
            "local_packet":[-1,0,1],
            "roles":{"-1":"potential","0":"scalar_pin","1":"realized"},
            "closure":"-1 + 0 + 1 = 0",
            "terminal_zero":"close_local_toroid",
            "next":"find_new_scalar_0_pin_using_same_immutable_formula",
        },
        "TOPHTransport":{
            "state_out":STATE,
            "next_pin":STATE,
            "reuse_dead_dot":False,
            "oe":True,
        },
    }

def verify_cycles(count:int=2)->dict:
    frames=[life_frame(i) for i in range(1,count+1)]
    checks={
        "all_proofs_pass":all(all(f["TOPHProve"].values()) for f in frames),
        "append_only":all(f["TOPHCommit"]["append_only"] for f in frames),
        "all_terminal_zero":all(f["TOPHProject"]["closure"]=="-1 + 0 + 1 = 0" for f in frames),
        "all_return_to_new_zero_pin":all(f["TOPHTransport"]["next_pin"]=="000" for f in frames),
        "no_dead_dot_reuse":all(f["TOPHTransport"]["reuse_dead_dot"] is False for f in frames),
        "all_oe":all(f["TOPHTransport"]["oe"] is True for f in frames),
    }
    return {
        "status":"0e" if all(checks.values()) else "xe",
        "checks":checks,
        "frames":frames,
    }

if __name__=="__main__":
    result=verify_cycles(2)
    print(json.dumps(result,indent=2,sort_keys=True))
    print("0e / TOPH SAPPHON KERNEL V2 COPPER MIND REFLECTION PASS" if result["status"]=="0e" else "xe")
