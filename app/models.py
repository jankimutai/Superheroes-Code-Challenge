from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# HeroPower = db.Table('hero_powers',
#                          db.Column('id',db.Integer,primary_key=True),
#                          db.Column('strength',db.String()),
#                          db.Column('hero_id', db.Integer, db.ForeignKey('hero.id')),
#                          db.Column('power_id', db.Integer, db.ForeignKey('power.id')),
#                          db.Column('created_at',db.DateTime,default = datetime.utcnow()),
#                          db.Column('updated_at',db.DateTime,default = datetime.utcnow(),onupdate=datetime.utcnow()),)

class HeroPower(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    strength = db.Column(db.String())
    hero_id = db.Column( db.Integer, db.ForeignKey('hero.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('power.id'))
    created_at = db.Column(db.DateTime,default = datetime.utcnow())
    updated_at = db.Column(db.DateTime,default = datetime.utcnow(),onupdate=datetime.utcnow())


class Hero(db.Model):
    __tablename__ = 'hero'

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String())
    super_name= db.Column(db.String())
    created_at = db.Column(db.DateTime(),default = datetime.utcnow())
    updated_at = db.Column(db.DateTime(),default=datetime.utcnow(),onupdate=datetime.utcnow())
    #relationship
    powers = db.relationship("HeroPower",backref= "hero")

# add any models you may need. 
class Power(db.Model):
    __tablename__ = 'power'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    created_at = db.Column(db.DateTime(),default = datetime.utcnow())
    updated_at = db.Column(db.DateTime(),default=datetime.utcnow(),onupdate=datetime.utcnow())
    #relationship
    heroes = db.relationship("HeroPower",backref= "power")