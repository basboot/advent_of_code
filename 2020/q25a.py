file1 = open('q25a.txt', 'r')
lines = file1.readlines()

pk_card = int(lines[0].rstrip())
pk_door = int(lines[1].rstrip())

MOD = 20201227
BASE = 7

print(pk_card, pk_door)

# start with 1



def get_loop_size(pk):
    value = 1
    i = 0
    while True:
        i += 1
        value = (value * BASE) % MOD
        if value == pk:
            return i

ls_card = get_loop_size(pk_card)
ls_door = get_loop_size(pk_door)

# Using direct fast method to compute
# (a ^ b) % p.
enc_key = pow(pk_card, ls_door, MOD)

print(enc_key)

