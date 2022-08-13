#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from cgitb import text
from email.headerregistry import Address
from itertools import count
import json
from os import stat
import sys
from tracemalloc import start
from turtle import onrelease
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(200))
    seeking_talent =  db.Column(db.String(120))
    seeking_description =  db.Column(db.String(500))
    shows = db.relationship('Shows', backref='Venue', lazy=True)
    
    
    def __repr__(self):
      return f'<Todo {self.id} {self.name}, list {self.city}>'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

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

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Shows(db.Model):
    __tablename__ = 'Shows'
    id = db.Column(db.Integer, primary_key=True)
    artist_id =  db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue_id =   db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    start_time = db.Column(db.String(250), nullable = False)

    def __repr__(self):
      return f'<Artist {self.id} {self.artist_id}{self.venue_id} {self.start_time}>'

    
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
 
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  #date = dateutil.parser.parse(value)
  if isinstance(value, str):
        date = dateutil.parser.parse(value)
  else:
        date = value
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------
def getVenues(cities):

  
  cnt =0
  venues =[]
  for k in cities:
    #venues= db.session.query(Venue).filter(Venue.city == k.city)
    return k
    """  for m in venues:
        venues.append({ 
                      "city":k['city'],
                      "state":k['state'],
                      "id": m.id,
                      "name": m.name,
                      "num_upcoming_shows": venues.count(), })
  return venues """
@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  vns = db.session.query(Venue).group_by(Venue.id, Venue.city, Venue.state).all()

  ls = []
  cities = {}
  cnt = len(vns)
  for i in range(len(vns)):
    r = vns[i]
    vns1 = db.session.query(Venue).filter(Venue.city ==r.city, Venue.state==r.state).all()
    ln = len(vns1)
    dict1 = {"city":r.city,
              "state":r.state,
              "venues": [{
                "id": r.id,
                "name": r.name,
                "num_upcoming_shows": ln,
              }]
             }
    ls.append(dict1)
   # [print(vns)]
   
    """
     vns1 = db.session.query(Venue).filter(Venue.city ==city, Venue.state==state).all() 
     ln = len(vns1)
    for j in range(len(vns1)):
       dict2 = {"venues": [{
                "id": vns1[j].id,
                "name": vns1[j].name,
                "num_upcoming_shows": ln,
              }]   
       }
       dict1.update(dict2)
       ls.append(dict1) """
  print(ls)
  """ count = 0
  for row in vns:
  
    cities= 
    count =+1
  data = getVenues(cities) """
  
  """  oneVenue = Venue.query.filter_by(id=2)
  for i in range(len(vns)):
    return i
  data1=[{
    "city": "San Francisco",
    "state": oneVenue,
    "venues": [{
      "id": 1,
      "name": "The Musical Hop",
      "num_upcoming_shows": 0,
    }, {
      "id": 3,
      "name": "Park Square Live Music & Coffee",
      "num_upcoming_shows": 1,
    }]
  }, {
    "city":'New York',
    "state": "NY",
    "venues": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }] """
  return render_template('pages/venues.html',  areas=ls); 

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  res = {}
  try:
    vn = db.session.query(Venue).filter(Venue.name == request.form.get('search_term', '')).all()
    cnt = 1
  
    error = False
    for v in vn:
        vnls={}
        vnls.add({ "count": cnt,
                    "data": [{
                      "id": v.id,
                      "name": v.name,
                      "num_upcoming_shows": len(vn),
                  }]
      })
        res.add(vnls)
  except:
     flash('Venue with title " ' + request.form['search_term'] + '" does not exit!')

  finally:
    db.session.close()

  """  response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  } """
  return render_template('pages/search_venues.html', results=res, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
 
    oneVenues = db.session.query(Venue).filter(Venue.id==venue_id).all()
    
    ls = []

    for oneVenue in oneVenues:
       dt={
          "id": oneVenue.id,
          "name": oneVenue.name,
          "genres": [],
          "address": oneVenue.address,
          "city": oneVenue.city,
          "state": oneVenue.state,
          "phone": oneVenue.phone,
          "website": oneVenue.website_link,
          "facebook_link": oneVenue.facebook_link,
          "seeking_talent": oneVenue.seeking_talent,
          "image_link":oneVenue.image_link,
          "past_shows": [],
          "upcoming_shows": [],
          "past_shows_count": 0,
          "upcoming_shows_count": 0,
        }
       ls.append(dt)
    #db.session.commit()
    # how to loop and push into the list in python
   
 
    """ 
    data1={
      "id": 1,
      "name": "The Musical Hop",
      "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
      "address": "1015 Folsom Street",
      "city": "San Francisco",
      "state": "CA",
      "phone": "123-123-1234",
      "website": "https://www.themusicalhop.com",
      "facebook_link": "https://www.facebook.com/TheMusicalHop",
      "seeking_talent": True,
      "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
      "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
      "past_shows": [{
        "artist_id": 4,
        "artist_name": "Guns N Petals",
        "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
        "start_time": "2019-05-21T21:30:00.000Z"
      }],
      "upcoming_shows": [],
      "past_shows_count": 1,
      "upcoming_shows_count": 0,
    }
    data2={
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "genres": ["Classical", "R&B", "Hip-Hop"],
      "address": "335 Delancey Street",
      "city": "New York",
      "state": "NY",
      "phone": "914-003-1132",
      "website": "https://www.theduelingpianos.com",
      "facebook_link": "https://www.facebook.com/theduelingpianos",
      "seeking_talent": False,
      "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
      "past_shows": [],
      "upcoming_shows": [],
      "past_shows_count": 0,
      "upcoming_shows_count": 0,
    }
    data3={
      "id": 3,
      "name": "Park Square Live Music & Coffee",
      "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
      "address": "34 Whiskey Moore Ave",
      "city": "San Francisco",
      "state": "CA",
      "phone": "415-000-1234",
      "website": "https://www.parksquarelivemusicandcoffee.com",
      "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
      "seeking_talent": False,
      "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "past_shows": [{
        "artist_id": 5,
        "artist_name": "Matt Quevedo",
        "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
        "start_time": "2019-06-15T23:00:00.000Z"
      }],
      "upcoming_shows": [{
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-01T20:00:00.000Z"
      }, {
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-08T20:00:00.000Z"
      }, {
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-15T20:00:00.000Z"
      }],
      "past_shows_count": 1,
      "upcoming_shows_count": 1,
    } """
    data = list(filter(lambda d: d['id'] == venue_id, ls))[0]
    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  myName = request.form.get('name')
  myCity = request.form.get('city')
  myState = request.form.get('state')
  myAddress = request.form.get('address')
  myPhone = request.form.get('phone')
  myFacebook_link = request.form.get('facebook_link')
  myImage_link = request.form.get('image_link')
  myWebsite_link = request.form.get('website_link')
  mySeeking_talent = request.form.get('seeking_talent')
  mySeeking_description = request.form.get('seeking_description')
  # TODO: modify data to be the data object returned from db insertion
  
  try:
    venue =  Venue(name=myName, city=myCity, state=myState, address=myAddress, phone=myPhone,image_link=myImage_link, website_link=myWebsite_link,facebook_link=myFacebook_link, seeking_talent=mySeeking_talent, seeking_description=mySeeking_description)
    # on successful db insert, flash success

    db.session.add(venue)
    db.session.commit()
    error = False
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
    
  except:
    error = True
    db.session.rollback()
  finally:
        db.session.close()
  if error:
    return error
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        #flash('An error occurred. Venue ' + myName + ' could not be listed.')

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return jsonify({ 'success': True })
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  vns = db.session.query(Artist).all()

  ls = []
  for i in vns:
    
    dict1 = {"id":i.id,
              "name":i.name,
              
             }
    ls.append(dict1)
  
  # TODO: replace with real data returned from querying the database
  data=[{
    "id": 4,
    "name": "Guns N Petals",
  }, {
    "id": 5,
    "name": "Matt Quevedo",
  }, {
    "id": 6,
    "name": "The Wild Sax Band",
  }]
  return render_template('pages/artists.html', artists=ls)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  res = {}
  try:
    vn = db.session.query(Artist).filter(Artist.name ==request.form.get('search_term', '')).all()
    cnt = 1
  
    error = False
    for v in vn:
        vnls={}
        vnls.add({ "count": cnt,
                    "data": [{
                      "id": v.id,
                      "name": v.name,
                      "num_upcoming_shows": len(vn),
                  }]
      })
        res.add(vnls)
  except:
     flash('Artist with a name " ' + request.form['search_term'] + '" does not exit!')

  finally:
    db.session.close()
  """  response={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
  } """
  return render_template('pages/search_artists.html', results=res, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
    oneArtists = db.session.query(Artist).filter(Artist.id==artist_id).all()
    
    ls = []

    for oneArtist in oneArtists:
       dt={
          "id": oneArtist.id,
          "name": oneArtist.name,
          "genres":[oneArtist.genres],
          "address": '',
          "city": oneArtist.city,
          "state": oneArtist.state,
          "phone": oneArtist.phone,
          "website": oneArtist.website_link,
          "facebook_link": oneArtist.facebook_link,
          "seeking_venue": oneArtist.seeking_venue,
          "seeking_description":oneArtist.seeking_description,
          "image_link":oneArtist.image_link,
          "past_shows": [],
          "upcoming_shows": [],
          "past_shows_count": 0,
          "upcoming_shows_count": 0,
        }
       ls.append(dt)
       """ data1={
      "id": 4,
      "name": "Guns N Petals",
      "genres": ["Rock n Roll"],
      "city": "San Francisco",
      "state": "CA",
      "phone": "326-123-5000",
      "website": "https://www.gunsnpetalsband.com",
      "facebook_link": "https://www.facebook.com/GunsNPetals",
      "seeking_venue": True,
      "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
      "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
      "past_shows": [{
        "venue_id": 1,
        "venue_name": "The Musical Hop",
        "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
        "start_time": "2019-05-21T21:30:00.000Z"
      }],
      "upcoming_shows": [],
      "past_shows_count": 1,
      "upcoming_shows_count": 0,
    }
    data2={
      "id": 5,
      "name": "Matt Quevedo",
      "genres": ["Jazz"],
      "city": "New York",
      "state": "NY",
      "phone": "300-400-5000",
      "facebook_link": "https://www.facebook.com/mattquevedo923251523",
      "seeking_venue": False,
      "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      "past_shows": [{
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
        "start_time": "2019-06-15T23:00:00.000Z"
      }],
      "upcoming_shows": [],
      "past_shows_count": 1,
      "upcoming_shows_count": 0,
    }
    data3={
      "id": 6,
      "name": "The Wild Sax Band",
      "genres": ["Jazz", "Classical"],
      "city": "San Francisco",
      "state": "CA",
      "phone": "432-325-5432",
      "seeking_venue": False,
      "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "past_shows": [],
      "upcoming_shows": [{
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
        "start_time": "2035-04-01T20:00:00.000Z"
      }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
        "start_time": "2035-04-08T20:00:00.000Z"
      }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
        "start_time": "2035-04-15T20:00:00.000Z"
      }],
      "past_shows_count": 0,
      "upcoming_shows_count": 3,
    } """
    
    data = list(filter(lambda d: d['id'] == artist_id, ls))[0]
    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  oneArtists = db.session.query(Artist).filter(Artist.id==artist_id).all()
    
  ls = []

  for oneArtist in oneArtists:
       artist={
          "id": oneArtist.id,
          "name": oneArtist.name,
          "genres":[oneArtist.genres],
          "address": '',
          "city": oneArtist.city,
          "state": oneArtist.state,
          "phone": oneArtist.phone,
          "website": oneArtist.website_link,
          "facebook_link": oneArtist.facebook_link,
          "seeking_venue": oneArtist.seeking_venue,
          "seeking_description":oneArtist.seeking_description,
          "image_link":oneArtist.image_link,
        }
       ls.append(artist)
  
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  myName = request.form.get('name')
  myCity = request.form.get('city')
  myState = request.form.get('state')
  myPhone = request.form.get('phone')
  myGenres = request.form.get('genre')
  myFacebook_link = request.form.get('facebook_link')
  myImage_link = request.form.get('image_link')
  myWebsite_link = request.form.get('website_link')
  mySeeking_venue = request.form.get('seeking_venue')
  mySeeking_description = request.form.get('seeking_description')
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  try:
    db.session.query(Artist).filter(Artist.id==artist_id).update(name=myName, city=myCity, state=myState, phone=myPhone,genres=myGenres,image_link=myImage_link, website_link=myWebsite_link,facebook_link=myFacebook_link, seeking_venue=mySeeking_venue, seeking_description=mySeeking_description)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
        db.session.close()
  if error:
     print(error)

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  myName = request.form.get('name')
  myCity = request.form.get('city')
  myState = request.form.get('state')
  myPhone = request.form.get('phone')
  myGenres = request.form.get('genre')
  myFacebook_link = request.form.get('facebook_link')
  myImage_link = request.form.get('image_link')
  myWebsite_link = request.form.get('website_link')
  mySeeking_venue = request.form.get('seeking_venue')
  mySeeking_description = request.form.get('seeking_description')
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  
  try:
    artist =  Artist(name=myName, city=myCity, state=myState, phone=myPhone,genres=myGenres,image_link=myImage_link, website_link=myWebsite_link,facebook_link=myFacebook_link, seeking_venue=mySeeking_venue, seeking_description=mySeeking_description)

    db.session.add(artist)
    db.session.commit()
    error = False
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
    
  except:
    error = True
    db.session.rollback()
  finally:
        db.session.close()
  if error:
     #return sys.exc_info()
    flash('An error occurred. Artist ' + myName + ' could not be listed.')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')

""" def create_show_submission():
  
  artistId = request.form.get('artist_id')
  venueId = request.form.get('venue_id')
  startTime = request.form.get('start_time')
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  print(request.form())
  try:
    show =  Shows(artist_id=artistId,venue_id=venueId,start_time=startTime)
    
    db.session.add(show)
    db.session.commit()
    error = False
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
    
  except:
    error = True
    db.session.rollback()
  finally:
        db.session.close()
  if error:
     #return sys.exc_info()
    flash('An error occurred. A show with the following ' + venueId + ' could not be created.')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')

 """
#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  sdb = db.session.query(Shows).join(Artist, Artist.id==Shows.artist_id).all()
  ls =[]
  for sd in sdb:
    #print(sd)
    
    ls.append({
    "venue_id": sd.Venue.id,
    "venue_name":sd.Venue.name,
    "artist_id": sd.Artist.id,
    "artist_name":sd.Artist.name,
    "artist_image_link":sd.Artist.image_link,
    "start_time":sd.start_time.strftime("%m/%d/%Y, %H:%M:%S") 
    })
  """  dct = {
    "venue_id": sd.venue_id,
    "venue_name":sd.,
    "artist_id": 4,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21T21:30:00.000Z"
    }
  """
  data=[{
    "venue_id": 1,
    "venue_name": "The Musical Hop",
    "artist_id": 4,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21T21:30:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 5,
    "artist_name": "Matt Quevedo",
    "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "start_time": "2019-06-15T23:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-01T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-08T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-15T20:00:00.000Z"
  }]
  return render_template('pages/shows.html', shows=ls)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  artistId = request.form.get('artist_id')
  venueId = request.form.get('venue_id')
  startTime = request.form.get('start_time')
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  
  show =  Shows(artist_id=artistId,venue_id=venueId,start_time=startTime)
  
  db.session.add(show)
  db.session.commit()
  error = False
  
  # on successful db insert, flash success
  flash('Show was successfully listed!')


      
      # TODO: on unsuccessful db insert, flash an error instead.
      # e.g., flash('An error occurred. Show could not be listed.')
      # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
