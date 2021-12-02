from flask import Flask, Response, request
from db_utils import PostgresID
from rsa_utils import RSA_encrypt, decode_public_key
from aes_utils import generate_eas_key, encrypt_AES, decrypt_AES
import json
import uuid
from Constant import Constant
from hashlib import shake_128
from ast import literal_eval


app = Flask(__name__)


def make_password(public_key, user_id):
    concat_str = public_key + str(user_id) + "mysalt"
    password = shake_128(concat_str.encode()).hexdigest(16)
    assert len(password) == 32
    password = int(password, 16)
    return password

@app.route('/registration', methods=["POST"])
def registration():
    pub_key = request.args.get("pub_key")
    aes_key = generate_eas_key()
    id_ = str(uuid.uuid4())
    print("id =", id_)
    print("aes key =", aes_key)
    password = make_password(pub_key, id_)
    container_aes_key = encrypt_AES(aes_key.to_bytes(16, "big"), password)
    print("cont aes key = {}\ndecontainer aes key = {}".format(
        container_aes_key, int.from_bytes(decrypt_AES(container_aes_key, password), "big")
    ))
    users_db.insert_user(id_, pub_key, container_aes_key)
    response_json = {"id": id_}
    response_string = json.dumps(response_json)
    return Response(response_string, status=200, mimetype="application/json")

@app.route('/get_aes', methods=["GET"])
def get_aes():
    id_ = request.args.get('id')
    exist = users_db.check_user(id_)
    if not exist:
        return Response("User {} not found".format(id_),
                        status=404)
    rsa_key_pub, container_aes_key = users_db.get_user_data(id_)
    container_aes_key = literal_eval(container_aes_key)
    password = make_password(rsa_key_pub, id_)
    print(container_aes_key)
    aes_key = decrypt_AES(container_aes_key, password)
    aes_key = int.from_bytes(aes_key, "big")
    rsa_key_pub = decode_public_key(rsa_key_pub)
    print("rsa key decode =", rsa_key_pub)
    print("aes key =", aes_key)
    enc_aes_key = RSA_encrypt(int(aes_key), rsa_key_pub)
    response_json = {"aes_key": enc_aes_key}
    response_string = json.dumps(response_json)

    return Response(response_string, status=200, mimetype="application/json")

if __name__ == "__main__":
    users_db = PostgresID(
        dbname = Constant.DB_NAME,
        user = Constant.DB_USER,
        password = Constant.DB_PASSWORD,
        host = Constant.DB_HOST,
        port = Constant.DB_PORT
    )
    app.run("0.0.0.0", port=6005, debug=False)