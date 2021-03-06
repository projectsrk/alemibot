import shutil

def split_for_window(text, offset=0):
    width = shutil.get_terminal_size((100, 100))[0] # pass a fallback, 1st arg is width
    width -= width//10 # pad by 1/10th
    text = text.replace("\n", "\n" + " "*offset)
    buf = text.split(" ")
    out = ""
    line = ""
    cap = width - offset
    for w in buf:
        if len(line + " " + w) > cap:
            if len(w) > cap: # word wouldn't fit anyway
                line += " " + w
                while len(line) > cap:
                    out += line[:cap] + "\n" + " "*offset
                    line= line[cap:]
                continue
            else:
                out += line + "\n" + " "*offset
                line = ""
        line += w + " "
    out += line
    return out
