from rsa_utils import RSA_decrypt, read_private_key
from aes_utils import encode_file_AEAD, decode_file_AEAD
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('mode', type=str, choices=["encrypt", "decrypt"],
                        help='mode: encrypt or decrypt')
    parser.add_argument('enc_key', type=int,
                        help='AES encryption key')
    parser.add_argument('private_key', type=str,
                        help='path to RSA private key')
    parser.add_argument('path', type=str,
                        help='path to file')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    key_private = read_private_key(args.private_key)
    aes_key = RSA_decrypt(args.enc_key, key_private)
    # print(aes_key)
    if args.mode == "encrypt":
        encode_file_AEAD(args.path, args.path + ".encrypt", aes_key)
    elif args.mode == "decrypt":
        assert args.path.split(".")[-1] == "encrypt"
        decode_path = ".".join(args.path.split(".")[:-1])
        decode_file_AEAD(args.path, decode_path, aes_key)
