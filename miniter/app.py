"""
id, name, email, password, profile
"""
from flask import Flask, jsonify, request
# jsonify : dicitionary --> JSON --> HTTP Response

app          = Flask(__name__)
app.users    = {}
app.id_count = 1

@app.route('/ping', methods=['GET'])
def ping():
    return 'pong'

@app.route('/sign-up', methods=['POST'])
def sign_up():
    new_usre                = request.json
    new_user['id']          = app.id_count
    app.users[app.id_count] = new_user
    app.id_count            = app.id_count + 1

    return jsonify(new_user)
