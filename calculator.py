from collections import deque


class Calculator:
    def __init__(self):
        self.var_dic = {}
        self.pm = '+-'
        self.pm_map = {'++': '+', '--': '+', '+-': '-', '-+': '-'}
        self.ops = {'*': 1, '/': 1, '+': 0, '-': 0}
        self.brs = '()'
        self.isfinish = False
        self.err_codes = {'unknown_var': 'Unknown variable',
                          'inv_id': 'Invalid expression', 'inv_assgn': 'Invalid assignment'}
        self.inv_expression = False
        self.help_msg = "The calculator performs addition, subtraction, multiplication and integer division \n"\
                        "of an arbitrary number of integers. " \
                        "It supports both unary and binary minus and plus operators.\n" \
                        "Each operator + or - can be entered several times following each other.\n" \
                        "Examples:     ---4 ++ 5 -8 ---2\n" \
                        "               2*(-4---5)*3+9/4\n"\
                        "It also allows one to use variables, whose names should consist only from letters.\n" \
                        "Examples: aba = 2+15/5, c = -1-3*aba-6, c/aba -56\n"\
                        "Two commands: /help and /exit are supported as well."

    def err_msg(self, code):
        print(self.err_codes[code])

    def perform_op(self, s1, s2, op):
        n1 = int(s1)
        n2 = int(s2)
        if op == '+':
            return n1 + n2
        if op == '-':
            return n1 - n2
        if op == '*':
            return n1 * n2
        if op == '/':
            return n1 // n2

    def command_input(self):
        while not self.isfinish:
            s = input('> ')
            if s.startswith('/'):
                self.execute_command(s)
                continue
            s = s.replace(" ", "")
            if len(s) == 0:
                continue
            self.evaluate(s)
        print('Bye!')

    def execute_command(self, s):
        if s == '/exit':
            self.isfinish = True
        elif s == '/help':
            print(self.help_msg)
        else:
            print('Unknown command')

    def evaluate(self, s):
        if '=' not in s:
            out = self.evaluate_rhs(s)
            if out is None:
                if self.inv_expression:
                    self.err_msg('inv_id')
                return
            print(out)
        else:
            i = s.find('=')
            lhs = s[:i]
            rhs = s[i + 1:]
            if not lhs.isalpha():
                self.err_msg('inv_id')
                return
            out = self.evaluate_rhs(rhs)
            if out is None:
                if self.inv_expression:
                    self.err_msg('inv_assgn')
                return
            self.var_dic[lhs] = out

    # remove repeated signs
    def remove_rep_signs(self, s):
        while True:
            copy_s = s[:]
            for pm_pair, sign in self.pm_map.items():
                s = s.replace(pm_pair, sign)
            if len(s) == len(copy_s):
                return s

    # check that operators are used correctly
    def check_ops(self, expr):
        if expr[-1] in self.ops:  # the last symbol must not be an operator
            self.inv_expression = True
            return False
        count = 0  # check that parenthesis are balanced
        for sym in expr:
            if sym == '(':
                count += 1
            elif sym == ')':
                count -= 1
        if count != 0:
            self.inv_expression = True
            return False
        for i in range(len(expr) - 1):
            ex1, ex2 = expr[i], expr[i + 1]
            if (ex1 in self.ops and ex2 in self.ops) \
                    or (ex1 == '(' and ex2 in self.ops and ex2 not in self.pm)\
                    or (ex2 == ')' and ex1 in self.ops ):  # exclude two operators in a row and "(*", "+)" etc
                self.inv_expression = True
                return False
        return True

    # transform from infix to postfix notation
    def infix_to_postfix(self, expr):
        stack = deque()
        out = []
        for sym in expr:
            if sym.isnumeric():
                out.append(sym)
            else:
                if len(stack) == 0 or stack[-1] == '(':
                    stack.append(sym)
                    continue
                top = stack[-1]
                if sym in self.ops:
                    if self.ops[sym] > self.ops[top]:
                        stack.append(sym)
                    else:
                        while len(stack) != 0 and (stack[-1] != '(' or self.ops[sym] <= self.ops[stack[-1]]):
                            out.append(stack.pop())
                        stack.append(sym)
                if sym == '(':
                    stack.append(sym)
                if sym == ')':
                    while stack[-1] != '(':
                        out.append(stack.pop())
                    stack.pop()
        while len(stack) != 0:
            out.append(stack.pop())
        return out

    # calculate the postfix expression
    def postfix_calc(self, expr):
        stack = deque()
        for sym in expr:
            if sym.isnumeric():
                stack.append(sym)
            else:
                s1, s2 = stack.pop(), stack.pop()
                stack.append(str(self.perform_op(s2, s1, sym)))
        return stack.pop()

    # calculate rhs if it is valid and return it else return None
    def evaluate_rhs(self, s):
        self.inv_expression = False
        s = self.remove_rep_signs('0+' + s)
        s = s.replace('(+', '(0+'); s = s.replace('(-', '(0-')
        # separate operators from numbers and variables
        for op in (list(self.ops) + list(self.brs)):
            s = s.replace(op, '&' + op + '&')
        # s_list = list(filter(lambda sym: sym != '', s.split('&')))
        s_list = [sym for sym in s.split('&') if sym != '']
        # check the expression for repeated operators
        if not self.check_ops(s_list):
            return
        # try to substitute variables
        temp = []
        for op in s_list:
            if not (op.isnumeric() or op in self.ops or op in self.brs):
                if op.isalpha():  # operand is a valid variable name
                    if op in self.var_dic:  # substitute variable
                        if int(self.var_dic[op]) >= 0:
                            temp.append(self.var_dic[op])  # substitute variable
                        else:
                            temp += ['(', '0', '-', self.var_dic[op][1:], ')']  # separate "-" for negative variable
                        continue
                    else:
                        self.err_msg('unknown_var')
                        return
                else:  # not valid variable name
                    self.inv_expression = True
                    return
            else:
                temp.append(op)
        s_list = temp
        # calculate the result using the postfix notation
        return self.postfix_calc(self.infix_to_postfix(s_list))
        

Calculator().command_input()
