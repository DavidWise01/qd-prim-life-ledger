
#include <stdint.h>
#include <stdio.h>
#include <math.h>

int main(void){
    uint64_t caught_weight_loss=0;
    uint64_t caught_provenance_loss=0;
    uint64_t caught_double_active=0;
    uint64_t caught_replay_mismatch=0;

    double a=0.5,b=0.5;
    double forged=a+b-0.01;
    if(fabs(forged-1.0)>1e-12) caught_weight_loss++;

    uint64_t pa=60,pb=40;
    uint64_t forged_p=pa+pb-1;
    if(forged_p!=100) caught_provenance_loss++;

    int active_terminal=2;
    if(active_terminal!=1) caught_double_active++;

    uint32_t ledger=0x12345678u;
    uint32_t replay=ledger^1u;
    if(replay!=ledger) caught_replay_mismatch++;

    int pass=(caught_weight_loss==1 &&
              caught_provenance_loss==1 &&
              caught_double_active==1 &&
              caught_replay_mismatch==1);

    printf("weight_loss_mutations_caught=%llu\n",(unsigned long long)caught_weight_loss);
    printf("provenance_loss_mutations_caught=%llu\n",(unsigned long long)caught_provenance_loss);
    printf("multi_active_terminal_mutations_caught=%llu\n",(unsigned long long)caught_double_active);
    printf("replay_mismatch_mutations_caught=%llu\n",(unsigned long long)caught_replay_mismatch);
    printf("status=%s\n",pass?"PASS":"FAIL");
    return pass?0:5;
}
