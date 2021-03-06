import re
from . import batchify

def is_me(message):
    return message.from_user is not None \
    and message.from_user.is_self \
    and message.via_bot is None # can't edit messages from inline bots

def get_text(message):
    if message.text is not None:
        return message.text
    else:
        if message.caption is not None:
            return message.caption
        else:
            return ""

def get_text_dict(message):
    if "text" in message:
        return message["text"]
    elif "caption" in message:
        return message["caption"]
    else:
        return {"markdown": "", "raw": ""}

def parse_sys_dict(msg):
    events = []
    if "new_chat_members" in msg:
        events.append("new chat members")
    if "left_chat_member" in msg:
        events.append("member left")
    if "new_chat_title" in msg:
        events.append("chat title changed")
    if "new_chat_photo" in msg:
        events.append("chat photo changed")
    if "delete_chat_photo" in msg:
        events.append("chat photo deleted")
    if "group_chat_created" in msg:
        events.append("group chat created")
    if "supergroup_chat_created" in msg:
        events.append("supergroup created")
    if "channel_chat_created" in msg:
        events.append("channel created")
    if "migrate_to_chat_id" in msg:
        events.append("migrate to chat id")
    if "migrate_from_chat_id" in msg:
        events.append("migrate from chat id")
    if "pinned_message" in msg:
        events.append("pinned msg")
    if "game_score" in msg:
        events.append("game score")
    return "SYS[ " + " | ".join(events) + " ]"

async def edit_or_reply(message, text, *args, **kwargs):
    if is_me(message) and len(message.text.markdown + text) < 4090: 
        return await message.edit(message.text.markdown + "\n" + text, *args, **kwargs)
    else:
        ret = None
        for m in batchify(text, 4090):
            ret = await message.reply(m, *args, **kwargs)
        return ret

def tokenize_json(text):
    res = re.subn(
        r'("[^\"]+"|[0-9.\-]+)',
        '``\g<1>``', text)
    if res[1] * 2 > 100: # we generate 2 entities for every replace we do (kinda)
        return tokenize_lines(text) # try to tokenize per line at least
    return "`" + res[0] + "`"

def tokenize_lines(text, mode='markdown'):
    BEFORE = "```" if mode == "markdown" else "<code>"
    AFTER = "```" if mode == "markdown" else "</code>"
    res =  re.subn(r'(.+)', BEFORE+'\g<1>'+AFTER, text)
    if res[1] * 2 > 100: # we generate 2 entities for every replace we do (kinda)
        return BEFORE + text + AFTER
    return res[0]
