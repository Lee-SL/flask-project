from werkzeug.security import safe_str_cmp
from user import User

def authenticate(username, password):
    #get is useful as it can return none if there is no username instead of using item['chair'] for getting an object
    user = User.find_by_username(username)
    #safe way to compare strings from different ascii, unicode etc
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)