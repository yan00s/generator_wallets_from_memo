import json
from bip32utils import BIP32Key, BIP32_HARDEN
from mnemonic import Mnemonic
from eth_keys import keys
import os

# from ecdsa.ecdsa import int_to_string, string_to_int
# print(f"seed: {seed_hex}") # BIP39 Seed
# print(f"xprv: {xprv}") # BIP32 Root Key
# xprv = bip32_entrp.ExtendedKey()
# seed_hex = seed.hex()

def create_wallet_eth():
    mnemon = Mnemonic('english')
    mnemonic_phase = mnemon.generate(160)
    seed = Mnemonic.to_seed(mnemonic_phase)
    bip32_entrp = BIP32Key.fromEntropy(seed)

    bip32_child_key_obj = bip32_entrp.ChildKey(
            44 + BIP32_HARDEN
        ).ChildKey(
            60 + BIP32_HARDEN
        ).ChildKey(
            0 + BIP32_HARDEN
        ).ChildKey(0).ChildKey(0) # m/44'/60'/0'/0

    public_key = '0x' + bip32_child_key_obj.PublicKey().hex()

    priv_key = keys.PrivateKey(bip32_child_key_obj.PrivateKey())
    pub_key = priv_key.public_key
    # pub_key.to_checksum_address()
    address = pub_key.to_checksum_address()

    data = {'mnemonic':mnemonic_phase,
            'address_eth': address,
            'public_key_eth': public_key,
            'private_key_eth': str(priv_key)}
    return data


t = 'generation wallet with eth address\n'
print(t)
result = []
count_wallet = int(input('count wallet: '))
if 'result.json' in os.listdir():
    g = str(input('are you sure want continue? this will delete the file (- if no, enter if yes): '))
    if '-' in g:
        exit(0)
for _ in range(count_wallet):
    result.append(create_wallet_eth())
    print(f'generation wallet {_}')
print('complete')
with open('result.json', 'w', encoding='UTF-8') as f:
    json.dump(result, f, indent=4)
input()