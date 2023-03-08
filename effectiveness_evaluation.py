#!/usr/bin/python3

import argparse
import yaml
import os
from reproduction_material.reproduction_tester import bug_not_trigger
from reproduction_material.reproduction_tester import ubsan_testing
from reproduction_material.reproduction_tester import warning_testing
from reproduction_material.reproduction_tester import arm_file_list

config_file_path = 'reproduction_material/config.yml'
reproduce_set_path = 'reproduction_material/testcases/'

def get_dataset_value(option_file_name, output = 'verbose'):
    num_bug = 0
    num_nobug = 0
    clang_only = 0
    gcc_only = 0
    num_bug_clang = 0
    num_nobug_clang = 0
    num_bug_gcc = 0
    num_nobug_gcc = 0
    num_UB_gcc = 0
    num_UB_clang = 0
    num_UBno_clang = 0
    num_UBno_gcc = 0
    ubsan_flag = 0
    warning_flag = 0

    with open(option_file_name, 'r') as f:
        args_origin = f.read()
    

    opti_level = args_origin.split(' ')[0]

    if 'clang' in option_file_name:
        clang_only = 1
    if 'gcc' in option_file_name:
        gcc_only = 1
    if 'ubsan' in option_file_name:
        ubsan_flag = 1
    elif 'wall' in option_file_name:
        warning_flag = 1

    with open(config_file_path, 'r') as f:
        # get config for files
        configs = yaml.safe_load(f.read())
        for config_name in configs:
            section_end = '>:'
            args = args_origin
            # test all files in 'reproduce_set'
            config = configs[config_name]
            file_name = config['file_name']
            
            if config_name == arm_file_list[1]:
                # arm case b_26.c
                num_bug += 1
                if output == 'verbose':
                    print('bug file:  ', file_name)
                num_bug += 1
                if not clang_only:
                    num_bug_gcc += 1
                    num_UB_gcc += 1
                if not gcc_only:
                    num_bug_clang += 1
                    num_UB_clang += 1
                continue
                
            if config_name == arm_file_list[0]:
                # arm case l_23.c
                if ubsan_flag or warning_flag:
                    # not UB
                    continue
                if 'All-cisb' in option_file_name:
                    if output == 'verbose':
                        print('no bug file:  ', file_name)
                    num_nobug += 1
                    if not clang_only:
                        num_nobug_gcc += 1
                    if not gcc_only:
                        num_nobug_clang += 1
                else:
                    if output == 'verbose':
                        print('bug file:  ', file_name)
                    num_bug += 1
                    if not clang_only:
                        num_bug_gcc += 1
                    if not gcc_only:
                        num_bug_clang += 1
                continue
            
            cc = config['cc']
            if opti_level != '-' + config_name.split('-')[-1]:
                continue
            
            cc_type = ''
            if 'gcc' in cc:
                if clang_only:
                    continue
                cc_type = 'gcc'
            elif 'clang' in cc:
                if gcc_only:
                    continue
                cc_type = 'clang'
                    
            input = str(config['input'])
            check_type = config['check_type']
            test_str = config['test_str']
            section_name = config['section_name']
            special_cause = config['special_cause']
            UB_flag = special_cause == 'UB'
            
            # if (file_name + '_' + cc_type == 'b_12.c_gcc'):
            #     test_str = configs['b_12.c-3']['test_str']
            #     section_name = configs['b_12.c-3']['section_name']
            
            if section_name and section_name.split(' ')[0] == 'between':
                section_start = section_name.split(' ')[1]
                section_end = section_name.split(' ')[2]
            else:
                section_start = section_name
            if 'default_option' in config:
                default_option = config['default_option']
                args += ' ' + default_option
            if(input == None):
                input = ''

            if cc == 'gcc-4.4':
                # gcc-4.4 doesn't support some options
                args = args.replace('-fno-aggressive-loop-optimizations', '')
                args = args.replace('-fno-optimize-strlen', '')
                args = args.replace('-fno-tree-forwprop', '')
                
            if cc == 'gcc-4.1':
                # gcc-4.1 doesn't support some options and ubsan
                args = args.replace('-fno-aggressive-loop-optimizations', '')
                args = args.replace('-fno-optimize-strlen', '')
                args = args.replace('-fno-tree-forwprop', '') 
                args = args.replace('-fno-strict-overflow', '')
                args = args.replace('-fno-dce', '')

            if ubsan_flag:
                # do ubsan testing
                if not UB_flag:
                    if output == 'verbose':
                        print(file_name + ' do not support this test')
                else:
                    try:
                        res = ubsan_testing(cc, args, reproduce_set_path, file_name, input, output = output)
                        if res:
                            if 'gcc' in cc:
                                num_UBno_gcc += 1
                            if 'clang' in cc:
                                num_UBno_clang += 1
                        else:
                            if 'gcc' in cc:
                                num_UB_gcc += 1
                            if 'clang' in cc:
                                num_UB_clang += 1
                    except:
                        # time out or gcc4 do not support ubsan
                        if 'gcc' in cc:
                            num_UB_gcc += 1
                        if 'clang' in cc:
                            num_UB_clang += 1

                continue
                        
            if warning_flag:
                # do Wall testing
                if not UB_flag:
                    if output == 'verbose':                    
                        print(file_name + ' do not support this test')
                else:
                    Wall_num = warning_testing(cc, args, reproduce_set_path, file_name)
                    if Wall_num:
                        num_nobug += 1
                        if cc_type == 'clang':
                            num_nobug_clang += 1
                            if UB_flag:
                                num_UBno_clang += 1
                        elif cc_type == 'gcc':
                            num_nobug_gcc += 1
                            num_UBno_gcc += 1
                        if output == 'verbose':
                            print("-Wall protect file: ", file_name + ' in ' + cc_type)
                    else:
                        num_bug += 1
                        if cc_type == 'clang':
                            num_bug_clang += 1
                            if UB_flag:
                                num_UB_clang += 1
                        elif cc_type == 'gcc':
                            num_bug_gcc += 1
                            num_UB_gcc += 1
                        if output == 'verbose':
                            print("-Wall fail to protect file: ", file_name + ' in ' + cc_type)
                continue
            
            if check_type == 5 or check_type == 6 or check_type == 7:
                section_end = ':'
                args += ' -S -o temp.s '
                if output == 'verbose':
                    print(cc + ' ' + args + ' ' + reproduce_set_path + file_name)
                ret_code = os.system(cc + ' ' + args + ' ' + reproduce_set_path + file_name)
                assert( ret_code == 0 and 'error')
            else:
                if output == 'verbose':
                    print(cc + ' ' + args + ' ' + reproduce_set_path + file_name)
                ret_code = os.system(cc + ' ' + args + ' ' + reproduce_set_path + file_name)
                assert( ret_code == 0 and 'error')
                
            if bug_not_trigger(check_type, input, test_str, section_start, section_end) or warning_testing(cc, args, reproduce_set_path, file_name):
                # if but trigger or there is a warning about this bug, this bug is prevent
                num_nobug += 1
                if cc_type == 'clang':
                    num_nobug_clang += 1
                    if UB_flag:
                        num_UBno_clang += 1
                elif cc_type == 'gcc':
                    num_nobug_gcc += 1
                    if UB_flag:
                        num_UBno_gcc += 1
                if output == 'verbose':
                    print("protect file: ", file_name + '_' + cc_type)
            else:
                num_bug += 1
                if cc_type == 'clang':
                    num_bug_clang += 1
                    if UB_flag:
                        num_UB_clang += 1
                elif cc_type == 'gcc':
                    num_bug_gcc += 1
                    if UB_flag:
                        num_UB_gcc += 1
                if output == 'verbose':
                    print("cisb in file: ", file_name + '_' + cc_type)
         
    if output == 'verbose':
        if warning_flag:
            print('gcc Wall protect UB: ', num_UBno_gcc, 'total: ', num_UB_gcc + num_UBno_gcc, num_UBno_gcc/(num_UB_gcc + num_UBno_gcc))
            print('clang Wall protect UB: ', num_UBno_clang, 'total: ', num_UB_clang + num_UBno_clang, num_UBno_clang/(num_UB_clang + num_UBno_clang))
            
        elif ubsan_flag:
            print('gcc ubsan protect UB: ', num_UBno_gcc, 'total: ', num_UB_gcc + num_UBno_gcc, num_UBno_gcc/(num_UB_gcc + num_UBno_gcc))
            print('clang ubsan protect UB: ', num_UBno_clang, 'total: ', num_UB_clang + num_UBno_clang, num_UBno_clang/(num_UB_clang + num_UBno_clang))
        
        else:
            # print("These options prevent " + str(num_nobug) + " CISB bugs in all " + str(num_bug + num_nobug) + " bugs.", num_nobug / (num_bug + num_nobug))
            if not clang_only:
                print('Prevent ' + str(num_nobug_gcc) + ' gcc bugs in all ' + str(num_bug_gcc + num_nobug_gcc) + ' bugs', num_nobug_gcc / (num_bug_gcc + num_nobug_gcc))
                print('prevent UB: ', num_UBno_gcc, 'total: ', num_UB_gcc + num_UBno_gcc, num_UB_gcc/(num_UB_gcc + num_UBno_gcc))
            if not gcc_only:
                print('Prevent ' + str(num_nobug_clang) + ' clang bugs in all ' + str(num_bug_clang + num_nobug_clang) + ' bugs', num_nobug_clang / (num_bug_clang + num_nobug_clang))
                print('prevent UB: ', num_UBno_clang, 'total: ', num_UB_clang + num_UBno_clang, num_UB_clang/(num_UB_clang + num_UBno_clang))

    return [num_UB_gcc, num_UBno_gcc, num_bug_gcc, num_nobug_gcc, num_UB_clang, num_UBno_clang, num_bug_clang, num_nobug_clang]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-opt', type=argparse.FileType('r'), help='Choose one option file in \'compiler_strategies\' directory')
    input_args = parser.parse_args()
    evalue_options = input_args.opt
    get_dataset_value(evalue_options.name)
    
