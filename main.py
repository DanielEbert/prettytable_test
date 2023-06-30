from __future__ import annotations

import prettytable

from collections import defaultdict

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

results: dict[str, dict[str, int]] = {}

for result in (old_results, new_results):
    for subsys_name, subsys_results in result.items():
        if subsys_name not in results:
            results[subsys_name] = {}
        for runnable_name, runnable_results in subsys_results.items():
            if runnable_name not in results[subsys_name]:
                results[subsys_name][runnable_name] = {}
            for finding_type, finding_count in runnable_results.items():
                if finding_type not in results[subsys_name][runnable_name]:
                    results[subsys_name][runnable_name][finding_type] = finding_count
                else:
                    results[subsys_name][runnable_name][finding_type] += finding_count

t = prettytable.PrettyTable()
t.field_names = ['Subsystem', 'Runnable', 'Finding Type', 'Count']
t.align = 'l'
t.align['Count'] = 'c'

for subsys_name, subsys_results in results.items():
    subsys_column = subsys_name
    for runnable_name, runnable_results in subsys_results.items():
        findings_count = 0
        for i, finding_type in enumerate(runnable_results):
            runnable_column = runnable_name if i == 0 else ''
            divide = True if len(runnable_results) == 1 else False

            t.add_row([subsys_column, runnable_column, finding_type, runnable_results[finding_type]], divider=divide)

            findings_count += runnable_results[finding_type]
            subsys_column = ''

        if len(runnable_results) > 1:
            # Print Summary Row
            t.add_row(['', '', '', '-----'])
            t.add_row(['', '', '', findings_count], divider=True)

table_string = t.get_string()

# postprocess table

rows = table_string.split('\n')

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

print('\n'.join(rows))

