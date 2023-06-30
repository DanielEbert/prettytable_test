from __future__ import annotations

import prettytable

results = {
    'RbpCcpOcp': {
        'Assertion Failure': 3,
        'Divide by Zero': 4,
    },
    'RbpCcpOoc': {
        'Stack Buffer Overflow': 3,
    }
}

t = prettytable.PrettyTable()
t.field_names = ['Runnable', 'Finding Type', 'Count']
t.align = 'l'
t.align['Count'] = 'c'

for runnable_name in results:
    runnable = results[runnable_name]
    findings_count = 0
    for i, finding_type in enumerate(runnable):
        runnable_column = runnable_name if i == 0 else ''
        divide = True if i == len(runnable) - 1 else False
        t.add_row([runnable_column, finding_type, runnable[finding_type]], divider=False)
        findings_count += runnable[finding_type]
    if len(runnable) > 1:
        # Print Summary Row
        t.add_row(['','','-----'])
        t.add_row(['','',findings_count], divider=True)

print(t)

