from app import db
from flask_login import UserMixin


class DiveEvent(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable = False)
    dive_site_id = db.Column(db.Integer, db.ForeignKey('dive_site.id', ondelete='CASCADE'), nullable = False)
    date = db.Column(db.DateTime, nullable=False)
    

    def __repr__(self):
        return '{}{}{}'.format(self.user_id, self.dive_site_id, self.date)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False, index=True)
    email = db.Column(db.String(150), unique=True, nullable=False)  #
    password = db.Column(db.String(200), nullable=False)
    user_favourites = db.Column(db.Text, default = "[]")
    

    def __repr__(self):
        return '{}{}{}'.format(self.id, self.username, self.email)


class DiveSite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False, index=True)
    location = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_path = db.Column(db.String(200), nullable=True)
    dive_events = db.relationship('DiveEvent', backref='dive_site', lazy='dynamic')
    
    
    def __repr__(self):
        return '{}{}{}'.format(self.id, self.name, self.location)
    

class Favourites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    dive_site_id = db.Column(db.Integer, db.ForeignKey('dive_site.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return '{}{}{}'.format(self.id, self.user_id, self.dive_site_id)
        