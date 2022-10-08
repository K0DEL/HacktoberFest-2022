from flask import Blueprint, request
from prisma.models import Post

post_blueprint = Blueprint('post', __name__)

@post_blueprint.route('/', methods=['GET','POST'])
def list_create():
  if request.method == 'GET':
    posts = Post.prisma().find_many()
    return {
      "data": [post.dict(exclude={'author'}) for post in posts]
    }

  if request.method == 'POST':
    data = request.json

    if data is None:
      return

    title = data.get('title')
    published = data.get('published')
    authorId = data.get('authorId')

    if title is None or published is None or authorId is None:
      return {"error": "You need to provide title, published and authorId"}

    post = Post.prisma().create(data={'title': title, 'authorId': authorId, 'published': published })


    return post.dict()

@post_blueprint.route('/<int:id>', methods=['GET','PUT', 'DELETE'])
def view_update_delete(id):
  if request.method == 'GET':

    post = Post.prisma().find_unique(where={'id': id}, include={'author': True})
    if post is None:
      return {'error': 'Post doesn`t exist'}, 404

    return post.dict()

  if request.method == 'PUT':
    data = request.json

    if data is None:
      return

    title = data.get('title')
    published = data.get('published')
    authorId = data.get('authorId')

    if title is None or published is None or authorId is None:
      return {"error": "You need to provide title, published and authorId"}

    post = Post.prisma().update(where={'id': id }, include={'author': True}, data={'title': title, 'published': published, 'author': {'connect': {'id': authorId}}})

    if post is None:
      return {'error': 'Post doesn`t exist'}, 404

    return post.dict()

  if request.method == 'DELETE':
    post = Post.prisma().delete(where={'id': id})
    if post is None:
      return {'error': 'Post doesn`t exist'}, 404

    return post.dict(exclude={'author'})
