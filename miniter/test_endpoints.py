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
