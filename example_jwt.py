from flask import Flask, jsonify, request
import jwt
from datetime import datetime, timezone, timedelta

app = Flask(__name__)


@app.route("/", methods=["POST"])
def login():
    token = jwt.encode(
        payload={
            "exp": datetime.now(timezone.utc) + timedelta(minutes=1),
            # extra info that can be kept on the token
            "email": "sample@email.com"
        },
        key="my-secret-key",
        algorithm="HS256"
    )
    return jsonify({"token": token}), 200


@app.route("/secret", methods=["POST"])
def secret():
    raw_token = request.headers.get("Authorization")
    token = raw_token.split()[1]
    try:
        token_information = jwt.decode(token, key="my-secret-key",
            algorithms="HS256")
        print(raw_token)
        return jsonify({"token": token, "info": token_information}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
        

if __name__ == "__main__":
    app.run(debug=True)
