import csv

# a dict of tables and their keys
table_key = {
    "dataset/CISB-dataset-classification.csv": "Unique bug id",
    "dataset/CISB-dataset-detailed-info.csv": "Commit/Bugzilla ID",
    "dataset/CISB-dataset-reproduce.csv": "Unique bug id"
}

for t, k in table_key.items():
    with open(t, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
    
    has_redundant = False
    key_column_index = reader.fieldnames.index(k)
    keys = {}
    for row in rows:
        key = row[reader.fieldnames[key_column_index]]
        if key in keys:
            print(f'In {t} found redundant key: {key}')
            has_redundant = True
        else:
            keys[key] = True
    if not has_redundant:
        print(f'{t} has no redundant key')