import sys
import re

def lex(characters, token_exprs):
    pos = 0
    tokens = []
    while pos < len(characters):
        match = None
        for token_expr in token_exprs:
            pattern, tag = token_expr
            regex = re.compile(pattern)
            match = regex.match(characters, pos)
            if match:
                text = match.group(0)
                if tag: # проверяем толькоесли есть тег (отбрасываем пробелы и комментарии)
                    token = (text, tag)
                    tokens.append(token)
                break
        if not match: # Ошибка: "Неизвестный символ"
            sys.stderr.write('Неизвестный символ: %s\n' % characters[pos])
            sys.exit(1)
        else:
            pos = match.end(0)
    return tokens
