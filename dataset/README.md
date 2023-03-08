## Dataset Format

This dataset maintains three tables.

Table 1: CISB-dataset-classification.csv
- This table presents all unique bugs organized according to our three-layer taxonomy.

| Column | Header(\* means the key)        | Description                                                  |
| ------ | ------------------------------- | ------------------------------------------------------------ |
| 1      | Root cause                      | The root cause of the bug (the 1st layer of our taxonomy)    |
| 2      | Insecure optimization behaviors | Insecure optimizations behaviors of the bug (the 2nd layer of our taxonomy) |
| 3      | Security consequences           | Security consequences of the bug (the 3rd layer of our taxonomy) |
| 4      | Security Impacts                | Specific security impacts of the bug                         |
| 5      | Unique bug id\*                 | The identifier (or a list of alias identifier) for each unique bug type with the same cause and impacts; b-(number) for the ones from Bugzilla, l-(number) for the ones from the Linux. |
| 6      | Frequency                       | The number of times we found this kind of bug                |

Table 2: CISB-dataset-detailed-info.csv
- This tables presents more details of each bug report (Bugzilla pages or Git commit logs).

| Column | Header (\* means the key) | Description                                                  |
| ------ | ------------------------- | ------------------------------------------------------------ |
| 1      | Unique bug id             | The identifier for each unique bug type with the same cause and impacts; b-(number) for the ones from Bugzilla, l-(number) for the ones from the Linux |
| 2      | Unique bug name           | A short description to name the bug                          |
| 3      | Occurence                 | The number of times we found this kind of bug                |
| 4      | Source                    | From where we find the bug.                                  |
| 5      | Commit/Bugzilla ID\*      | Linux kernel git commit log or llvm/gcc bugzilla ID.         |
| 6      | Year                      | Time when this bug report is submitted.                      |
| 7      | First appearance          | Time when this kind of bugs is firstly submitted.            |
| 8      | Security impacts          | Specific security impacts of the bug                         |
| 9      | Specific cause            | The sub classification of Implicit-Specification. See the definition of No-UB, default-behavior or environment assumption in our paper |

Table 3: CISB-dataset-reproduce.csv
- This table presents the reproduction result of CISBs in our dataset.

| Column | Header(\* means the key)   | Description                                                  |
| ------ | -------------------------- | ------------------------------------------------------------ |
| 1      | Unique bug id\*            | The identifier for each unique bug type with the same cause and impacts; b-(number) for the ones from Bugzilla, l-(number) for the ones from the Linux |
| 2      | Result                     | The result of our reproducation                              |
| 3      | Compiler version:gcc       | The compiler(gcc) version we reproduce the bug               |
| 4      | Compiler version:llvm      | The compiler(llvm) version we reproduce the bug              |
| 5      | Compiler Explorer snapshot | An online compiler snapshot that preserve the code to reproduce the bug |
