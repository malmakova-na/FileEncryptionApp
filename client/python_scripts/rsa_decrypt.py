from rsa_utils import RSA_decrypt, read_private_key
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('enc_key', type=int,
                        help='encryption key')
    parser.add_argument('private_key', type=str,
                        help='path to RSA private key')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    key_private = read_private_key(args.private_key)
    aes_key = RSA_decrypt(args.enc_key, key_private)
    print(aes_key)
