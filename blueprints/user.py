from flask import Blueprint, request
from prisma.models import User

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/', methods=['GET','POST'])
def list_create():
  if request.method == 'GET':
    users = User.prisma().find_many(include={'posts': True})
    return {
      "data": [user.dict() for user in users]
    }

  if request.method == 'POST':
    data = request.json

    if data is None:
      return

    name = data.get('name')
    email = data.get('email')

    if name is None or email is None:
      return {"error": "You need to provide name and email"}

    user = User.prisma().create(data={'email': email, 'name': name})

    return dict(user)
