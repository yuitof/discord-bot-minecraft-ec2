import os
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from flask import Flask, jsonify, request, abort

if os.environ.get('ENV') != 'production':
    from dotenv import load_dotenv
    load_dotenv()

app = Flask(__name__)

PUBLIC_KEY = os.environ.get('APPLICATION_PUBLIC_KEY')

@app.before_request
def verify_key():
    print('called before request')
    verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))

    signature = request.headers["X-Signature-Ed25519"]
    timestamp = request.headers["X-Signature-Timestamp"]
    body = request.data.decode("utf-8")

    try:
        verify_key.verify(f'{timestamp}{body}'.encode(), bytes.fromhex(signature))
    except BadSignatureError:
        abort(401, 'invalid request signature')

@app.route('/', methods=['POST'])
def my_command():
    try:
        print('called route')
        if request.json["type"] == 1:
            return jsonify({
                "type": 1
            })
        
        if request.json["type"] == 2:
            if request.json["data"]["name"] == "test":
                return jsonify({
                    "type": 4,
                    "data": {"content": "Hello👋"},
            })

    except Exception as e:
        print(e)

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=3000)
