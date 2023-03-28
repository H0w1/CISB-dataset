#!/bin/python3

import os
from tabulate import tabulate
import re

ENV_dict = os.environ
spec_cpu_path = ENV_dict.get('SEPC_CPU_2006_PATH')
default_spec_cpu_path = '/cisb_docker/CISB-dataset/spec/cpu2006'

def get_testing_map(file_path):
    # read from the testing result file, generate a map to store the result, return it
    with open (file_path, 'r') as f :
        content = f.read()
        begin = content.find('-----')
        end = content.find('========')
        test_map = {}
        for line in content[begin: end].split('\n')[1:]:
            time = 0
            key = None
            for item in line.split(' '):
                if item != '':
                    time += 1
                    if time == 1:
                        key = item
                        
                    if time == 3:
                        test_map[key] = item
        # get map : {test name in spec2006 : consume time}
        # print(test_map)
        return test_map

def get_options(file_path):
    # read from the testing result file, get the options set of the testing, return it
    with open (file_path, 'r') as f:
        content = f.read()
    pattern = "\"-O.*\""
    search = re.search(pattern, content).span()
    strategy = get_key(content[search[0]:search[1]])
    if not strategy:
        # this result file is not one of our 14 strategies in spec/config/
        return 'others'
    # print(strategy)
    cc = ''
    if 'clang' in content:
        cc = 'clang'
    else :
        cc = 'gcc'
    
    return cc + '_' + strategy

def get_key(option_set):
    l = len(option_set.split('-'))
    if l == 2 or l == 3:
        if 'undefined' in option_set:
            return 'Ubsan.cfg'
        if 'O3' in option_set:
            return 'O3.cfg'
        if 'O2' in option_set:
            return 'O2.cfg'
        if 'O1' in option_set:
            return 'O1.cfg'
        if 'O0' in option_set:
            return 'O0.cfg'
    if l == 16:
        # clang_All-cisb.cfg
        return 'All-cisb.cfg'
    if l == 14:
        # clang_All-ub.cfg
        return 'All-ub.cfg'
    if l == 19:
        # gcc_All-ub.cfg
        return 'All-ub.cfg'
    if l == 59:
        # gcc_All-cisb.cfg
        return 'All-cisb.cfg'
    return None

def get_overhead(dict1, dict2):
    # will return the overhead of using the dict2 strategy, baseling is dict1 strategy
    sum1 = 0
    sum2 = 0
    for key in dict1.keys():
        if key in dict2 and dict1[key].isdigit() and dict2[key].isdigit() :
            sum1 += int(dict1[key])
            sum2 += int(dict2[key])
    return (sum2 - sum1) / sum1

def table6_overhead():
    table6_data = {}
    config_files = ['clang_All-cisb.cfg', 'clang_All-ub.cfg', 'clang_O0.cfg', 'clang_O1.cfg', 'clang_O2.cfg',
                        'clang_O3.cfg', 'clang_Ubsan.cfg', 'gcc_All-cisb.cfg', 'gcc_All-ub.cfg', 'gcc_O0.cfg',
                                        'gcc_O1.cfg', 'gcc_O2.cfg', 'gcc_O3.cfg', 'gcc_Ubsan.cfg']
    
    has_default_spec = os.path.isfile(f'{default_spec_cpu_path}/shrc')
    global spec_cpu_path
    if not spec_cpu_path and not has_default_spec:
        print('please set environment virable SEPC_CPU_2006_PATH, using \"export SEPC_CPU_2006_PATH=\'path/to/spec/cpu2006\'\"')
    else:
        if not spec_cpu_path and has_default_spec:
            spec_cpu_path = default_spec_cpu_path
        result_path = spec_cpu_path + '/result/'
        for parent, dirnames, filenames in os.walk(result_path,  followlinks=True):
            for filename in filenames:
                # get testing results map from data in cpu2006/result/
                # print(filename)
                if not filename.endswith('ref.txt'):
                    continue
                file_path = os.path.join(parent, filename)
                option_set = get_options(file_path)
                testing_result = get_testing_map(file_path)
                if option_set != 'others':
                    table6_data[option_set] = testing_result
        
        for option_set in config_files:
            # check all strategy
            if option_set not in table6_data:
                print('cant read ' + option_set + ' result!')
        
        # print(table6_data)
        
        if (len(table6_data) == 14):
            # all 14 tests in out paper
            table_header = ['Strategy', 'Overhead']
            table_data = []
            print('Table 6: An evaluation of the mitigations provided by the compiler', 'overhead part')
            table_data.append(('clang_O3', 0))
            val = get_overhead(table6_data['clang_O3.cfg'], table6_data['clang_O2.cfg'])
            table_data.append(('clang_O2', val))
            val = get_overhead(table6_data['clang_O3.cfg'], table6_data['clang_O1.cfg'])
            table_data.append(('clang_O1', val))
            val = get_overhead(table6_data['clang_O3.cfg'], table6_data['clang_O0.cfg'])
            table_data.append(('clang_O0', val))
            val = get_overhead(table6_data['clang_O3.cfg'], table6_data['clang_All-cisb.cfg'])
            table_data.append(('clang_All-cisb', val))
            val = get_overhead(table6_data['clang_O3.cfg'], table6_data['clang_All-ub.cfg'])
            table_data.append(('clang_All-ub', val))            
            val = get_overhead(table6_data['clang_O3.cfg'], table6_data['clang_Ubsan.cfg'])
            table_data.append(('clang_Ubsan', val))     
               
            table_data.append(('gcc_O3', 0))
            val = get_overhead(table6_data['gcc_O3.cfg'], table6_data['gcc_O2.cfg'])
            table_data.append(('gcc_O2', val))
            val = get_overhead(table6_data['gcc_O3.cfg'], table6_data['gcc_O1.cfg'])
            table_data.append(('gcc_O1', val))
            val = get_overhead(table6_data['gcc_O3.cfg'], table6_data['gcc_O0.cfg'])
            table_data.append(('gcc_O0', val))
            val = get_overhead(table6_data['gcc_O3.cfg'], table6_data['gcc_All-cisb.cfg'])
            table_data.append(('gcc_All-cisb', val))
            val = get_overhead(table6_data['gcc_O3.cfg'], table6_data['gcc_All-ub.cfg'])
            table_data.append(('gcc_All-ub', val))            
            val = get_overhead(table6_data['gcc_O3.cfg'], table6_data['gcc_Ubsan.cfg'])
            table_data.append(('gcc_Ubsan', val))        
            
            print(tabulate(table_data, headers=table_header, tablefmt='grid'))
        else:
            print('please do all the 14 tests in cpu2006/result/ to genarate table_6_overhead results')
            

if __name__ == '__main__':
    table6_overhead()