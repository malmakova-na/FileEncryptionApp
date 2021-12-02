import random
import math
import time
import base64
import os
import re
import sys
import argparse
from Crypto.Util import asn1

def MR_testing(n, k):
    if n < 2:
        return False
    #Представляем n-1 в виде 2^r*d, где d - нечетно
    d = n - 1
    r = 0
    while not (d & 1):
        r += 1
        d >>= 1
    for _ in range(k):
        a = random.randint(2, n-2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == 1:
                return False
            if x == n - 1:
                break
        else:
            return False
    return True

def is_prime(number):
    if number < 10:
        return number in {2, 3, 5, 7}

    if not (number & 1):
        return False

    bitsize = number.bit_length()

    #Минимальное кол-во тестов Миллера-Рабина для проверки того, что number - простое с точностью до 2^(-100)
    #Согласно NIST FIPS 186-4, Appendix C, Table C.3
    #https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.186-4.pdf С.3
    if bitsize >= 1536:
        k = 3
    elif bitsize >= 1024:
        k = 4
    elif bitsize >= 512:
        k = 7
    else:
        k = 10
    return MR_testing(number, k+1)

def extended_gcd(a, b):
    #возвращает (r, i, j), где r = НОД(a,b) = i*a + j*b
    x = 0
    y = 1
    lx = 1
    ly = 0
    oa = a  # Запоминание оригинальных a,b для удаления негативных значений
    ob = b
    while b != 0:
        q = a // b
        (a, b) = (b, a % b)
        (x, lx) = ((lx - (q * x)), x)
        (y, ly) = ((ly - (q * y)), y)
    if lx < 0:
        lx += ob
    if ly < 0:
        ly += oa
    return a, lx, ly

def inverse(x, n):
    dev, inv, _ = extended_gcd(x, n)
    if dev != 1:
        raise ValueError('{} и {} не взаимно простые, делитель = {}'.format(x, n, dev))
    return inv

def get_prime(nbits):
    while True:
        int_ = random.randint(1 << (nbits - 1), (1 << nbits) - 1)
        if is_prime(int_):
            return int_

def calculate_e_d(p, q, e = 65537):
    phi_n = (p-1)*(q-1)

    d = inverse(e, phi_n)

    if (e * d) % phi_n != 1:
        raise ValueError('d {} не мультипликативно обратное к числу e {} по модулю phi_n {}'.format(d, e, phi_n))

    return e, d

def find_p_q(nbits):
    total_bits = nbits * 2

    shift = nbits//16
    pbits = nbits + shift
    qbits = nbits - shift

    p = get_prime(pbits)
    q = get_prime(qbits)

    def is_acc(p, q):
        if p == q:
            return False
        p_q = p*q

        return p_q.bit_length() == total_bits

    change_p = False
    while not is_acc(p, q):
        if change_p:
            p = get_prime(pbits)
        else:
            q = get_prime(qbits)
        change_p = not change_p
    return max(p, q), min(p, q)

def gen_RSA_keys(length):
    while True:
        (p, q) = find_p_q(length // 2)

        try:
            (e, d) = calculate_e_d(p, q)
            break
        except ValueError:
            pass
    dp = d % (p - 1)
    dq = d % (q - 1)
    q_inv = inverse(q, p)
    return p, q, e, d, dp, dq, q_inv

def get_RSA_keys(nbits):
    p, q, e, d, dp, dq, q_inv = gen_RSA_keys(nbits)
    n = p*q
    return (e,n), (n, p, q, e, d, dp, dq, q_inv)

def RSA_encrypt(x, key_e):
    e, n = key_e
    return pow(x, e, n)

def RSA_decrypt(c, key_d):
    n, p, q, e, d, dp, dq, q_inv = key_d
    m1 = pow(c, dp, p)
    m2 = pow(c, dq, q)
    h = (q_inv * (m1 - m2)) % p
    return m2 + h*q


# Запись и чтение ключей

def write_private_key(filename, key_d):
    seq = asn1.DerSequence(list(key_d))
    b64 = base64.b64encode(seq.encode())
    str_ = '-----BEGIN RSA PRIVATE KEY-----\n' + b64.decode('utf-8') + '\n-----END RSA PRIVATE KEY-----\n'
    with open(filename, 'w') as f:
        f.write(str_)

def write_public_key(filename, key_e):
    seq = asn1.DerSequence(list(key_e))
    b64 = base64.b64encode(seq.encode())
    str_ = '-----BEGIN RSA PUBLIC KEY-----\n' + b64.decode('utf-8') + '\n-----END RSA PUBLIC KEY-----\n'
    with open(filename, 'w') as f:
        f.write(str_)

def write_keys(filename, key_e, key_d):
    write_private_key(filename, key_d)
    write_public_key(filename + '.pub', key_e)
    print('RSA-ключи записаны в {} и {}.pub'.format(filename, filename))

def read_private_key(filename):
    with open(filename, 'r') as f:
        str_ = f.read()
    b64 = re.search('-----BEGIN RSA PRIVATE KEY-----\n(.+)\n-----END RSA PRIVATE KEY-----\n', str_).group(1)
    barr = base64.b64decode(b64)
    seq = asn1.DerSequence()
    seq.decode(barr)
    return tuple([seq[i] for i in range(8)])


def read_public_key(filename):
    with open(filename, 'r') as f:
        str_ = f.read()
    b64 = re.search('-----BEGIN RSA PUBLIC KEY-----\n(.+)\n-----END RSA PUBLIC KEY-----\n', str_).group(1)
    barr = base64.b64decode(b64)
    seq = asn1.DerSequence()
    seq.decode(barr)
    return tuple([seq[i] for i in range(2)])

def decode_public_key(key_str):
    b64 = re.search('-----BEGIN RSA PUBLIC KEY-----\n(.+)\n-----END RSA PUBLIC KEY-----\n', key_str).group(1)
    barr = base64.b64decode(b64)
    seq = asn1.DerSequence()
    seq.decode(barr)
    return tuple([seq[i] for i in range(2)])

def encode_public_key(key_e):
    seq = asn1.DerSequence(list(key_e))
    b64 = base64.b64encode(seq.encode())
    str_ = '-----BEGIN RSA PUBLIC KEY-----\n' + b64.decode('utf-8') + '\n-----END RSA PUBLIC KEY-----\n'
    return str_