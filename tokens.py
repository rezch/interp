from enum import Enum


class Var(Enum):
    VAR = 0
    INT = 1
    FLOAT = 2
    STR = 3


class StdIO(Enum):
    READ = 0
    WRITE = 1


class Statement(Enum):
    IF = 0
    ELSE = 1
    WHILE = 2
    FOR = 3


class Operators(Enum):
    EQ = 0  # ==
    NE = 1  # !=
    LT = 2  # <
    GT = 3  # >
    LE = 4  # <=
    GE = 5  # >=
    AS = 6  # = (assignment)


class Logical(Enum):
    AND = 0
    OR = 1
    NOT = 2


class Arithmetic(Enum):
    ADD = 0
    SUB = 1
    MULT = 2
    DIV = 3
    INC = 4  # ++var
    DEC = 5  # --var
    ADDEQ = 6  # +=
    SUBEQ = 7  # -=
    MULTEQ = 8  # *=
    DIVEQ = 9  # /=


class Bracket(Enum):
    FUNC_OP = 0  # (
    FUNC_CL = 1  # )
    SPACE_OP = 2  # {
    SPACE_CL = 3  # }


class Endline:
    ...


class Variable:
    def __init__(self, name, is_lexical: bool = False, type_: Var = Var.STR):
        self.name = name
        self.type_ = type_
        self.lexical = is_lexical
        if self.type_ == Var.STR and self.lexical:
            self.name = self.name[1:-1]

    def __str__(self):
        res = f'{self.name}'
        if self.lexical == True:
            res += f' type: {self.type_}'
        else:
            res = 'VAR: ' + res
        return res


# class Token:
#     def __init__(self, type_: Enum, const: bool = False) -> None:
#         self.type = type_
#         self.const = const

