/* CPU-only Linux loader shim.  It only reports CUDA unavailable; it never
   replaces the CPU P1·P2·P3 operator.  Needed because the current shared
   library references optional CUDA symbols even when nvcc is absent. */
#include <stdint.h>
int triad_cuda_available(void){return 0;}
const char *triad_cuda_device_name(void){return "";}
int triad_cuda_modal_evolve(float*a,float*b,double*c,int64_t d,int32_t e,int32_t f,const float*g,const float*h,float i,float j,float k,float l,float m,float n,float o,float p,float q,float r,uint64_t s,uint32_t t){return 0;}
int triad_cuda_modal_relax(float*a,float*b,double*c,int64_t d,int32_t e,int32_t f,const float*g,const float*h,float i,float j,float k,float l,float m,float n,float o,float p,float q,float r,uint64_t s){return 0;}
int triad_mr_cuda_evolve(void*a,double*b,const void*c,const double*d,int32_t e,int32_t f,const double*g,const double*h,double i,double j,double k,uint32_t l,int32_t m){return 0;}
