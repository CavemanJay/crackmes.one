import r2pipe
import string


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
print(encoded_vals)
key = "".join(decode(e) for e in encoded_vals)
print(key)
