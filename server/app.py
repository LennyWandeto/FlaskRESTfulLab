#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plants_dict = [pl.to_dict()for pl in Plant.query.all()]
        resp = make_response(jsonify(plants_dict), 200)
        return resp
    pass
    
    def post(self):
        data = request.get_json()
        new_rec = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price']
        )
        db.session.add(new_rec)
        db.session.commit()
        
        resp_in_dict = new_rec.to_dict()
        resp = make_response(resp_in_dict, 201)
        return resp


class PlantByID(Resource):
    def get(self, id):
        plants_dict = Plant.query.filter_by(id=id).first().to_dict()
        resp = make_response(jsonify(plants_dict), 200)
        return resp
    pass

api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
