from rsa_utils import get_RSA_keys, write_keys
import argparse
import os

def parse_args():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('output', type=str,
                        help='path to folder where generate keys')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    os.makedirs(args.output, exist_ok=True)
    key_e, key_d = get_RSA_keys(1024)
    write_keys(args.output, key_e, key_d)
