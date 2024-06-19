from flask_restful import Api, Resource, reqparse
from app import db
from flask import jsonify
from .models import Category, Post


def initialize_routes(api: Api):
    api.add_resource(CategoryListResource, '/categories')
    api.add_resource(CategoryResource, '/categories/<int:id>')
    api.add_resource(PostListResource, '/posts')
    api.add_resource(PostResource, '/posts/<int:id>')


class CategoryListResource(Resource):
    pass


class CategoryResource(Resource):
    pass


class PostListResource(Resource):
    def get(self):
        return {'id': 1}


class PostResource(Resource):
    pass