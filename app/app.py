#!/usr/bin/env python3

from flask import Flask, make_response,jsonify,request
from flask_migrate import Migrate
from flask_restful import Api,Resource,reqparse

from models import db, Hero,Power,HeroPower
import jsonschema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
migrate = Migrate(app, db)

db.init_app(app)
api =Api(app)
class Home(Resource):
    def get(self):
        response_dict = {
            "message":"Welcome to Super Heroes API"
        }
        response = make_response(
            jsonify(response_dict),
            200,
        )
        return response
    
api.add_resource(Home,"/")

class Heroes(Resource):
    def get(self):
        heroes = Hero.query.all()
        hero_list = [{
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name
        } for hero in heroes]
        response = make_response(
            jsonify(hero_list),
            200,
        )
        return response
api.add_resource(Heroes,'/heroes')

class HeroesById(Resource):
    def get(self, id):
        hero = Hero.query.filter_by(id=id).first()
        if hero:
            hero_list = [{
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'powers':[]
        }]
            response =make_response(jsonify(hero_list),200)
            return response
        else:
            response_dict = {
            "error":"Hero not found"
            }
            response = make_response(
                jsonify(response_dict),
                200,
            )
            return response
api.add_resource(HeroesById,'/heroes/<int:id>')

class Powers(Resource):
    def get(self):
        powers = Power.query.all()
        power_list = [{
            'id': power.id,
            'name': power.name,
            'description': power.description
        } for power in powers]
        response = make_response(
            jsonify(power_list),
            200,
        )
        return response
api.add_resource(Powers,'/powers')
class PowerById(Resource):
    def get(self,id):
        power = Power.query.filter_by(id=id).first()
        if power:
            power_dict = {
                "id":power.id,
                "name":power.name,
                "description":power.description,
            }
            response = make_response(jsonify(power_dict),200)
            return response
        else:
            response = make_response(jsonify({"error":"Power not found"}))
            return response
        
    def patch(self,id):
        parser = reqparse.RequestParser()
        parser.add_argument("description")
        data = parser.parse_args()

        power = Power.query.filter_by(id=id).first()
        if power:
            if data['description']:
                power.description = data['description']

                try:
                    db.session.commit()
                except ValueError as e:
                    # Return a JSON data with the appropriate HTTP status code
                    error_message = str(e)
                    response = {
                        'errors': [error_message]
                    }
                    return make_response(jsonify(response), 500)
                else:
                    power_dict = {
                                "id":power.id,
                                "name":power.name,
                                "description":power.description
                            }
                    response = make_response(
                                jsonify(power_dict),
                                200
                            )
                    return response
                finally:
                    response = make_response(jsonify({"message": "Power updated successfully."}))
        else:
            response = make_response(jsonify({"error":"Power not found"}))
            return response

api.add_resource(PowerById,'/powers/<int:id>')      

class Hero_PowerResource(Resource):
    def post(self):
        data = request.get_json()

        strength = data['strength']
        power_id = data['power_id']
        hero_id = data['hero_id']
        hero_power = HeroPower(strength=strength, hero_id=hero_id, power_id=power_id)
        db.session.add(hero_power)
        db.session.commit()

        hero = Hero.query.filter_by(id=hero_id).all()
        powers = Power.query.filter_by(id=power_id).all()
        powers_data = [{
            "id":power.id,
            "name" :power.name,
            "description": power.description
            }for power in powers]
        response = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'powers': powers_data
        }
        return jsonify(response),201
api.add_resource(Hero_PowerResource,"/heropower")

if __name__ == '__main__':
    app.run(port=5555,debug=True)
