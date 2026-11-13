#!/usr/bin/env python3
"""Writes the full brief of one task for a lane agent to a file. Usage: brief.py <ID> <task file> <lane a|b>
Brief = common.txt + continue.txt + task file + how to report (placeholders __WT__, __BRANCH__, __ID__)."""
import os, sys
SP = os.path.dirname(os.path.abspath(__file__))
tid, fname, lane = sys.argv[1:4]
r = lambda n: open(os.path.join(SP, n)).read().rstrip('\n')
report = ('WHEN YOU ARE DONE, answer with a short report in exactly these parts: DONE (yes only if the acceptance checks passed '
          'and the work is pushed, otherwise no), SUMMARY (what exists now, at most 120 words), COMMITS (short hashes pushed to '
          'origin), TESTS (which checks ran and their results), OPEN POINTS (what is missing, unverified or known broken), '
          'SHARED CHANGES (changes outside your own packages, or none).')
text = '\n\n'.join([r('common.txt'), r('continue.txt'), r(fname), report])
text = text.replace('__WT__', '/home/user/wt/' + lane).replace('__BRANCH__', 'lane-' + lane).replace('__ID__', tid)
os.makedirs(os.path.join(SP, 'out'), exist_ok=True)
out = os.path.join(SP, 'out', tid + '.brief.txt')
open(out, 'w').write(text + '\n')
print(out, len(text), 'bytes')
