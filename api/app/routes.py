from flask_restful import Api, Resource, reqparse
from app import db
from flask import jsonify, request
from .models import Post
import logging

def initialize_routes(api: Api):
    api.add_resource(PostListResource, '/posts')
    api.add_resource(PostResource, '/posts/<int:id>')

# Define the request parser for parsing incoming POST data
post_parser = reqparse.RequestParser()
post_parser.add_argument('title', type=str, required=True, help='Title is required')
post_parser.add_argument('content', type=str, required=True, help='Content is required')
post_parser.add_argument('category_id', type=int, required=True, help='Category ID is required')

class PostListResource(Resource):
    def get(self):
        posts = Post.query.all()
        return jsonify([{'id': post.id, 'title': post.title, 'content': post.content, 'category_id': post.category_id} for post in posts])

    def post(self):
        try:
            args = post_parser.parse_args()
            new_post = Post(title=args['title'], content=args['content'], category_id=args['category_id'])
            db.session.add(new_post)
            db.session.commit()
            return jsonify({'message': 'Post created', 'post': {'id': new_post.id, 'title': new_post.title, 'content': new_post.content, 'category_id': new_post.category_id}}), 201
        except Exception as e:
            logging.error(f"Error creating post: {e}")
            db.session.rollback()
            return jsonify({'message': 'Internal Server Error', 'error': str(e)}), 500

class PostResource(Resource):
    def get(self, id):
        post = Post.query.get_or_404(id)
        return jsonify({'id': post.id, 'title': post.title, 'content': post.content, 'category_id': post.category_id})

    def put(self, id):
        try:
            post = Post.query.get_or_404(id)
            post_parser = reqparse.RequestParser()
            post_parser.add_argument('title', type=str, required=True, help='Title is required')
            post_parser.add_argument('content', type=str, required=True, help='Content is required')
            post_parser.add_argument('category_id', type=int, required=True, help='Category ID is required')
            args = post_parser.parse_args()
            post.title = args['title']
            post.content = args['content']
            post.category_id = args['category_id']
            db.session.commit()
            return {'message': 'Post updated', 'post': {'id': post.id, 'title': post.title, 'content': post.content, 'category_id': post.category_id}}
        except Exception as e:
            logging.error(f"Error updating post: {e}")
            db.session.rollback()
            return jsonify({'message': 'Internal Server Error', 'error': str(e)}), 500

