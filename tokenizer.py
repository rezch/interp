from tokens import *


class TokenizerException(Exception):
    def __init__(self, message=None):
        self.message = message
        if message is None:
            self.message = ''

    def __str__(self):
        return f'Tokenizer error: {self.message}'


class Tokenizer:
    VARS = {
        'var': 0,
        'int': 1,
        'float': 2,
        'str': 3,
    }

    STDIO = {
        'read': 0,
        'write': 1,
    }

    STATEMENT = {
        'if': 0,
        'else': 1,
        'while': 2,
        'for': 3,
    }

    OPERATORS = {
        '!': 0,
        '<': 2,
        '>': 3,
        '=': 6,
    }

    LOGICAL = {
        'and': 0,
        'or': 1,
        'not': 2,
    }

    ARITHMETIC = {
        '+': 0,
        '-': 1,
        '*': 2,
        '/': 3
    }

    OPERATORS_MODULE = {
        '==': 0,
        '!=': 1,
        '<=': 4,
        '>=': 5,
    }

    ARITHMETIC_MODULE = {
        '++': 4,
        '--': 5,
        '+=': 6,
        '-=': 7,
        '*=': 8,
        '/=': 9,
    }

    BRACKETS = {
        '(': 0,
        ')': 1,
        '{': 2,
        '}': 3,
    }

    STRING_QUOTES = [
        '"', "'"
    ]

    ENDLINE = [';']

    ALL_TOKENS = [
        VARS, STDIO, STATEMENT, OPERATORS, LOGICAL, ARITHMETIC
    ]

    ALL_TOKENS_DICT = {
        0: Var,
        1: StdIO,
        2: Statement,
        3: Operators,
        4: Logical,
        5: Arithmetic,
    }

    ALL_TOKENS_VALUES = [
        *list(VARS.keys()), *list(STDIO.keys()), *list(STATEMENT.keys()), *list(OPERATORS.keys()), *list(LOGICAL.keys()), *list(ARITHMETIC.keys())
    ]

    MODULE_TOKENS = [
        *list(OPERATORS.keys()), *list(ARITHMETIC.keys())
    ]

    def __init__(self, raw_tokens: list, parse: bool = False) -> None:
        self.tokens = []
        self.raw_tokens = raw_tokens
        self.size = len(raw_tokens)
        if parse:
            self.parse()

    def parse(self, index: int = 0, token: str = None) -> None:
        if index == self.size:
            self.__prepare_token(token)
            return

        if token is not None:
            if self.raw_tokens[index] not in Tokenizer.MODULE_TOKENS:
                self.__prepare_token(token)
            else:
                self.__prepare_module_token(token, self.raw_tokens[index])
                self.parse(index + 1, None)
                return

        if self.raw_tokens[index] in Tokenizer.VARS.keys():
            self.tokens.append(Var(Tokenizer.VARS[self.raw_tokens[index]]))

        elif self.raw_tokens[index] in Tokenizer.STDIO.keys():
            self.tokens.append(StdIO(Tokenizer.STDIO[self.raw_tokens[index]]))

        elif self.raw_tokens[index] in Tokenizer.STATEMENT.keys():
            self.tokens.append(Statement(Tokenizer.STATEMENT[self.raw_tokens[index]]))

        elif self.raw_tokens[index] in Tokenizer.LOGICAL.keys():
            self.tokens.append(Logical(Tokenizer.LOGICAL[self.raw_tokens[index]]))

        elif self.raw_tokens[index] in Tokenizer.MODULE_TOKENS:
            self.parse(index + 1, self.raw_tokens[index])
            return

        elif self.raw_tokens[index] in Tokenizer.ENDLINE:
            self.tokens.append(Endline())

        elif self.raw_tokens[index] not in Tokenizer.ALL_TOKENS_VALUES:
            self.__prepare_vars(self.raw_tokens[index])

        self.parse(index + 1, None)

    def __prepare_vars(self, raw_token: str) -> None:
        if raw_token in Tokenizer.BRACKETS:
            self.tokens.append(Bracket(Tokenizer.BRACKETS[raw_token]))
            return

        if raw_token[0] in Tokenizer.STRING_QUOTES:  # lexical string
            self.tokens.append(
                Variable(raw_token, is_lexical=True, type_=Var.STR)
            )
            return

        if raw_token[0].isdigit():  # lexical number
            type_ = int
            if '.' in raw_token:
                type_ = float
            try:
                self.tokens.append(
                    Variable(type_(raw_token), is_lexical=True, type_=Var.INT)
                )
            except (ValueError, TypeError):
                raise TokenizerException(f'Bad token: {type_.__name__} error: {raw_token}')
            return

        # variable name
        self.tokens.append(Variable(raw_token))

    def __prepare_module_token(self, lhs: str, rhs: str) -> None:
        raw_token = lhs + rhs

        for key, value in Tokenizer.OPERATORS_MODULE.items():
            if key == raw_token:
                self.tokens.append(Operators(value))
                return

        for key, value in Tokenizer.ARITHMETIC_MODULE.items():
            if key == raw_token:
                self.tokens.append(Arithmetic(value))
                return

        raise TokenizerException(f'Bad token {raw_token}')

    def __prepare_token(self, raw_token: str) -> None:
        for i, TOKEN in enumerate(Tokenizer.ALL_TOKENS):
            if raw_token in TOKEN.keys():
                type_ = Tokenizer.ALL_TOKENS_DICT[i]
                token = TOKEN[raw_token]

                if type_ == 3 and token == 0:  # !
                    raise TokenizerException(f'Bad token {raw_token}')

                self.tokens.append(type_(token))
                return

