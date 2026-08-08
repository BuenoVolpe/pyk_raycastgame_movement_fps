import re
#=====================================#
from engine.configs.configs import configs
#=====================================#
def highlight_command(text):
    #-------------------------------------#
    tokens = []
    #-------------------------------------#
    pattern = re.compile(
        r'''
        ("[^"]*")                         | # strings
        (\[[^\]]*\])                      | # lists
        (\{[^}]*\})                       | # dicts
        (\btrue\b|\bfalse\b|\bnone\b|\bTrue\b|\bFalse\b|\bNone\b)     | # bool/null
        (\b\d+(\.\d+)?\b)                 | # numbers
        ([a-zA-Z_]\w*(?=\s*=))            | # kwargs
        ([a-zA-Z_]\w*)                    # worlds
        ''',
        re.VERBOSE
    )
    #-------------------------------------#
    last = 0
    #=====================================#
    for match in pattern.finditer(text):
        #-------------------------------------#
        if match.start() > last:
            #-------------------------------------#
            tokens.append(
                (
                    text[last:match.start()],
                    "white"
                )
            )
        #=====================================#
        value = match.group()
        #-------------------------------------#
        if match.group(1):
            color = configs.console.input_colors.strings
        #-------------------------------------#
        elif match.group(2):
            color = configs.console.input_colors.lists
        #-------------------------------------#
        elif match.group(3):
            color = configs.console.input_colors.dicts
        #-------------------------------------#
        elif match.group(4):
            color = configs.console.input_colors.bool
        #-------------------------------------#
        # elif match.group(5):
        #     color = configs.console.input_colors.numbers
        #-------------------------------------#
        # elif match.group(6):
        #     color = configs.console.input_colors.kwargs
        #-------------------------------------#
        else:
            color = configs.console.input_colors.worlds
        #=====================================#
        tokens.append(
            (
                value,
                color
            )
        )
        #-------------------------------------#
        last = match.end()
    #-------------------------------------#
    if last < len(text):
        tokens.append(
            (
                text[last:],
                "white"
            )
        )
    #-------------------------------------#
    return tokens

