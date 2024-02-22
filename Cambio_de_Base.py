nums_bases = '0123456789ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'

def hexadecimal(num_base10, num_base):

    num = ''
    residuo = num_base10%num_base

    if residuo != num_base10:
        num_entero = num_base10//num_base
        num += hexadecimal(num_entero,num_base) + nums_bases[residuo]
        return num
    else:
        return nums_bases[residuo]

while True:
    num_base = 100
    while num_base > len(nums_bases):
        num_base = int(input('Nueva base: '))
    num_base10 = int(input('Número base 10: '))
    print(f'Número base {num_base}: {hexadecimal(num_base10, num_base)}')
    print()
