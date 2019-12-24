import re

# input: 171309-643603 (472295)
d4_input = range(171309, 643604)


def match_incremental(psw):
    return all(map(
        lambda i: int(psw[i]) <= (int(psw[i+1]) if i+1 < len(psw) else 10),
        range(len(psw))
    ))


num_ok = 0
for password in d4_input:
    str_password = str(password)
    if re.search(r'(\d)\1+', str_password) and match_incremental(str_password):
        num_ok += 1

print('D4P1 result:', num_ok)


def match_group(psw):
    return any(map(
        lambda i: len(i.group()) == 2, re.finditer(r'(\d)\1+', psw)
    ))


num_ok = 0
for password in d4_input:
    str_password = str(password)
    if match_group(str_password) and match_incremental(str_password):
        num_ok += 1

print('D4P2 result:', num_ok)
