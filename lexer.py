from itertools import chain


class Lexer:
    OPERATORS = {
        'COMPARISON': ('>', '<', '=', '!'),
        'ASSIGNMENT': ('=', ),
        'LOGICAL': ('and', 'or', 'not'),
        'PARENTHESIS': ('(', ')', '{', '}', '<', '>'),
        'ARITHMETIC': ('+', '-', '*', '/')
    }

    FUNCTIONS = {
        'STDIO': ('read', 'write'),
        'STATEMENTS': ('if', 'else'),
        'LOOPS': ('while', 'for'),
        'VARS': ('var', ),
        'TYPES': ('int', 'float', 'str')
    }

    ENDLINE = ';'

    TOKEN_ENDS = (' ', ENDLINE) + \
        OPERATORS['COMPARISON'] + \
        OPERATORS['ASSIGNMENT'] + \
        OPERATORS['PARENTHESIS'] + \
        OPERATORS['ARITHMETIC']

    ALL_TOKENS = list(chain(*OPERATORS.values())) + list(chain(*FUNCTIONS.values()))

    WORD_ENDS = (')', '}', '>') + (ENDLINE, )

    EMPTY_TOKENS = (' ', ENDLINE, '\n')

    LINE_ENDS = ('\n', )

    STRING_QUOTES = [
        '"', "'"
    ]

    def __init__(self, source: str, parse=False):
        self.source = source
        self.size = len(source)
        self.raw_tokens = []
        if parse:
            self.parse()
            print(self.raw_tokens)

    def parse(self) -> None:
        self.__parse(0, '')

    def __parse(self, index: int, word: str) -> None:
        if index >= self.size:
            self.__to_raw_token(word)
            return

        if word == '/' and self.source[index] == '/':  # comment
            while index < self.size and self.source[index] not in Lexer.LINE_ENDS:
                index += 1
            word = ''

        if self.source[index] in Lexer.STRING_QUOTES:
            self.__to_raw_token(word)
            word = ''
            index = self.__parse_string(index)

        if self.source[index] in self.TOKEN_ENDS:
            self.__to_raw_token(word)
            if self.source[index] == Lexer.ENDLINE:
                self.raw_tokens.append(';')
            word = ''

        elif self.source[index] in Lexer.WORD_ENDS:
            self.__to_raw_token(word)
            self.raw_tokens.append(self.source[index])
            word = ''

        elif word in Lexer.ALL_TOKENS:
            self.__to_raw_token(word)
            word = ''

        self.__parse(index + 1, word + self.source[index])

    def __to_raw_token(self, word: str) -> None:
        word = word.strip().replace('\n', '').replace(';', '').replace(',', '')
        if word == '':
            return
        self.raw_tokens.append(word)

    def __parse_string(self, index: int) -> int:
        string = ''
        quote = self.source[index]
        index += 1
        while index < self.size and self.source[index] != quote:
            string += self.source[index]
            index += 1
        self.raw_tokens.append(quote + string + quote)
        return index + 1

