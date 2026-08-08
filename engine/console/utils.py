import shlex

def parse_args(text):
    args = []
    kwargs = {}

    for token in shlex.split(text):
        if "=" in token:
            k, v = token.split("=", 1)
            kwargs[k] = parse_value(v)
        else:
            args.append(parse_value(token))

    return args, kwargs


def parse_value(value):
    if value.lower() == "true":
        return True

    if value.lower() == "false":
        return False

    if value.lower() == "none":
        return None

    try:
        return int(value)
    except:
        pass

    try:
        return float(value)
    except:
        pass

    return value

def split_command(text: str, do_strip=True):
    if ":" in text:
        cmd, args = text.split(":", 1)
    else:
        cmd = text
        args = ""
    if do_strip:
        return cmd.strip(), args.strip()
    else:
        return cmd, args

