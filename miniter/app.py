"""
id, name, email, password, profile
"""
# jsonify : dicitionary --> JSON --> HTTP Response
from flask      import Flask, jsonify, request
from flask.json import JSONEncoder

app          = Flask(__name__)
app.users    = {}
app.id_count = 1

@app.route('/ping', methods=['GET'])
def ping():
    return 'pong'


@app.route('/sign-up', methods=['POST'])
def sign_up():
    new_user                = request.json
    new_user['id']          = app.id_count
    app.users[app.id_count] = new_user
    app.id_count            = app.id_count + 1

    return jsonify(new_user)


"""
tweet id 
tweet contents
"""

app.tweets = []

@app.route('/tweet', methods=['POST'])
def tweet():
    payload = request.json
    user_id = int(payload['id'])
    tweet = payload['tweet']

    if user_id not in app.users:
        return 'User doens not exists', 400

    if len(tweet) > 300:
        return "You've Reached The Limit of 300", 400

    user_id = int(payload['id'])

    app.tweets.append({
        'user_id' : user_id,
        'tweet'   : tweet
    })

    return '', 200


@app.route('/follow', methods=['POST'])
def follow():
    payload   = request.json
    user_id   = int(payload['id'])
    follow_id = int(payload['follow'])

    print('************* payload: ', payload)
    print('\nchecking user id: ', user_id)
    print('\nchecing data : ', app.users)

    if user_id not in app.users or follow_id not in app.users:
        return 'User Does Not Exist', 400

    user = app.users[user_id]
    user.setdefault('follow', set()).discard(follow_id)

    return jsonify(user)


"""
To Avoid JSON seializable ERROR
CustomJsonEncoder Class has been added
"""

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)

        return JSONEncoder.default(self, obj)

app.json_encoder = CustomJSONEncoder


