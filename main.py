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


def accumulate_results(single_results: list[dict[str, dict[str, dict[str, int]]]]) -> defaultdict[defaultdict[int]]:
    results = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    for result in single_results:
        for subsys_name, subsys_results in result.items():
            for runnable_name, runnable_results in subsys_results.items():
                for finding_type, finding_count in runnable_results.items():
                    results[subsys_name][runnable_name][finding_type] += finding_count
    return results

def create_table(results: defaultdict[defaultdict[int]]) -> str:
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

results = accumulate_results([old_results, new_results])

table = postprocess_table(create_table(results))

print(table)

