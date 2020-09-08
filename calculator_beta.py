import string
digits = string.digits
letters = string.ascii_letters
pm = '+-'

# var_dic = {'a': '5', 'xx': '2'}
var_dic = {}
unk_var = False
invalid = False

help_msg = '''The program calculates additions and subtractions of an arbitrary number 
of operands.It supports both unary and binary minus operators. 
Each operator + or - can be entered several times following each other.
It also allow
Example:     ---4 ++ 5 -8 ---2'''

def execute_command(s):
    global isfinish
    if s == '/exit':
        isfinish = True
        return
    if s == '/help':
        print(help_msg)
        return
    else:
        print('Unknown command')

def substitute_var(s):  # substitute values of all variables
    global unk_var, invalid
    unk_var = False
    invalid = False
    output = ''
    ispm = True
    isletter = False
    var = ''

    for i, sym in enumerate(s):
        if ispm:  # previous symbol is sign
            if sym in letters:  # current symbol is letter
                var = sym  # start to record new variable
                isletter = True
            else:  # current symbol is not letter
                output += sym
            if sym not in pm:
                ispm = False
        elif isletter:  # previous symbol is letter
            if sym in letters:  # current symbol is letter
                var += sym  # continue to record variable
            elif sym in pm:  # current symbol is sign
                if var in var_dic:
                    output += var_dic[var] + sym  # substitute variable
                    var =''
                    ispm = True
                    isletter = False
                else:
                    unk_var = True  # unknown variable
                    return None
            else:  # current symbol is neither letter nor sign
                invalid = True  # invalid identifier
                print('Invalid identifier')
                return None
        else:  # previous symbol is neither letter nor sign
            if sym in letters:  # current symbol is letter
                invalid = True  # invalid identifier
                print('Invalid identifier')
                return None
            output += sym
            if sym in pm:  # current symbol is sign
                ispm = True

    if len(var) != 0:  # potential last unrecorded variable
        if var in var_dic:
            output += var_dic[var]  # substitute variable
        else:
            unk_var = True  # unknown variable
            print('Unknown variable')
            return None
    return output


def validate_rhs(s):
    s_var = substitute_var(s)
    if s_var is None:
        return None
    # if invalid:
    #     print('Invalid identifier')
    #     return False
    # if unk_var:
    #     print('Unknown variable')
    #     return False
    for sym in s_var:
        if sym not in pm and sym not in digits:
            print('Invalid expression')
            return None
    if s_var[-1] not in digits:
        print('Invalid expression')
        return None
    return str(sum(process(s_var)))


def validate_lhs(s):
    for sym in s:
        if sym not in letters:
            print('Invalid identifier')
            return False
    return True


def my_evaluate(s):
    if '=' not in s:
        out =  validate_rhs(s)
        if out is None:
            return
        print(out)
    else:
        i = s.find('=')
        lhs = s[:i]
        rhs = s[i+1:]
        if not validate_lhs(lhs):
            return
        out = validate_rhs(rhs)
        if out is None:
            return
        var_dic[lhs] = out


def process(s):
    output = []
    csign = '+'
    isdigit = False
    for i in range(len(s)):
        if not isdigit:  # previous input symbol is sign
            if s[i] in pm: # current input symbol is sign
                csign = '+' if (csign == '+' and s[i] == '+') or (csign == '-' and s[i] == '-') else '-'
            else: # current input symbol is digit
                isdigit = True
                cdigit = csign + s[i]
        else:   # previous input symbol is digit
            if s[i] in pm: # current input symbol is sign
                csign = s[i]
                isdigit = False
                output.append(int(cdigit))
            else: # current input symbol is digit
                cdigit += s[i]

    output.append(int(cdigit))
    return output



isfinish = False
while not isfinish:
    s = input()
    if s.startswith('/'):
        execute_command(s)
        continue
    s = s.replace(" ","")
    if len(s) == 0:
        continue
    my_evaluate(s)

print('Bye!')