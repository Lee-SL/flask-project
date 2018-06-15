from werkzeug.security import safe_str_cmp
from user import User

users = [
    User(1,'bob','asdf')
]

username_mapping = {u.username: u for u in users}
userid_mapping = {u.id: u for u in users}

def authenticate(username, password):
    #get is useful as it can return none if there is no username instead of using item['chair'] for getting an object
    user = username_mapping.get(username, None)
    #safe way to compare strings from different ascii, unicode etc
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)