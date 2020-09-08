

def remove_rep_signs(s):
    pm_map = {'++': '+', '--': '+', '+-': '-', '-+': '-'}
    while True:
        # copy_s = copy.deepcopy(s)
        copy_s = s[:]
        for pm_pair, sign in pm_map.items():
            s = s.replace(pm_pair, sign)
        if len(s) == len(copy_s):
            return s



s = '5+++7-6---+5---1'
w = remove_rep_signs(s)
print(w)