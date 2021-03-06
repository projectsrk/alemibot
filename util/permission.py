from pyrogram import filters

import json

ALLOWED = {}

try:
    with open("data/perms.json") as f:
        ALLOWED = json.load(f)
except FileNotFoundError:
    with open("data/perms.json", "w") as f:
        json.dump({}, f)

def check_allowed(_, __, message):
    if message.from_user is None:
        return False
    if message.from_user.is_self:
        return True
    return str(message.from_user.id) in ALLOWED

is_allowed = filters.create(check_allowed)

def list_allowed():
    return list(int(k) for k in ALLOWED.keys())

def allow(uid, val=True):
    if uid in ALLOWED and ALLOWED[uid] == val:
        return False
    ALLOWED[str(uid)] = val # this is handy when editing manually the file
    serialize()
    return True

def disallow(uid, val=False):
    if str(uid) not in ALLOWED:
        return False
    ALLOWED.pop(str(uid), None)
    serialize()
    return True

def serialize():
    with open("data/perms.json", "w") as f:
        json.dump(ALLOWED, f)
