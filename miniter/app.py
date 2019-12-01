"""
id, name, email, password, profile
"""
# jsonify : dictionary --> JSON --> HTTP Response
from flask      import Flask, jsonify, request
from flask.json import JSONEncoder
from sqlalchemy import create_engine, text


"""
To Avoid JSON seializable ERROR
CustomJsonEncoder Class has been added
Change SET to LIST
"""
class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)

        return JSONEncoder.default(self, obj)

app.json_encoder = CustomJSONEncoder


# Connect DB
def get_user(user_id):
    user = current.app.database.execute("""
        SELECT
            id,
            name,
            email,
            profile
        FROM users
        WHERE id =: user_id
    """), {
        'user_id' : user_id
    }).fetchone()

    return {
        'id'      : user['id'],
        'name'    : user['name'],
        'email'   : user['email'],
        'profile' : user['profile']
    } if user else None


def insert_user(user):
    return current_app.database.execute(text("""
        INSERT INTO users (
            name,
            email,
            profile,
            hashed_password
        ) VALUES (
            : name,
            : email,
            : profile,
            : password
        )
    """), user).lastrowid


def insert_tweet(user_tweet):
    return current_app.database.execute(text("""
        INSERT INTP tweets(
            user_id,
            tweet
        ) VALUES (
            :id,
            :tweet
        )
    """), user_tweet).rowcount


def insert_unfollow(user_unfollow):
    return current_app.database.execute(text("""
        DELETE FROM users_follow_list
        WHERE user_id =: id
        AND follow_user_id =: unfollow
    """), user_unfollow).rowcount


def get_timeline(user_id):
    timeline = current_app.database.execute(text("""
        SELECT
            t.user_id,
            t.tweet
        FROM tweets t
        LEFT JOIN users_follow_list ufl ON ufl.user_id =: user_id
        WHERE t.user_id =: user_id
        OR t.user_id = ufl.follow_user_id
    """), {
        'user_id' : user_id
    }).fetchall()


def create_app(test_config = None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_pyfile('config.py')

    else:
        app.config.update(test_config)

    database = create_engine(
        app.config['DB_URL'], 
        encoding = 'utf-8', 
        max_overflow = 0
    )
    app.database = database

    return app


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

    if user_id not in app.users or follow_id not in app.users:
        return 'User Does Not Exist', 400

    user = app.users[user_id]
    user.setdefault('follow', set()).discard(follow_id)

    return jsonify(user)


@app.route('/unfollow', methods=['POST'])
def unfollow():
    payload     = request.json
    user_id     = int(payload['id'])
    unfollow_id = int(payload['unfollow'])

    if user_id not in app.users or unfollow_id not in app.users:
        return 'User Does Not Exist', 400

    user = app.users[user_id]
    user.setdefault('follow', set()).discard(unfollow_id)

    return jsonify(user)



"""
TIME LINE
- user id
- follower's tweet list
- follower's id
- tweet contents
"""
@app.route('/timeline/<int:user_id>', methods=['GET'])
def timeline(user_id):
    if user_id not in app.users:
        return 'User Does Not Exist', 400

    follow_list = app.users[user_id].get('follow', set())
    follow_list.add(user_id)
    timeline = [tweet for tweet in app.tweets 
                if tweet['user_id'] in follow_list]

    return jsonify(
        {
            'user_id' : user_id,
            'timeline': timeline
        }
    )

