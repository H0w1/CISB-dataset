#!/bin/python3
import os

spec_path = '/cisb_docker/CISB-dataset/spec'

config_files = ['clang_All-cisb.cfg', 'clang_All-ub.cfg', 'clang_O0.cfg', 'clang_O1.cfg', 'clang_O2.cfg',
                        'clang_O3.cfg', 'clang_Ubsan.cfg', 'gcc_All-cisb.cfg', 'gcc_All-ub.cfg', 'gcc_O0.cfg',
                                        'gcc_O1.cfg', 'gcc_O2.cfg', 'gcc_O3.cfg', 'gcc_Ubsan.cfg']

for config_file in config_files:
        os.system(f'bash {spec_path}/config/spec.sh {config_file}')