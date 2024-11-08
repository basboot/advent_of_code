import hashlib
import re
from functools import cache

salt = "qzyelonm"
nonce = 0

N_STRETCH = 2017 # 1 = part 1, 2017 = part 2

@cache
def get_hash(salt, nonce):
    digest = salt + str(nonce)
    for i in range(N_STRETCH):
        result = hashlib.md5(digest.encode())
        digest = result.hexdigest()
    return digest

def find_n_consecutive_chars(s, n):
    pattern = r'(.)\1{' + str(n - 1) + '}'
    match = re.search(pattern, s)
    if match:
        return match.group(0)
    return None

keys = []
while len(keys) < 64:
    digest = get_hash(salt, nonce)

    match = find_n_consecutive_chars(digest, 3)
    if match is not None: # found!
        is_key = False

        str_to_find = "".join([match[0]] * 5)
        for i in range(1000):
            if get_hash(salt, nonce + 1 + i).find(str_to_find) > -1:
                keys.append(nonce)
                print(keys)
                break


    nonce += 1

print("Part 2", keys[-1])

# 20316 too low
# 20864






















































# ba2ba3f253c7957774b24c0ad09850f2 from 2773 matched to f70f7c357774c7777792191124f591ca on index 3669
# ab619b808838d86f3f3c777a7e802cad from 3030 matched to f70f7c357774c7777792191124f591ca on index 3669
# f4017b7774af6cbc82e2b10ef1b7e870 from 3168 matched to f70f7c357774c7777792191124f591ca on index 3669
# a7ac1dd8ce4a651725a96f6ba777cb5b from 3399 matched to f70f7c357774c7777792191124f591ca on index 3669
# 8d628f277752fde901181a047fc3ad30 from 3503 matched to f70f7c357774c7777792191124f591ca on index 3669
# 61d9a9514dac62788842a9b6f6c0c6e3 from 3244 matched to 2b466486658e88888ca3899fe8e3622d on index 4221
# 75ea642bfdfd67fcf0f8504259b98884 from 3428 matched to 2b466486658e88888ca3899fe8e3622d on index 4221
# f11c3a5100bed4abedc7e888904580a5 from 3681 matched to 2b466486658e88888ca3899fe8e3622d on index 4221
# 2f65c35337369ee11e888fbc5e9b6432 from 3738 matched to 2b466486658e88888ca3899fe8e3622d on index 4221
# e88841e879dc2edf63e3bdc599a82b77 from 4038 matched to 2b466486658e88888ca3899fe8e3622d on index 4221
# e49028d88bfce888d7581d00205f64fe from 4201 matched to 2b466486658e88888ca3899fe8e3622d on index 4221
# 80576b62a6584bfc966add877e2befff from 3523 matched to 55f7f9c7707fffff6dcd108e974b240b on index 4272
# 0cfff78f12292d686cad9df77e4d7787 from 3818 matched to 55f7f9c7707fffff6dcd108e974b240b on index 4272
# 68564fff5627a19858036d398a0f9b65 from 3837 matched to 55f7f9c7707fffff6dcd108e974b240b on index 4272
# 6c028a01d707b42b9fff333462dd2917 from 3868 matched to 55f7f9c7707fffff6dcd108e974b240b on index 4272
# 374502e04cd81522ce817d75be29fffd from 3982 matched to 55f7f9c7707fffff6dcd108e974b240b on index 4272
# 17f42a193cfffde0d85bce7defaf2a3b from 4029 matched to 55f7f9c7707fffff6dcd108e974b240b on index 4272
# f11c3a5100bed4abedc7e888904580a5 from 3681 matched to 66acc784778b51444e5fd8888814ec3b on index 4550
# 2f65c35337369ee11e888fbc5e9b6432 from 3738 matched to 66acc784778b51444e5fd8888814ec3b on index 4550
# e88841e879dc2edf63e3bdc599a82b77 from 4038 matched to 66acc784778b51444e5fd8888814ec3b on index 4550
# e49028d88bfce888d7581d00205f64fe from 4201 matched to 66acc784778b51444e5fd8888814ec3b on index 4550
# 2b466486658e88888ca3899fe8e3622d from 4221 matched to 66acc784778b51444e5fd8888814ec3b on index 4550
# e86f95e2ee8cf9625c11137015853903 from 4606 matched to 373a11111b3442fa7b6fac3426dd96b7 on index 5587
# eff82af063f630735c48a11161f5bfa1 from 4641 matched to 373a11111b3442fa7b6fac3426dd96b7 on index 5587
# d89b39ea6d082c1111d263ed73b263c4 from 4763 matched to 373a11111b3442fa7b6fac3426dd96b7 on index 5587
# 79e2a9a78b83f3986bc78f0ad4891119 from 5045 matched to 373a11111b3442fa7b6fac3426dd96b7 on index 5587
# c5a84f49175731bc0611119685895e30 from 5283 matched to 373a11111b3442fa7b6fac3426dd96b7 on index 5587
# 13da01f3d9376f525771113fd2c7963a from 5394 matched to 373a11111b3442fa7b6fac3426dd96b7 on index 5587
# b55c3d951ec65b3c22049ce66e167111 from 5436 matched to 373a11111b3442fa7b6fac3426dd96b7 on index 5587
# d21e69e18f111a77338686834f3d1330 from 5499 matched to 373a11111b3442fa7b6fac3426dd96b7 on index 5587
# 92753332f9be64741e44cce62e639a08 from 5174 matched to 9856940d833333dcf5f32ad03019ef90 on index 6141
# 2c8301e6d1ed028d81b7233367f16da2 from 5262 matched to 9856940d833333dcf5f32ad03019ef90 on index 6141
# 304804a7a508f66ecb7f333277476d95 from 5484 matched to 9856940d833333dcf5f32ad03019ef90 on index 6141
# b767e4b20f13303332e87bb8a4873795 from 5643 matched to 9856940d833333dcf5f32ad03019ef90 on index 6141
# 81238af57ea95b04a589b03339384ee4 from 5790 matched to 9856940d833333dcf5f32ad03019ef90 on index 6141
# 85bf5e7afdfb57797e0333bfd43ef047 from 5869 matched to 9856940d833333dcf5f32ad03019ef90 on index 6141
# 6cbb19d10a0f2d7063121fdf555a2731 from 10535 matched to 432379adbad85055555cd6bd6e10ed9f on index 11353
# e6259556bf267ba6a61aede7ec55536e from 10700 matched to 432379adbad85055555cd6bd6e10ed9f on index 11353
# 555bc772277b43024baffa147368dcb0 from 10736 matched to 432379adbad85055555cd6bd6e10ed9f on index 11353
# 38e81023555bb74dbefdc10b9a945f52 from 10802 matched to 432379adbad85055555cd6bd6e10ed9f on index 11353
# 7b8465552c296633d7a6f334115afb77 from 10983 matched to 432379adbad85055555cd6bd6e10ed9f on index 11353
# 482c008fe25f555dcf709d01cacd5b35 from 11049 matched to 432379adbad85055555cd6bd6e10ed9f on index 11353
# c16fedbbfc69ad916b3ca3e7555ff1f9 from 11060 matched to 432379adbad85055555cd6bd6e10ed9f on index 11353
# 1e44a7b4c105196796b55514928fc80b from 11182 matched to 432379adbad85055555cd6bd6e10ed9f on index 11353
# aaf614c2f17c16067f25d555cc629d82 from 11254 matched to 432379adbad85055555cd6bd6e10ed9f on index 11353
# 681a3a1ed480007ba05e0806f86d8147 from 12801 matched to 000006f3e67be32c4066c25e6c6190f6 on index 13574
# 5dcb0cdc539ec76393a000b6b495ae92 from 12817 matched to 000006f3e67be32c4066c25e6c6190f6 on index 13574
# 2e2d3a5e1132b8e470000297c93e143d from 13203 matched to 000006f3e67be32c4066c25e6c6190f6 on index 13574
# fe485035c3dd6b201a000eb309682985 from 13245 matched to 000006f3e67be32c4066c25e6c6190f6 on index 13574
# 1a1b418c74d71f382b0008dd9aad3a36 from 13309 matched to 000006f3e67be32c4066c25e6c6190f6 on index 13574
# 499b1d11b78954000969acbb069f425c from 13348 matched to 000006f3e67be32c4066c25e6c6190f6 on index 13574
# da69335557847112b0226f0196484255 from 16243 matched to b0dfb26055555381610c6ddebcd0ff52 on index 16804
# 57ad95551b07aef766b47a6184c9b3eb from 16405 matched to b0dfb26055555381610c6ddebcd0ff52 on index 16804
# f5550d240270b4645af6525c8fd86375 from 16457 matched to b0dfb26055555381610c6ddebcd0ff52 on index 16804
# 07c48d84f820555bd0fc76a864b74f16 from 16540 matched to b0dfb26055555381610c6ddebcd0ff52 on index 16804
# f2c47156e15b555288d0764f4d7e679a from 16803 matched to b0dfb26055555381610c6ddebcd0ff52 on index 16804
# c55e2840a6a8c267e853e333d6f64d5f from 16456 matched to 60894b42177c9df3d2cb8333337ebd22 on index 17114
# 293de3f8ec420a528c94b8dbd1e6e333 from 16500 matched to 60894b42177c9df3d2cb8333337ebd22 on index 17114
# 7dc3856cc5307bce319e6ad4c333e2f0 from 16729 matched to 60894b42177c9df3d2cb8333337ebd22 on index 17114
# cbb695c569ee9b7d7afd594558c93332 from 16849 matched to 60894b42177c9df3d2cb8333337ebd22 on index 17114
# a84ad96333ff439407b9d9a167ed5601 from 17033 matched to 60894b42177c9df3d2cb8333337ebd22 on index 17114
# c463b4ed6ead13337d4667bad409c087 from 17060 matched to 60894b42177c9df3d2cb8333337ebd22 on index 17114
# 0e94047ae2451107634dbb888fbcd325 from 20035 matched to 493a908b256e851272363af88888b225 on index 21024
# 68639c0888c0c565983d31e69a4ba8c3 from 20316 matched to 493a908b256e851272363af88888b225 on index 21024
# d16e6de3e916bf2888dfb7435a3f2636 from 20409 matched to 493a908b256e851272363af88888b225 on index 21024
# df5b61e03dd476e13975888d9baf9dec from 20779 matched to 493a908b256e851272363af88888b225 on index 21024
# d7a016f1d888e43995f4e294effc01ee from 20822 matched to 493a908b256e851272363af88888b225 on index 21024
# 9867f11f41f1928ed61888382f59c6fd from 20864 matched to 493a908b256e851272363af88888b225 on index 21024
# f1c3c570cf876679a9208885865470fb from 20932 matched to 493a908b256e851272363af88888b225 on index 21024
# ab149d19981c9ebd0a7cb5aaad42c208 from 23876 matched to 44c2d237f61a51baaaaa47488424c962 on index 24710
# eeda6eb74d11e64990e3daaa93ce0bf4 from 23891 matched to 44c2d237f61a51baaaaa47488424c962 on index 24710
# 9d29887c88c1c391e05995baaa7bbbed from 24021 matched to 44c2d237f61a51baaaaa47488424c962 on index 24710
# 7843e2e9ea687940d2742daaa3d907e5 from 24242 matched to 44c2d237f61a51baaaaa47488424c962 on index 24710
# b88f90c610c97adaaabb3afe71da69b5 from 24273 matched to 44c2d237f61a51baaaaa47488424c962 on index 24710
# 96cb9aaae98b3964d751ec3148fc9994 from 24293 matched to 44c2d237f61a51baaaaa47488424c962 on index 24710
# a0e752e7cdbc5c05d3aaad97207a7a33 from 24359 matched to 44c2d237f61a51baaaaa47488424c962 on index 24710
# 96f3aaaee0fcd333404d40b40b180432 from 24476 matched to 44c2d237f61a51baaaaa47488424c962 on index 24710
# 69a47e0a5dcbfaf1f21028e0d9aaab2f from 24492 matched to 44c2d237f61a51baaaaa47488424c962 on index 24710
# dafc1db078deab15aaaa0a1a969b1ef2 from 24607 matched to 44c2d237f61a51baaaaa47488424c962 on index 24710
# aaa56c317b8e6c443f884d4057cce0b2 from 24612 matched to 44c2d237f61a51baaaaa47488424c962 on index 24710
# 9aaa019f7d77a2716ce70969ee6887a4 from 24705 matched to 44c2d237f61a51baaaaa47488424c962 on index 24710