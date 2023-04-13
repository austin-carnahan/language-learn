from app.models.user import User, db
from flask import make_response

def register_user(userdata):
    try:
        print(userdata)
        # Check if username already exists
        user_check = db.session.execute(db.select(User).filter_by(username=userdata['username'])).scalar()
        print(user_check)
        if user_check:
            print("Found existing username")
            return make_response({"message": "username already exists"}, 409)
        else:
            username = userdata['username']
            password = userdata['password']

            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()

            created_user = db.session.execute(db.select(User).filter_by(username=username)).scalar()
            print("Serializing Response...")
            return make_response({
                'message': f"New user: {created_user.username} successfully created",
                'username': created_user.username,
                'id': created_user.id,
            }, 200)

    except Exception as e:
        print(e)
        return make_response({'message': str(e)}, 500)
    
def login_user(credentials):
    try:
        # Check if username already exists
        user = db.session.execute(db.select(User).filter_by(username=credentials['username'])).scalar()
        print(user)
        if not user:
            return make_response({ "message": "username not found"}, 400)
        else:
            #TODO: use seperate method for hashing and validating password
            #TODO: login should return JWT token or something. Right now it doesnt do anything
            # Check password
            if credentials['password'] == user.password:
                return make_response({
                    'message': "User successfuly authenticated",
                    'username': {user.username},
                    'id': {user.id},
                }, 200)
            else:
                return make_response({'message': 'Incorrect password'}, 409)

    except Exception as e:
        print(e);
        return make_response({'message': str(e)}, 500)