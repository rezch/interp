tokens = ['+', '-', '*', '/', '(', ')']

priority = {
    '(': 0,
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
}


def parse(data: str) -> list:
    result = []
    buffer = ''
    data = data.replace(' ', '')
    for sym in data:
        if sym not in tokens:
            buffer += sym
        else:
            if buffer != '':
                result += [buffer]
            result += [sym]
            buffer = ''

    if buffer != '':
        result += [buffer]
    return result


def converter(data: str) -> list:
    data = parse(data)
    buffer = []
    result = []
    for token in data:
        if token == '(':
            buffer = [token] + buffer
            continue

        elif token not in tokens:
            result += [token]
            continue

        if not buffer:
            buffer = [token]
        elif token == ')':
            while True:
                temp = buffer[0]
                buffer = buffer[1:]
                if temp == '(':
                    break
                result += [temp]
        elif priority[buffer[0]] < priority[token]:
            buffer = [token] + buffer
        else:
            while buffer:
                temp = buffer[0]
                result += [temp]
                buffer = buffer[1:]
                if priority[temp] == priority[token]:
                    break
            buffer = [token] + buffer

    while buffer:
        temp = buffer[0]
        result += [temp]
        buffer = buffer[1:]

    return result


if __name__ == "__main__":
    print(converter('(a + b - c * d) - (d + c) / b'))
    # ['a', 'b', '+', 'c', 'd', '*', '+', 'd', 'c', '+', 'b', '*', '-']
