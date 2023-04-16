from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    diameter = db.Column(db.Integer)
    water_on_surface = db.Column(db.Boolean)

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "water_on_surface": self.water_on_surface,
            # do not serialize the password, its a security breach
        }

class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    skin_color = db.Column(db.String)

    planet_id = db.Column(db.Integer, db.ForeignKey("planets.id"))
    origin_planet = db.relationship("Planets")

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "skin_color": self.skin_color,
            "origin_planet": self.origin_planet.serialize(),
            # do not serialize the password, its a security breach
        }

class Favourites (db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user_favorite = db.relationship("User")

    external_type = db.Column(db.String, nullable=False)
    external_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Favourite from %r>' % self.user_favorite

    def serialize(self):
        return {
            "id": self.id,
            "external_type": self.external_type,
            "external_id": self.external_id
            # do not serialize the password, its a security breach
        }