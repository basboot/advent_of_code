from collections import Counter
import hashlib

door_id = "ffykfhsq"
nonce = 0
password = ""

while len(password) < 8:
    str_to_hash = door_id + str(nonce)
    result = hashlib.md5(str_to_hash.encode())
    digest = result.hexdigest()
    if digest[0:5] == "00000":
        password += digest[5]
        print(">", password)
    nonce += 1

print("Part 1", password)

nonce = 0
password = ['-'] * 8
valid_positions = set([str(x) for x in range(8)])

print(valid_positions)

n_found = 0
while n_found < 8:
    str_to_hash = door_id + str(nonce)
    result = hashlib.md5(str_to_hash.encode())
    digest = result.hexdigest()
    if digest[0:5] == "00000":
        if digest[5] in valid_positions:
            # print(f"option to place {digest[6]} at pos {digest[5]}, for {nonce}")
            if password[int(digest[5])] == "-":
                password[int(digest[5])] = digest[6]
                print(">", password)
                n_found += 1
    nonce += 1

print("Part 2", "".join(password))
