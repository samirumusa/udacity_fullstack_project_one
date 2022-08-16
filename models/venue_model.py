from flask_moment import Moment
from flask_migrate import Migrate
from config import app, db
moment = Moment(app)
migrate = Migrate(app, db)

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(200))
    seeking_talent =  db.Column(db.String(120))
    seeking_description =  db.Column(db.String(500))
    shows = db.relationship('Shows', backref='Venue', lazy=True)
    
    
    def __repr__(self):
      return f'<Todo {self.id} {self.name}, list {self.city}>'
