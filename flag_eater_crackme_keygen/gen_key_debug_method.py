from typing import List
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


def update_input(stdin: List[str]):
    with open('input.txt', 'w') as f:
        f.write("".join(stdin))


PWD_LENGTH = 30
stdin = ['A']*PWD_LENGTH
for i in range(PWD_LENGTH):
    r = r2pipe.open(
        "./chall", flags=['-d', '-e', 'dbg.profile=profile.rr2', '-2'])
    r.cmd('aa; db 0x55555555522d;'+'dc;'*(i+1))
    registers = r.cmdJ('drj')
    expected_value: int = registers.rax
    val: int = registers.rdx
    stdin[i] = decode(expected_value)
    update_input(stdin)

    print("".join(stdin))
