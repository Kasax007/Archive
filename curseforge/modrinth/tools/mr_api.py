"""Small Modrinth API helper. The token is read from $SP/.mr_token at call time and never printed or logged."""
import json, os, urllib.request, urllib.error, uuid

SP = '/tmp/claude-0/-home-user/4ca9508b-4f8c-5a8e-91dc-6059d6cc887c/scratchpad'
UA = 'Kasax007-release-sync/1.0'
LOG = f'{SP}/mr/api.log'


def _token():
    return open(f'{SP}/.mr_token').read().strip()


def call(method, path, body=None, raw=None, ctype=None, base='https://api.modrinth.com'):
    url = base + path
    headers = {'User-Agent': UA, 'Authorization': _token()}
    data = None
    if body is not None:
        data = json.dumps(body).encode(); headers['Content-Type'] = 'application/json'
    elif raw is not None:
        data = raw; headers['Content-Type'] = ctype or 'application/octet-stream'
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            code, text = r.status, r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        code, text = e.code, e.read().decode('utf-8', 'replace')
    with open(LOG, 'a') as f:
        f.write(f'{method} {path} -> {code} {text[:300]}\n')
    try:
        return code, json.loads(text) if text else None
    except ValueError:
        return code, text


def multipart(fields, files):
    """fields: {name: json-able}, files: [(part name, file name, bytes)] -> (body, content type)"""
    b = uuid.uuid4().hex
    out = []
    for k, v in fields.items():
        out.append(f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\nContent-Type: application/json\r\n\r\n'.encode()
                   + json.dumps(v).encode() + b'\r\n')
    for part, fname, data in files:
        out.append(f'--{b}\r\nContent-Disposition: form-data; name="{part}"; filename="{fname}"\r\n'
                   f'Content-Type: application/java-archive\r\n\r\n'.encode() + data + b'\r\n')
    out.append(f'--{b}--\r\n'.encode())
    return b''.join(out), f'multipart/form-data; boundary={b}'
