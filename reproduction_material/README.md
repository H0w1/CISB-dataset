# Reproduction Material

We provide the following reproduction materials:
- testcases for all the reproducted CISB;
- an automatic tool to test whether one CISB is triggered with pre-defined oracles.

## Tested Compilers 

All the test compilers should have been installed if you start by 
using our [Dockerfile](../env/Dockerfile).

The compilers we use in the experiment script are the latest ones that can be 
used to reproduce the CISBs. This group includes 
gcc-4.1, gcc-4.4, gcc-4.9, gcc-7, gcc-12, clang-12, and clang-14.

To help with installation, we provide our own [script](../env/auto_get_compiler.sh) 
that installs these compilers
   ```
cd path/to/aritifact/env
chomod +x auto_get_compiler.sh
sudo auto_get_compiler.sh
```

To check whether all required compilers are installed properly, simply
execute the [scritp](../check-compiler.py).
```
python3 check-compiler.py
```
## Testcases
The source code of these testcases can be found in the folder 
`path/to/artifact/reproduction_material/testcases`.

## The script to check the reproduction

We provide a [script](./reproduction_tester.py) to check the reproduction of each 
single testcase automatically.
- useage:`python3 reproduction_tester.py [-h] [-level LEVEL] [-cc CC] [-opt OPT] file`
- An example to get the reproduction result of `b-1.c` with gcc and compilation options of strategy
"All-cisb" in `compiler_strategies/All-cisb_gcc.txt`.
```
# python3 reproduction_tester.py ./test_cases/b-1.c -level O3 -cc gcc -opt ../compiler_strategies/All-cisb_gcc.txt 2> /dev/null
```
You can create your own config file with the compilation options you want to test and replace `All-cisb_gcc.txt` with the name of your config file when running this test script.

## Test oracle

To automatically check the presence of CISBs of given testcase with certain compiler 
options during the reproduction process, we summarize a list of test oracles.
These test oracles are stored in [**config.yml**](./config.yml).

These are the format of these oracles:
- file_name: The file name of the test program.
- cc: The tested C compiler.
- opti_level: Optimization level (O0/O1/O2/O3).
- input: The input string used for testing.
- check_type: The type of check performed on the output of the program. There are seven types of checks that can be performed:
  - 1: if the output is not test_str, the bug is triggered.
  - 2: if the output is test_str, the bug is triggered.
  - 3: if the disassembly code does not contain test_str in section section_name, the bug is triggered.
  - 4: if the disassembly code contains test_str in section section_name, the bug is triggered.
  - 5: Generate assembly code and check if it does not contain test_str in section section_name, the bug is triggered.
  - 6: Generate assembly code and check if the assembly code contains test_str in section section_name, the bug is triggered.
  - 7: Generate assembly code and check if the assembly code contains test_str in the next line after section_name, the bug is triggered.
- test_str: The string used to detect the presence of the bug.
- section_name: The name of the section in the disassembly code where the test string is searched for. 
  If the section_name begins with the word "between" followed by two strings, it indicates that the
  detector should check the scope between the positions of the two strings in the disassembly code.
