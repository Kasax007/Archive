#!/usr/bin/env python3
"""Builds a lane workflow script from brief files.
Usage: gen.py <out.js> <name> <lane a|b> <description> <ID=file.txt|title|detail> ...
Each task prompt = common.txt + continue.txt + the task file (placeholders __WT__, __BRANCH__, __ID__)."""
import json, os, sys
SP = os.path.dirname(os.path.abspath(__file__))
out, name, lane, desc = sys.argv[1:5]
common = open(os.path.join(SP, 'common.txt')).read().rstrip('\n')
cont = open(os.path.join(SP, 'continue.txt')).read().rstrip('\n')
wt, br = '/home/user/wt/' + lane, 'lane-' + lane
tasks = []
for spec in sys.argv[5:]:
    idfile, title, detail = spec.split('|')
    tid, fname = idfile.split('=')
    text = open(os.path.join(SP, fname)).read().rstrip('\n')
    prompt = (common + '\n\n' + cont + '\n\n' + text).replace('__WT__', wt).replace('__BRANCH__', br).replace('__ID__', tid)
    tasks.append((tid, title, detail, prompt))
s = 'export const meta = {\n  name: %s,\n  description: %s,\n  phases: [\n' % (json.dumps(name), json.dumps(desc))
for tid, title, detail, _ in tasks:
    s += "    { title: %s, detail: %s, model: 'opus' },\n" % (json.dumps(title), json.dumps(detail))
s += '''  ],
}

const REPORT = {
  type: 'object',
  properties: {
    done: { type: 'boolean', description: 'true only if the acceptance checks passed and the work is pushed' },
    summary: { type: 'string', description: 'what exists now, at most 120 words' },
    commits: { type: 'string', description: 'short hashes pushed to origin' },
    tests: { type: 'string', description: 'which checks ran and their results' },
    open_points: { type: 'string', description: 'what is missing, unverified or known broken' },
    shared_changes: { type: 'string', description: 'changes outside your own packages, or none' },
  },
  required: ['done', 'summary', 'commits', 'tests', 'open_points', 'shared_changes'],
}

const TASKS = [
'''
for tid, title, detail, prompt in tasks:
    s += '  { key: %s, title: %s, prompt: %s },\n' % (json.dumps(tid), json.dumps(title), json.dumps(prompt))
s += '''];

const results = {}
for (const t of TASKS) {
  phase(t.title)
  const r = await agent(t.prompt, { label: t.title, phase: t.title, model: 'opus', effort: 'high', schema: REPORT })
  results[t.key] = r
  log(`${t.title}: ${r && r.done ? 'done' : 'NOT done'}`)
  if (!r || !r.done) break
}
return results
'''
open(out, 'w').write(s)
print(out, len(s), 'bytes,', len(tasks), 'tasks')
