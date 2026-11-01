"""Builds the next modpack and server pack from the last ones: only Challenge Craft changes.

mkpacks.py server OLD_SERVER.zip NEW_JAR OUT.zip OLD_TAG NEW_TAG
mkpacks.py client OLD_CLIENT.zip OUT.zip OLD_TAG NEW_TAG MOD_FILE_ID
"""
import re
import sys
import zipfile
from pathlib import Path


def copy_info(info, name):
    out = zipfile.ZipInfo(name, date_time=info.date_time)
    out.compress_type = info.compress_type
    out.external_attr = info.external_attr
    out.create_system = info.create_system
    out.comment = info.comment
    return out


def server(old, jar, out, old_tag, new_tag):
    jar = Path(jar)
    src = zipfile.ZipFile(old)
    root_old = f"Serverpack Challenge Craft 26.3-{old_tag}/"
    root_new = f"Serverpack Challenge Craft 26.3-{new_tag}/"
    old_jars = [i for i in src.infolist() if re.fullmatch(re.escape(root_old) + r"mods/challengecraft-[^/]+\.jar", i.filename)]
    assert len(old_jars) == 1, old_jars
    with zipfile.ZipFile(out, "w") as dst:
        for info in src.infolist():
            assert info.filename.startswith(root_old), info.filename
            name = root_new + info.filename[len(root_old):]
            if info is old_jars[0]:
                new = copy_info(info, root_new + "mods/" + jar.name)
                new.date_time = __import__("time").localtime(jar.stat().st_mtime)[:6]
                dst.writestr(new, jar.read_bytes())
                print("replaced", info.filename, "->", new.filename)
                continue
            dst.writestr(copy_info(info, name), src.read(info))


def client(old, out, old_tag, new_tag, file_id):
    src = zipfile.ZipFile(old)
    with zipfile.ZipFile(out, "w") as dst:
        for info in src.infolist():
            data = src.read(info)
            if info.filename == "manifest.json":
                text = data.decode("utf-8")
                text, n1 = re.subn(r'("version": ")' + re.escape(old_tag) + '"', r'\g<1>' + new_tag + '"', text)
                text, n2 = re.subn(r'("projectID": 1508454,\s*"fileID": )\d+', r'\g<1>' + str(file_id), text)
                assert n1 == 1 and n2 == 1, (n1, n2)
                data = text.encode("utf-8")
                print("manifest: version", new_tag, "Challenge Craft file", file_id)
            dst.writestr(copy_info(info, info.filename), data)


if __name__ == "__main__":
    if sys.argv[1] == "server":
        server(*sys.argv[2:7])
    else:
        client(*sys.argv[2:6], int(sys.argv[6]))
