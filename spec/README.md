# Setup for SPEC CPU 2006 
1. Install [SPEC CPU2006 Benchmark](https://www.spec.org/cpu2006/).
- Please note that we can't share SPEC CPU2006 here becuase it is commercial.

2. After obtaining SPEC CPU2006 Benchmark, it is needed to 
**place the `cpu2006` folder under the `spec` directory**，which is automatically 
setted if you follow the [installation guide](../README.md#artifact-setup).

3. To set up SPEC CPU 2006, please follow the instructions below:
```
cd path/to/artifact/spec
cp -r config cpu2006
cd cpu2006
source ./shrc
```

# Performance evaluation of compiler mitigations
To measure the performance overhead of each compiler strategy separately, we 
provide the following script to run SPEC CPU 2006 Benchmark. Here is an example 
of how to test the performance of gcc with O3 optimization:
```
cd path/to/artifact/spec
bash config/spec.sh gcc_O3.cfg
```
You can replace gcc_O3.cfg with the config file name of the compiler strategy 
you want to test.

> Note that it may take about 3-8 hours to do one test. 

The test result files generated under path/to/spec/result are in the format
"CINT2006.*.rerf.txt", where * represents a number that increases with the number 
of experiments.

To identify which test a particular result file corresponds to, you should check 
the compiler and compiler options listed in the report. The results will indicate 
the performance of the compiled binary with chosen compiler options.

We also provide a script to run the tests of all the compiler strategies in on step:
```
python3 config/test_all.py
```

**Expected build errors for C++ benchmarks and `perlbench`.**
Please note that build errors may occur when attempting to compile C++ benchmarks 
and `perlbench`. These issues are expected, as we solely focus on C benchmarks 
and do not include C++ benchmarks for our dataset. Additionally, we found 
that `perlbench` is incompatible with the modern compilers we tested. 

## SPEC CPU 2006 config files
Below is the config file and compiler options used for each compiler strategy we test. 
The config file can be found in `path/to/artifact/spec`:

   | File name          | Compiler options                                             |
   | ------------------ | ------------------------------------------------------------ |
   | gcc_O3.cfg         | -O3                                                          |
   | clang_O3.cfg       | -O3                                                          |
   | gcc_O2.cfg         | -O2                                                          |
   | clang_O2.cfg       | -O2                                                          |
   | gcc_O1.cfg         | -O1                                                          |
   | clang_O1.cfg       | -O1                                                          |
   | gcc_O0.cfg         | -O0                                                          |
   | clang_O0.cfg       | -O0                                                          |
   | gcc_All-UB.cfg     | -O3 -fno-strict-overflow -fwrapv -fno-delete-null-pointer-checks -fno-strict-aliasing -fno-aggressive-loop-optimizations |
   | clang_All-UB.cfg   | -O3 -fno-strict-overflow  -fno-delete-null-pointer-checks   -fno-strict-aliasing -fwrapv |
   | gcc_All-CISB.cfg   | -O3 -fno-tree-dominator-opts -fno-tree-vrp -fno-tree-fre   -fno-strict-overflow -fno-dce -fno-tree-ccp -fno-tree-copy-prop   -fno-tree-forwprop -fno-tree-ter -fno-tree-pre  -fno-strict-aliasing -fno-aggressive-loop-optimizations  -fno-builtin   -fno-tree-dse -fno-optimize-strlen -fno-tree-dce -fno-cse-follow-jumps  -fno-unswitch-loops |
   | clang_All-CISB.cfg | -O3 -fno-builtin -fno-strict-overflow  -fno-strict-aliasin -fwrapv -fno-delete-null-pointer-checks |
   | gcc_UBSan.cfg      | -O3 -fsanitize=undefined                                     |
   | clang_UBSan.cfg    | -O3 -fsanitize=undefined                                     |

   