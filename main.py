from __future__ import annotations

import prettytable

from collections import defaultdict
from collections import Counter
import dataclasses
import json

old_results = {
    'CCP': {
        'RbpCcpOcp': {
            'Assertion Failure': 3,
            'Divide by Zero': 4,
        },
        'RbpCcpOoc': {
            'Stack Buffer Overflow': 3,
        }
    }
}

new_results = {
    'CCP': {
        'RbpCcpOcp': {
            'Integer Overflow': 1,
            'Divide by Zero': 5,
        }
    },
    'PSD': {
        'XCZ': {
            'asd Overflow': 1,
            'Divide by Zero': 5,
        }
    }
}


findings = {
    'CCP': {
        'RbpCcpOcp': [
            {
                'epoch_timestamp': 1688227256,
                'timestamp': '01.07.2023 18:01:33',   # use same name as folder here
                'branch': 'develop',
                'commit': 'b5d7664',
                'commit_timestamp': '24.06.2023 12:05:17',
                'bug_type': 'Divide by Zero',
                'artifactory_folder': '2023_07_01_19_39_22/findings/crashes/0'
            },
        ],
        'RbpCcpOoc': [
            {
                'epoch_timestamp': 1688227256,
                'timestamp': '01.07.2023 18:01:33',   # use same name as folder here
                'branch': 'develop',
                'commit': 'b5d7664',
                'commit_timestamp': '24.06.2023 12:05:17',
                'bug_type': 'Divide by Zero',
                'artifactory_folder': '2023_07_01_19_39_22/findings/crashes/0'
            },
        ]
    },
    'PSD': {
        'XYZ': [
            {
                'epoch_timestamp': 1688227256,
                'timestamp': '01.07.2023 18:01:33',   # use same name as folder here
                'branch': 'develop',
                'commit': 'b5d7664',
                'commit_timestamp': '24.06.2023 12:05:17',
                'bug_type': 'Divide by Zero',
                'artifactory_folder': '2023_07_01_19_39_22/findings/crashes/0'
            }
        ]
    }
}

@dataclasses.dataclass
class Finding:
    epoch_timestamp: int
    timestamp: str
    branch: str
    commit: str
    commit_timestamp: str
    bug_type: str
    artifactory_folder: str

# subsys and runnable known
f1 = Finding(1688227257, '01.07.2023 18:01:33', 'develop', 'b5d7664', '24.06.2023 12:05:17', 'Divide by Zero', '2023_07_01_19_39_22/findings/crashes/1')
f2 = Finding(1688227259, '01.07.2023 18:02:33', 'develop', 'b5d7664', '24.06.2023 12:05:17', 'Integer Overflow', '2023_07_01_19_39_22/findings/crashes/2')
f3 = Finding(1688227259, '01.07.2023 18:02:33', 'develop', 'b5d7664', '24.06.2023 12:05:17', 'Divide by Zero', '2023_07_01_19_39_22/findings/crashes/3')

def add_findings(findings, subsys, runnable, new_findings):
    for finding in new_findings:
        if subsys not in findings:
            findings[subsys] = {}
        if runnable not in findings[subsys]:
            findings[subsys][runnable] = []
        findings[subsys][runnable].insert(0, dataclasses.asdict(finding))

add_findings(findings, 'CCP', 'RbpCcpOcp', [f1, f2, f3]) 
print(json.dumps(findings, indent=2))

def create_findings_table(findings: dict[str, dict[str, list[dict[str, str | int]]]]) -> str:
    t = prettytable.PrettyTable()
    t.field_names = ['Subsystem', 'Runnable', 'Detection Timestamp', 'Finding Type', 'Artifactory Folder', 'Branch', 'Commit']
    t.align = 'l'

    for subsys_name, subsys_findings in findings.items():
        subsys_column = subsys_name
        for runnable_name, runnable_findings in subsys_findings.items():
            previous_column = defaultdict(lambda: None)
            for i, finding in enumerate(runnable_findings):
                runnable_column = runnable_name if i == 0 else ''
                divide = True if len(runnable_findings) - 1 == i else False

                column_names = ['timestamp', 'bug_type', 'artifactory_folder', 'branch', 'commit']
                columns = []

                for name in column_names:
                    if name not in finding:
                        # log.warn...
                        columns.append('Unknown')
                        previous_column[name] = None
                        continue
                    if finding[name] != previous_column[name] or name == 'bug_type':
                        columns.append(finding[name])
                    else:
                        columns.append('')
                    previous_column[name] = finding[name]

                t.add_row([subsys_column, runnable_column] + columns, divider=divide)

                subsys_column = ''

    return t.get_string()

def create_finding_count_table(findings: dict[str, dict[str, list[dict[str, str | int]]]]) -> str:
    t = prettytable.PrettyTable()
    t.field_names = ['Subsystem', 'Runnable', 'Finding Type', 'Count']
    t.align = 'l'
    t.align['Count'] = 'c'

    for subsys_name, subsys_findings in findings.items():
        subsys_column = subsys_name
        for runnable_name, runnable_findings in subsys_findings.items():
            finding_counts = Counter([f['bug_type'] for f in runnable_findings]).most_common()

            for i, (finding, count) in enumerate(finding_counts):
                runnable_column = runnable_name if i == 0 else ''
                divide = True if len(finding_counts) == 1 else False

                t.add_row([subsys_column, runnable_column, finding, count], divider=divide)
                subsys_column = ''

            if len(finding_counts) > 1:
                # Print Summary Row
                t.add_row(['', '', '', '-----'])
                t.add_row(['', '', '', len(runnable_findings)], divider=True)

    return t.get_string()

def postprocess_table(table: str) -> str:
    rows = table.split('\n')

    for i, row in enumerate(rows[1:-1], start=1):
        prev_row = rows[i-1]
        next_row = rows[i+1]
        
        if row[3] == '-' and next_row[3] == ' ':
            subsys_column_size = 0
            for c in row[1:]:
                if c != '-':
                    break
                subsys_column_size += 1
            rows[i] = '|' + ' ' * subsys_column_size + row[subsys_column_size + 1:]

    return '\n'.join(rows)

findings_table = postprocess_table(create_findings_table(findings))
print(findings_table)

count_table = postprocess_table(create_finding_count_table(findings))
print(count_table)

