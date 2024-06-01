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
y += ' = ';
y = y + 'x';
'''


class Interpreter:
    def __init__(self, tokens: []) -> None:
        self.tokens = tokens
        self.size = len(tokens)
        self.index = 0
        self.stack = []
        self.data = {}  # variables

    def terminate(self) -> None:
        ...

    def __process_arithmetic(self):
        var = self.stack.pop()
        op = self.tokens[self.index]

        if op == Arithmetic.INC:
            self.data[var.name] += 1
            return
        elif op == Arithmetic.DEC:
            self.data[var.name] -= 1
            return

        self.index += 1
        self.run()
        value = self.stack.pop()
        if op == Arithmetic.ADD:
            self.stack.append(self.data[var.name] + value)
        elif op == Arithmetic.SUB:
            self.stack.append(self.data[var.name] - value)
        elif op == Arithmetic.MULT:
            self.stack.append(self.data[var.name] * value)
        elif op == Arithmetic.DIV:
            self.stack.append(self.data[var.name] / value)
        elif op == Arithmetic.ADDEQ:
            self.data[var.name] += value
        elif op == Arithmetic.SUBEQ:
            self.data[var.name] -= value
        elif op == Arithmetic.MULTEQ:
            self.data[var.name] *= value
        elif op == Arithmetic.DIVEQ:
            self.data[var.name] /= value

    def run(self) -> None:
        if self.index >= self.size:
            self.terminate()
            return

        token = self.tokens[self.index]

        if type(token) == Var:
            self.index += 1
            name = self.tokens[self.index]
            if type(name) != Variable or name.lexical or name.name in self.data:
                raise ValueError
            self.index += 2
            self.run()
            self.data[name.name] = self.stack.pop()

        elif type(token) == StdIO:
            print('stdio', token)

        elif type(token) == Statement:
            ...
        elif type(token) == Operators:
            if token == Operators.AS:
                lhs = self.stack.pop()
                self.index += 1
                self.run()
                rhs = self.stack.pop()
                self.data[lhs.name] = rhs
        elif type(token) == Logical:
            ...
        elif type(token) == Arithmetic:
            self.__process_arithmetic()
        elif type(token) == Bracket:
            ...
        elif type(token) == Endline:
            return
        elif type(token) == Variable:
            if token.lexical == True:
                self.stack.append(token.name)
            else:
                if token.name in self.data:
                    self.stack.append(token)
                else:
                    self.index += 1
                    self.data[token.name] = self.stack.pop()
                    return

        self.index += 1
        self.run()
        # self.stack_revert(stack_snapshot)


if __name__ == '__main__':
    lexer = Lexer(s, parse=True)
    tokenizer = Tokenizer(lexer.raw_tokens, parse=True)
    interp = Interpreter(tokenizer.tokens)
    interp.run()
    print('--------')
    print(interp.data)

