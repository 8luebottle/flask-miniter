import bcrypt
import config
import pytest
import json

from app        import create_app
from sqlalchemy import create_engine, text

database = create_engine(config.text_config['DB_URL'], encoding = 'UTF-8', max_overflow = 0)

@pytest.fixture
def api():
    app = create_app(config.test_config)
    app.config['TEST'] = True
    api = app.test_client()

    return api


def test_tweet(api):
    # Create New Test User
    new_user = {
        'email'   : 'baby_tiger2019@gmail.com'
        'passowrd': 'babytiger2019baby'
        'name'    : 'Baby Tiger'
        'profile' : 'Tech Blogger'
    }
    resp = api.post(
        '/sign-up',
        data         = json.dumps(new_user),
        content_type = 'application/jsson'
    )
    assert resp.status_code ==200

    # GET the ID of the New User
    resp_json   = json.loads(resp.data.decode('UTF-8'))
    new_user_id = resp_json['id']

    # LOG IN TEST
    rest = api.post(
        '/login',
        data = json.dumps(
            { 
                'email'   : 'baby_tiger2019@gmail.com',
                'password': 'babytiger2019baby'
            }
        ), 
        content_type = 'application/json'
    )
    rest_json    = json.loads(resp.data.decode('UTF-8'))
    access_token = resp_json['access_token']

    # TWEET TEST
    resp = api.post(
        '/tweet',
        data         = json.dumps({ 'tweet' : 'Hellow World!' }),
        content_type = 'application/json',
        headers      = {'Authorization' : access_token}
    )
    assert resp.status_code == 200

    # CHECK UP TWEET
    resp   = api.get(f'/timeline/{new_user_id}')
    tweets = json.loads(resp.data.decode('UTF-8')) 

    assert resp.status_code == 200
    assert tweets == {
        'user_id' : 1,
        'timeline': [
            {
                'user_id' : 1,
                'tweet'   : 'Hello World!'
            }
        ]
    }
