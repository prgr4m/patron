# -*- coding: utf-8 -*-
from flask import jsonify
from flask.views import MethodView


class ${resource_name}Resource(MethodView):
    decorators = []

    def get(self, ${resource_lower}_id):
        if ${resource_lower}_id is None:
            pass  # return all $resource_lower
        else:
            pass  # return a single $resource_lower

    def post(self):
        pass  # create a new $resource_lower

    def put(self, ${resource_lower}_id):
        pass  # update a single $resource_lower

    def delete(self, ${resource_lower}_id):
        pass  # delete a single $resource_lower
