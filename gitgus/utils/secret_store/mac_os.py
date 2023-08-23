import os
import re


def _decode_hex(s):
    s = eval('"' + re.sub(r"(..)", r"\x\1", s) + '"')  # This looks really dangerous
    if "" in s:
        s = s[: s.index("")]
    return s


def get_macos(service, name):
    service = service.replace("\\", "\\\\").replace('"', '\\"')
    name = name.replace("\\", "\\\\").replace('"', '\\"')

    cmd = " ".join(
        ["/usr/bin/security", " find-generic-password", '-g -s "%s" -a "%s"' % (service, name), "2>&1 >/dev/null"]
    )
    p = os.popen(cmd)
    s = p.read()
    p.close()
    m = re.match(r"password: (?:0x([0-9A-F]+)\s*)?\"(.*)\"$", s)
    if m:
        hex_form, string_form = m.groups()
        if hex_form:
            return _decode_hex(hex_form)
        else:
            return string_form


def set_macos(service, name, value):
    value = value.replace("\\", "\\\\").replace('"', '\\"')
    service = service.replace("\\", "\\\\").replace('"', '\\"')
    name = name.replace("\\", "\\\\").replace('"', '\\"')

    cmd = 'security add-generic-password -U -a "%s" -s "%s" -p "%s"' % (name, service, value)
    p = os.popen(cmd)
    p.read()
    p.close()
