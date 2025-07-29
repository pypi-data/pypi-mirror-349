#ifdef __OPENCL_VERSION__
#define Size ulong
#define Int int
#else
#define Size uint64_t
#define Int int32_t
#include <cfloat>
#endif

#define Real float
#define MODULE core1
#define VERY_SMALL_NUMBER 1e-20f

#ifdef __OPENCL_VERSION__
#define exp native_exp
#define log native_log
#define sqrt native_sqrt
#endif

#define MODULE_DOC                                                             \
  "Single-precision implementation\n-------------------------------\n.. "      \
  "currentmodule:: pigreads\n"
