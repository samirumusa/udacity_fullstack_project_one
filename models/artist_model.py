from flask_moment import Moment
from flask_migrate import Migrate
from config import app, db
moment = Moment(app)
migrate = Migrate(app, db)

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(200))
    seeking_venue =  db.Column(db.String(120))
    seeking_description =  db.Column(db.String(500))
    shows = db.relationship('Shows', backref='Artist', lazy=True)
    
    
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    def __repr__(self):
      return f'<Artist {self.id} {self.name}{self.facebook_link} {self.phone} {self.state} {self.city} {self.genres} {self.image_link}>'
