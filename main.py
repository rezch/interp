from lexer import Lexer
from tokens import *
from tokenizer import Tokenizer


s1 = '''
var name = "test";
var code = 124;

if(name == "test" and code!=123) { // comment no. 1
    // some comment
    write("Done"); // another comment
    code=code + "aaa";
}
else {
    write("!");
    ++code;
}
'''


s = '''
var x = 14;
x += 2;
x + 3;
x /= 2;

var y = "name";
y += '!';
x;
x;
y = y + '321';
x;
y;
y = 3 + x / 2;


'''


class Interpreter:
    def __init__(self, tokens: []) -> None:
        self.tokens = tokens
        self.size = len(tokens)
        self.data = dict()  # variables

    priorities = {
        Arithmetic.INC: 0,
        Arithmetic.DEC: 0,
        Logical.OR: 1,
        Logical.AND: 2,
        Logical.NOT: 3,
        Operators.EQ: 4,
        Operators.NE: 4,
        Operators.LT: 4,
        Operators.GT: 4,
        Operators.LE: 4,
        Operators.GE: 4,
        Arithmetic.ADD: 5,
        Arithmetic.SUB: 5,
        Arithmetic.MULT: 6,
        Arithmetic.DIV: 6,
        Arithmetic.MOD: 7,
        # functions
    }

    brackets = {
        Bracket.FUNC_OP: 10,
        Bracket.FUNC_CL: -10,
    }

    @staticmethod
    def process_line(line: []):
        priority = 0
        stack = []
        buffer = []
        adder = 0
        for token in line:
            if type(token) == Variable:
                stack.append(token)
                continue
            if type(token) == Bracket:
                adder += Interpreter.brackets[token]
                continue
            current_priority = Interpreter.priorities[token] + adder
            if current_priority > priority:
                priority = current_priority
                buffer.append(token)
            else:
                stack += buffer[::-1]
                buffer = [token]

        stack += buffer[::-1]
        return stack

    def run(self):
        line = []
        for token in self.tokens:
            if token == Endline:
                self.__process_line(line)
                line = []
            else:
                line.append(token)


if __name__ == '__main__':
    # lexer = Lexer(s, parse=True)
    # tokenizer = Tokenizer(lexer.raw_tokens, parse=True)
    # interp = Interpreter(tokenizer.tokens)
    # interp.run()
    # print('--------')
    # print(interp.data)

    # line: 4 + x * (2 - x) - 3
    l = [
        Variable(4, is_lexical=True, type_=Var.INT),
        Arithmetic.ADD,
        Variable('x'),
        Arithmetic.MULT,
        Bracket.FUNC_OP,
        Variable(2, is_lexical=True, type_=Var.INT),
        Arithmetic.SUB,
        Variable('x'),
        Bracket.FUNC_CL,
        Arithmetic.SUB,
        Variable(3, is_lexical=True, type_=Var.INT),
    ]
    for t in Interpreter.process_line(l):
        print(t)

