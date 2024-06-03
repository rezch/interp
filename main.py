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
        self.index = 0
        self.stack = list()
        self.data = dict()  # variables
        self.parenthesis = None

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
        self.__run()
        value = self.stack.pop()
        if type(var) == Variable:
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
        else:
            if op == Arithmetic.ADD:
                self.stack.append(var + value)
            elif op == Arithmetic.SUB:
                self.stack.append(var - value)
            elif op == Arithmetic.MULT:
                self.stack.append(var * value)
            elif op == Arithmetic.DIV:
                self.stack.append(var / value)
            else:
                raise SyntaxError

    def __prepare_parenthesis(self) -> bool:
        last = self.parenthesis
        if self.tokens[self.index] == Bracket.FUNC_OP:
            self.parenthesis = self.tokens[self.index]
            self.index += 1
            self.run()
            return False
        elif self.tokens[self.index] == Bracket.SPACE_OP:
            self.parenthesis = self.tokens[self.index]
            self.index += 1
            self.run()
            return False
        elif self.tokens[self.index] == Bracket.FUNC_CL:
            if last != Bracket.FUNC_OP:
                raise SyntaxError
            self.parenthesis = last
            return True
        elif self.tokens[self.index] == Bracket.SPACE_CL:
            if last != Bracket.SPACE_CL:
                raise SyntaxError
            self.parenthesis = last
            return True

    def run(self):
        while self.index < self.size:
            self.__run()
            self.index += 1

    def __run(self) -> None:
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
            self.__run()
            self.data[name.name] = self.stack.pop()

        elif type(token) == StdIO:
            print('stdio', self.stack)

        elif type(token) == Statement:
            ...
        elif type(token) == Operators:
            if token == Operators.AS:
                lhs = self.stack.pop()
                self.index += 1
                self.__run()
                rhs = self.stack.pop()
                self.data[lhs.name] = rhs
                return
            pass
        elif type(token) == Logical:
            ...
        elif type(token) == Arithmetic:
            self.__process_arithmetic()
            return
        elif type(token) == Bracket:
            if self.__prepare_parenthesis():
                return
        elif type(token) == Endline:
            return
        elif type(token) == Variable:
            if token.lexical == True:
                self.stack.append(token.name)
            else:
                if token.name not in self.data.keys():
                    print(token, self.data.keys(), '--------------')
                    raise NameError
                self.stack.append(token)

        self.index += 1
        self.__run()


if __name__ == '__main__':
    lexer = Lexer(s, parse=True)
    tokenizer = Tokenizer(lexer.raw_tokens, parse=True)
    interp = Interpreter(tokenizer.tokens)
    interp.run()
    print('--------')
    print(interp.data)

