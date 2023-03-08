import csv
from tabulate import tabulate
from spec.get_spec2006_result import table6_overhead

bug_class = "dataset/CISB-dataset-classification.csv"
bug_detail = "dataset/CISB-dataset-detailed-info.csv"

class unique_bug:
    def __init__(self, id, bug_class):
        self.id = id
        self.id_alias_list = self.id.split(' ')
        self.bug_class = bug_class
        self.occurance = []

bugs = []
with open(bug_class, mode = 'r', encoding='utf-8-sig') as c:
    reader = csv.DictReader(c)
    class_rows = list(reader)

# ubug_id_index = reader.fieldnames.index('Unique bug id')
# ubug_class_idx = reader.fieldnames.index('Insecure optimization behaviors')
bug_class_map = {
    "Eliminating security related code": "IS1",
    "Reordering order-sensitive security code": "IS2",
    "Introducing insecure instructions": "IS3",
    "Making sensitive data out of bound": "OS1",
    "Breaking timing guarantees": "OS2",
    "Introducing insecure micro-architectural side effect": "OS3"
}

for line in class_rows:
    if line:
        bid = line["Unique bug id"]
        bclass= bug_class_map[line["Insecure optimization behaviors"]]
        new_bug = unique_bug(bid, bclass)
        bugs.append(new_bug)   

with open(bug_detail, mode = 'r', encoding='utf-8-sig') as t:
    reader = csv.DictReader(t)
    detail_rows = list(reader)

for line in detail_rows:
    if line:
        bid = line["Unique bug id"]
        byear = line["Year"]
        # bkey = line[bug_key_idx]
        for b in bugs:
            if bid in b.id_alias_list:
                b.occurance.append(byear)
                break
        else:
            print('unknown bug', line)            

s = set()
for b in bugs:
    if set(b.id_alias_list).intersection(s):
        print('bug id is not unique')
        print(b.id, set(b.id_alias_list).intersection(s))
        exit(0)
    s.update(b.id_alias_list)

def table_2():
    print('Table 2: Statistics of bugs reported to Bugzilla and in the Linux kernel')
    taxonomy = ['IS1', 'IS2', 'IS3', 'OS1', 'OS2', 'OS3']
    num_all = 0
    for b in bugs:
        num_all += len(b.occurance)

    bug_occ = dict()
    with open(bug_detail, mode = 'r', encoding='utf-8-sig') as t:
        reader = csv.DictReader(t)
        detail_rows = list(reader)
    for line in detail_rows:
        if line:
            bid = line["Unique bug id"]
            byear = line["Year"]
            bug_occ.setdefault(bid, []).append(byear) 

    data = []
    for bc in taxonomy:
        num_ubug = num_bug = 0
        num_bugzilla_ubug = num_bugzilla_bug = 0
        num_linux_ubug = num_linux_bug = 0
        for b in bugs:
            if b.bug_class == bc:
                num_ubug += 1
                num_bug += len(b.occurance)
                for alias in b.id_alias_list:
                    if alias not in bug_occ.keys():
                        print('Unique bug not found ', alias)
                        continue
                    # alias bugs are the same unique bug 
                    b_counted = l_counted = False
                    if alias.startswith('b-'):
                        if not b_counted:
                            num_bugzilla_ubug += 1
                            b_counted = True
                        num_bugzilla_bug += len(bug_occ[alias])
                    elif alias.startswith('l-'):
                        if not l_counted:
                            num_linux_ubug += 1
                            l_counted = True
                        num_linux_bug += len(bug_occ[alias])

        row = [num_ubug, num_bug]
        row += [num_bug/num_all]
        row += [num_bugzilla_ubug, num_bugzilla_bug]
        row += [num_linux_ubug, num_linux_bug]
        data.append(row)   

    headers = ["BugClass", "UniBug", "Num", "P", "UniBz", "NumBz", "UniLinux", "NumLinux"]

    contents = []
    for i in range(len(taxonomy)):
        contents.append([taxonomy[i]] + data[i])

    # Calculate the summary of each column
    row_sums = [sum(row[i] for row in data) for i in range(len(data[0]))]
    summary = ["Total"] + row_sums
    contents.append(summary)

    # Use tabulate to print the table
    print(tabulate(contents, headers=headers, showindex=False, floatfmt=".2f", tablefmt='fancy_grid'))                   


def table_3():
    print('Table 3: Temporal distribution (report date) of bug classes')
    class_occurance = dict()
    for b in bugs:
        class_occurance.setdefault(b.bug_class, []).extend(b.occurance)

    class_occurance_statistic = dict()
    for c,o in class_occurance.items():
        # Years 04-06 07-09 10-12 13-15 16-18 19-21
        p = [0] * 6
        for year in o:
            if int(year) <= 2006:
                p[0] += 1
            elif int(year) <= 2009:
                p[1] += 1
            elif int(year) <= 2012:
                p[2] += 1
            elif int(year) <= 2015:
                p[3] += 1
            elif int(year) <= 2018:
                p[4] += 1
            else:
                p[5] += 1
        class_occurance_statistic[c] = p


        # Add a summary row and column to the dictionary object
    for key, value in class_occurance_statistic.items():
        class_occurance_statistic[key].append(sum(value))
    class_occurance_statistic['Total'] = [sum(x) for x in zip(*class_occurance_statistic.values())]

    # Convert the dictionary to a list of lists for tabulate
    table = [[key, *value] for key, value in class_occurance_statistic.items()]

    # Print the table using tabulate and specify row and column headers
    print(tabulate(table, headers=['', '04-06', '07-09', '10-12', '13-15', '16-18', '19-21', 'Total'], tablefmt='fancy_grid'))


class mitigation_work():
    def __init__(self, name, scope):
        self.name = name
        self.scope = scope
        self.target_cisb = set()
    
    def add_cisb(self, cisb_list):
        self.target_cisb.update(cisb_list)
    

def table_7():
    # the bug number of each bug class
    print('Table7: Automatic Prevention works')
    bug_class_occ = dict()
    for b in bugs:
        bug_class_occ.setdefault(b.bug_class, 0) 
        bug_class_occ[b.bug_class] += len(b.occurance)
    
    mitigation_target_map = {
        'UBSan': ['IS1', 'IS2', 'IS3'],
        'ThreadSan': ['IS1', 'IS2', 'IS3'],
        'TySan': ['IS1', 'IS2', 'IS3'],
        'Ct-verif, Jasmin, FaCT, CT-wasm, Simon, Barthe': ['OS2'],
        'Besson': ['OS1'],
        'Patrignani': ['OS3'],
        'STACK': ['IS1'],
        'Unisan': ['OS1'],
        'Yang': ['OS1'],
        'K-Hunt': ['OS2'],
        'Sprundel': ['OS1'],
        'Wu': ['IS1', 'IS2', 'IS3'],
        'SpecFuzz, SpecTaint': ['OS3'],
        'KUBO': ['IS1', 'IS2', 'IS3']
    }

    mitigation_cisb_map = {
        'UBSan': ['l-13', 'l-8', 'l-24', 'b-8', 'b-9', 'b-11', 'b-4', 'b-14'],
        'ThreadSan': ['b-12', 'l-5', 'l-40', 'l-46', 'l-30', 'l-49', 'l-3', 'l-21', 'l-4', 'l-4a'],
        'TySan': ['b-13', 'b-26'],
        'Ct-verif, Jasmin, FaCT, CT-wasm, Simon, Barthe': ['l-6'],
        'Besson': ['l-9', 'b-21'],
        'Patrignani': ['l-25'],
        'STACK': ['l-13', 'l-8', 'l-24', 'b-8', 'b-9', 'b-10'],
        'Unisan': ['l-11', 'l-29', 'b-22'],
        'Yang': ['l-9', 'b-21'],
        'K-Hunt': ['l-6'],
        'Sprundel': ['l-9', 'b-21'],
        'Wu': ['l-13', 'l-8', 'b-2', 'l-24', 'b-8', 'b-9', 'b-10', 'b-12', 'b-5', 'b-6', 'l-30', 'b-4'],
        'SpecFuzz, SpecTaint': ['l-25'],
        'KUBO': ['l-13', 'l-8', 'l-24', 'b-9', 'b-10', 'b-11', 'b-4']
    }

    mitigation_cisb_commets = {
        'Wu': "we suppose they can prevent all UB-based elimination bugs caused by clang",
        'KUBO': "the UB types they support are shown in their Table II"
    }

    mitigation_works = {}

    for mitigation, targets in mitigation_target_map.items():
        cisb = mitigation_cisb_map[mitigation]
        mitigation_works[mitigation] = mitigation_work(mitigation, targets)
        mitigation_works[mitigation].add_cisb(cisb)

    mitigation_rate = []
    for m in mitigation_works.values():
        ucisb_set = set()
        for b in bugs:
            for cisb in m.target_cisb:
                if cisb in b.id_alias_list:
                    ucisb_set.add(b.id)
        target_cisb_num = 0
        for b in bugs:
            for ucisb in ucisb_set:
                if b.id == ucisb:
                    target_cisb_num += len(b.occurance)
        scope_bug_num = 0
        for t in m.scope:
            scope_bug_num += bug_class_occ[t]
        mitigation_rate.append([m.name, m.scope, target_cisb_num/scope_bug_num])
    print(tabulate(mitigation_rate, headers=["Automatic Prevention", "Target CISB type", "Percentage"], floatfmt=".2f", tablefmt='fancy_grid'))

    mitigation_cisb_info = []
    for m, scope in mitigation_target_map.items():
        mitigation_cisb_info.append([m, scope, mitigation_cisb_map[m]])
    print(tabulate(mitigation_cisb_info, headers=["Automatic Prevention", "Target CISB type", "Target CISB"], tablefmt='fancy_grid'))
    
        
def table_6_eff():
    from effectiveness_evaluation import get_dataset_value
    print('Table 6: An evaluation of the mitigations provided by the compiler')
    
    file_path = 'compiler_strategies'
    strategy = ['O3', 'O2', 'O1', 'O0', 'All-ub_clang', 'All-ub_gcc', 'All-cisb_gcc', 'All-cisb_clang', 'ubsan', 'wall']
    table_header = ['Strategy', '', 'Eff.(UB-CISB)',  'Eff. (all CISB)']
    table_data = []
    for s in strategy:
        res = get_dataset_value(file_path + '/' + s + '.txt', output=None)
        if 'ub' in s or s == 'wall':
            if 'clang' not in s:
                table_data.append((s, 'gcc', res[1]/(res[1]+res[0]), '/'))
            if 'gcc' not in s:
                table_data.append((s, 'clang', res[5]/(res[5]+res[4]), '/'))
            continue
        if 'clang' not in s:
            table_data.append((s, 'gcc', res[1]/(res[1]+res[0]), res[3]/(res[3]+res[2])))
        if 'gcc' not in s:
            table_data.append((s, 'clang', res[5]/(res[5]+res[4]), res[7]/(res[7]+res[6])))
    print(tabulate(table_data, headers=table_header, tablefmt='fancy_grid'))

def table_6_overhead():
    table6_overhead()

def show_human_failed_prevention():
    human_fail_list = {'l-9': ["d4c5efdb97773f59a2b711754ca0953f24516739", "0b053c9518292705736329a8fe20ef4686ffc8e9", "7829fb09a2b4268b30dd9bc782fa5ebee278b137"]}
    for unique_bug, reports in human_fail_list.items():
        print(f'Evidence that programmers failed to prevent a CISB:')
        print(f'for {unique_bug}, these bug reports are the evidence {reports}.')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-exp', default='all', type=str, help='To specify which experiment(s) to run')
    args = parser.parse_args()
    if args.exp == "cisb-statistics":
        table_2()
        table_3()
    elif args.exp == "mitigation-evaluation":
        show_human_failed_prevention()
        table_6_eff()
        table_6_overhead()
    elif args.exp == "human-mitigation":
        show_human_failed_prevention()
    elif args.exp == "mitigation-effectiveness":
        table_6_eff()
    elif args.exp == "mitigation-overhead":
        table_6_overhead()
    elif args.exp == "target-cisb":
        table_7()
    elif args.exp == "all":
        table_2()
        table_3()
        show_human_failed_prevention()
        table_6_eff()
        table_6_overhead()
        table_7()
    else:
        print("Not a correct argument. Choose one from: all, cisb-statistics, human-mitigation, mitigation-evaluation, mitigation-effectiveness, mitigation-overhead, target-cisb") 
