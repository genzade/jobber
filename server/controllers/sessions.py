from flask.ext.restful import Resource, reqparse
from flask.ext.security import login_user, logout_user
from flask.ext.security.utils import verify_password
from server.models.user import User


class SessionsResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email', location='json')
        self.reqparse.add_argument('password', location='json')
        super().__init__()


class SessionsAPI(SessionsResource):
    def post(self):
        args = self.reqparse.parse_args()
        user = User.query.filter_by(email=args['email']).first()
        if user and verify_password(args['password'], user.password):
            login_user(user)
            return dict(user=user.email), 200
        return 'Invalid username or password', 400

    def delete(self):
        logout_user()
        return 'Successfully logged out', 200
