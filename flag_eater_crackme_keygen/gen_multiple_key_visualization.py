import r2pipe
import string
import tabulate


def is_prime(num):
    for n in range(2, int(num**0.5)+1):
        if num % n == 0:
            return False
    return True


def encode(char: int):
    return char >> 1 if is_prime(char) else char >> 4


def decode(encoded_val: int):
    alphabet = map(ord, string.printable)
    for c in alphabet:
        x = encode(c)
        if x == encoded_val:
            return chr(c)


def get_possible_decoded_vals(encoded_val: int):
    alphabet = map(ord, string.printable)
    for c in alphabet:
        x = encode(c)
        if x == encoded_val:
            yield chr(c)


PWD_LENGTH = 30
r = r2pipe.open('./chall', flags=['-d', '-e', 'dbg.profile=profile.rr2', '-2'])
r.cmd('s 0x555555558060')  # address of encoded input values
encoded_vals = r.cmdj('pxwj')[:30]  # Print heXadecimal 32bit Words into Json
possible_keys = [list(get_possible_decoded_vals(d)) for d in encoded_vals]


max_length = max(len(pos) for pos in possible_keys)
table_data = []
for depth in range(max_length):
    data = []
    for position in range(PWD_LENGTH):
        possible_depth = len(possible_keys[position])-1
        if depth > possible_depth:
            value = ''
        else:
            value = possible_keys[position][depth]

        data.append(value.encode())

    table_data.append(data)

print(tabulate.tabulate(table_data, tablefmt="jira"))
