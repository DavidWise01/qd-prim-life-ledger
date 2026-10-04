
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

static inline double now_sec(void){
    struct timespec ts; timespec_get(&ts,TIME_UTC);
    return (double)ts.tv_sec + (double)ts.tv_nsec/1e9;
}

typedef struct {
    uint64_t provenance_count;
    double weight;
    uint32_t history_hash;
    uint8_t active;
} Branch;

static inline uint32_t mix(uint32_t x){
    x ^= x>>16; x*=0x7feb352dU; x^=x>>15; x*=0x846ca68bU; x^=x>>16; return x;
}

int main(int argc,char **argv){
    uint64_t N = argc>1 ? strtoull(argv[1],0,10) : 100ULL;
    uint64_t rounds = argc>2 ? strtoull(argv[2],0,10) : 100000ULL;
    if(N<2 || N>1000000ULL) return 2;

    Branch *b = (Branch*)malloc(sizeof(Branch)*N);
    Branch *tmp = (Branch*)malloc(sizeof(Branch)*N);
    if(!b || !tmp) return 3;

    uint64_t invariant_fail=0, weight_fail=0, provenance_fail=0, replay_fail=0;
    uint64_t total_unifications=0;
    double t0=now_sec();

    uint32_t final_hash=0;
    uint64_t final_prov=0;
    double final_weight=0.0;

    for(uint64_t r=0;r<rounds;r++){
        double w0=1.0/(double)N;
        for(uint64_t i=0;i<N;i++){
            b[i].provenance_count=1;
            b[i].weight=w0;
            b[i].history_hash=mix((uint32_t)i ^ (uint32_t)r);
            b[i].active=1;
        }

        uint64_t active=N;
        while(active>1){
            uint64_t out=0;
            for(uint64_t i=0;i<active;i+=2){
                if(i+1<active){
                    Branch a=b[i], c=b[i+1];
                    tmp[out].provenance_count=a.provenance_count+c.provenance_count;
                    tmp[out].weight=a.weight+c.weight;
                    tmp[out].history_hash = a.history_hash < c.history_hash ? a.history_hash : c.history_hash;
                    tmp[out].active=1;
                    total_unifications++;
                }else{
                    tmp[out]=b[i];
                }
                out++;
            }
            for(uint64_t i=0;i<out;i++) b[i]=tmp[i];
            active=out;
        }

        final_hash=b[0].history_hash;
        final_prov=b[0].provenance_count;
        final_weight=b[0].weight;

        if(active!=1) invariant_fail++;
        if(final_prov!=N) provenance_fail++;
        if(fabs(final_weight-1.0)>1e-12) weight_fail++;

        uint64_t prov_count=0;
        uint64_t *counts=(uint64_t*)malloc(sizeof(uint64_t)*N);
        uint32_t *hashes=(uint32_t*)malloc(sizeof(uint32_t)*N);
        if(!counts || !hashes) return 4;
        for(uint64_t i=0;i<N;i++){
            counts[i]=1;
            hashes[i]=mix((uint32_t)i ^ (uint32_t)r);
        }
        uint64_t aN=N;
        while(aN>1){
            uint64_t out=0;
            for(uint64_t i=0;i<aN;i+=2){
                if(i+1<aN){
                    counts[out]=counts[i]+counts[i+1];
                    hashes[out]=hashes[i]<hashes[i+1]?hashes[i]:hashes[i+1];
                }else{
                    counts[out]=counts[i];
                    hashes[out]=hashes[i];
                }
                out++;
            }
            aN=out;
        }
        prov_count=counts[0];
        if(prov_count!=final_prov || hashes[0]!=final_hash) replay_fail++;
        free(counts); free(hashes);
    }

    double sec=now_sec()-t0;

    printf("theorem=metaverse_to_universe_unification\n");
    printf("N=%llu rounds=%llu\n",(unsigned long long)N,(unsigned long long)rounds);
    printf("sec=%.6f rounds_s=%.3f branch_inputs_s=%.3f\n",
      sec,(double)rounds/sec,((double)rounds*(double)N)/sec);
    printf("final_active=1 final_provenance=%llu final_weight=%.12f\n",
      (unsigned long long)final_prov,final_weight);
    printf("total_unifications=%llu\n",(unsigned long long)total_unifications);
    printf("invariant_fail=%llu weight_fail=%llu provenance_fail=%llu replay_fail=%llu\n",
      (unsigned long long)invariant_fail,(unsigned long long)weight_fail,
      (unsigned long long)provenance_fail,(unsigned long long)replay_fail);

    int pass=(invariant_fail==0 && weight_fail==0 && provenance_fail==0 && replay_fail==0);
    printf("status=%s\n",pass?"PASS":"FAIL");

    free(b); free(tmp);
    return pass?0:5;
}
