from flask_moment import Moment
from flask_migrate import Migrate
from config import app, db
moment = Moment(app)
migrate = Migrate(app, db)

class Shows(db.Model):
    __tablename__ = 'Shows'
    id = db.Column(db.Integer, primary_key=True)
    artist_id =  db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue_id =   db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    start_time = db.Column(db.String(250), nullable = False)
    
    def __repr__(self):
      return f'<Artist {self.id} {self.artist_id}{self.venue_id} {self.start_time}>'

