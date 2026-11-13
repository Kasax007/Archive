#!/usr/bin/env python3
"""Builds a lane workflow for ONE task with a quality loop: build, independent reviews (one after the other, each with
its own lens), then fixes of what the reviews found. One agent at a time, so two lanes mean two agents on the machine.
Usage: gen2.py <out.js> <name> <lane a|b> <ID> <task file> <title> <lenses file> [KEY=VALUE ...]
The lenses file holds one lens per paragraph: first line "key: short title", the rest what to look for."""
import json, os, sys
SP = os.path.dirname(os.path.abspath(__file__))
out, name, lane, tid, fname, title, lensfile = sys.argv[1:8]
extra = dict(a.split('=', 1) for a in sys.argv[8:])
r = lambda n: open(os.path.join(SP, n)).read().rstrip('\n')
wt, br = '/home/user/wt/' + lane, 'lane-' + lane


def fill(text):
    text = text.replace('__WT__', wt).replace('__BRANCH__', br).replace('__ID__', tid)
    for k, v in extra.items():
        text = text.replace('__' + k + '__', v)
    return text


build = fill('\n\n'.join([r('common.txt'), r('continue.txt'), r(fname)]))
lenses = []
for para in r(lensfile).split('\n\n'):
    head, _, body = para.strip().partition('\n')
    key, _, short = head.partition(':')
    lenses.append({'key': key.strip(), 'title': short.strip(), 'look': fill(body.strip())})
review = fill(r('review2.txt'))
fix = fill(r('fix2.txt'))
# PRE=<ID>,<lenses file>,<file with what was delivered>: first review and fix that earlier delivery
pre = None
if 'PRE' in extra:
    pid, plens, pdel = extra.pop('PRE').split(',')
    pl = []
    for para in r(plens).split('\n\n'):
        head, _, body = para.strip().partition('\n')
        key, _, short = head.partition(':')
        pl.append({'key': key.strip(), 'title': short.strip(), 'look': body.strip().replace('__ID__', pid)})
    sub = lambda t: t.replace('__WT__', wt).replace('__BRANCH__', br).replace('__ID__', pid)
    pre = {'id': pid, 'lenses': pl, 'review': sub(r('review2.txt')), 'fix': sub(r('fix2.txt')), 'delivered': r(pdel)}
s = 'export const meta = {\n  name: %s,\n  description: %s,\n  phases: [\n' % (json.dumps(name), json.dumps('Lane %s: %s (build, %d independent reviews, fixes)' % (lane.upper(), title, len(lenses))))
if pre:
    s += "    { title: 'Review of %s', detail: %s, model: 'opus' },\n" % (pre['id'], json.dumps('independent reviews of the delivered task: ' + ', '.join(l['title'] for l in pre['lenses'])))
    s += "    { title: 'Fix %s', detail: 'every finding reproduced and fixed, or refuted with evidence', model: 'opus' },\n" % pre['id']
s += "    { title: 'Build', detail: %s, model: 'opus' },\n" % json.dumps(title)
s += "    { title: 'Review', detail: %s, model: 'opus' },\n" % json.dumps('independent reviews: ' + ', '.join(l['title'] for l in lenses))
s += "    { title: 'Fix', detail: 'every finding reproduced and fixed, or refuted with evidence', model: 'opus' },\n  ],\n}\n\n"
s += '''const REPORT = {
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
const FINDINGS = {
  type: 'object',
  properties: {
    findings: {
      type: 'array',
      description: 'defects you can show, the worst first; an empty list is a valid answer',
      items: {
        type: 'object',
        properties: {
          title: { type: 'string', description: 'the defect in one sentence' },
          where: { type: 'string', description: 'file and line, or the screen, command or picture' },
          what_happens: { type: 'string', description: 'what a player or an operator sees, concretely' },
          evidence: { type: 'string', description: 'how you know: the code path, a test you ran, a log line, a picture' },
          severity: { type: 'string', enum: ['breaks play', 'wrong', 'rough'] },
        },
        required: ['title', 'where', 'what_happens', 'evidence', 'severity'],
      },
    },
    checked: { type: 'string', description: 'what you looked at and ran, in two or three sentences' },
  },
  required: ['findings', 'checked'],
}
const FIXED = {
  type: 'object',
  properties: {
    done: { type: 'boolean', description: 'true only if every finding is fixed or refuted, the checks passed and the work is pushed' },
    fixed: { type: 'string', description: 'the findings fixed, each with its commit and its test' },
    refuted: { type: 'string', description: 'the findings that were not defects, each with the evidence' },
    tests: { type: 'string', description: 'which checks ran and their results' },
    open_points: { type: 'string', description: 'what is still open' },
  },
  required: ['done', 'fixed', 'refuted', 'tests', 'open_points'],
}

'''
s += 'const BUILD = %s\nconst REVIEW = %s\nconst FIX = %s\nconst LENSES = %s\n\n' % (json.dumps(build), json.dumps(review), json.dumps(fix), json.dumps(lenses))
if pre:
    s += 'const PRE = %s\n\n' % json.dumps(pre)
    s += '''phase('Review of ' + PRE.id)
const preReviews = []
for (const lens of PRE.lenses) {
  const prompt = PRE.review.replace('__LENS__', lens.title + '. ' + lens.look).replace('__DELIVERED__', PRE.delivered)
  const r = await agent(prompt, { label: PRE.id + ' review: ' + lens.key, phase: 'Review of ' + PRE.id, model: 'opus', effort: 'high', schema: FINDINGS })
  preReviews.push({ lens: lens.key, result: r })
  log(`${PRE.id} review ${lens.key}: ${r ? r.findings.length + ' findings' : 'no result'}`)
}
const preFindings = preReviews.filter(x => x.result).flatMap(x => x.result.findings.map(f => ({ lens: x.lens, ...f })))
let preFixed = null
if (preFindings.length) {
  phase('Fix ' + PRE.id)
  preFixed = await agent(PRE.fix.replace('__FINDINGS__', JSON.stringify(preFindings, null, 1)), { label: PRE.id + ' fixes', phase: 'Fix ' + PRE.id, model: 'opus', effort: 'high', schema: FIXED })
  log(`${PRE.id} fixes: ${preFixed && preFixed.done ? 'done' : 'NOT done'}`)
}

'''
s += '''phase('Build')
const built = await agent(BUILD, { label: %s, phase: 'Build', model: 'opus', effort: 'high', schema: REPORT })
log(`build: ${built && built.done ? 'done' : 'NOT done'}`)
if (!built || !built.done) return { built, pre: typeof preFindings === 'undefined' ? null : { findings: preFindings, fixed: preFixed } }

phase('Review')
const reviews = []
for (const lens of LENSES) {
  const prompt = REVIEW.replace('__LENS__', lens.title + '. ' + lens.look)
    .replace('__DELIVERED__', 'Summary of the engineer: ' + built.summary + ' Commits: ' + built.commits + '. Tests they ran: ' + built.tests + ' Open points they named: ' + built.open_points)
  const r = await agent(prompt, { label: 'review: ' + lens.key, phase: 'Review', model: 'opus', effort: 'high', schema: FINDINGS })
  reviews.push({ lens: lens.key, result: r })
  log(`review ${lens.key}: ${r ? r.findings.length + ' findings' : 'no result'}`)
}
const findings = reviews.filter(x => x.result).flatMap(x => x.result.findings.map(f => ({ lens: x.lens, ...f })))
if (!findings.length) return { built, reviews, fixed: null, pre: typeof preFindings === 'undefined' ? null : { findings: preFindings, fixed: preFixed } }

phase('Fix')
const fixed = await agent(FIX.replace('__FINDINGS__', JSON.stringify(findings, null, 1)), { label: %s, phase: 'Fix', model: 'opus', effort: 'high', schema: FIXED })
log(`fixes: ${fixed && fixed.done ? 'done' : 'NOT done'}`)
return { built, findings, fixed, pre: typeof preFindings === 'undefined' ? null : { findings: preFindings, fixed: preFixed } }
''' % (json.dumps(tid + ' build'), json.dumps(tid + ' fixes'))
open(out, 'w').write(s)
print(out, len(s), 'bytes,', len(lenses), 'lenses')
