#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from cgitb import text
from email.headerregistry import Address
from itertools import count
import json
from os import stat
import sys
sys.path.append('C:\\Users\\MINE\\Desktop\\FSND\\projects\\01_fyyur\\starter_code\\models')
from tracemalloc import start
from turtle import onrelease
import dateutil.parser
from datetime import date
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from config import app, db
from models import show_model , venue_model, artist_model

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
app.config.from_object('config')
Shows = show_model.Shows
Venue = venue_model.Venue
Artist = artist_model.Artist
# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


    # TODO: implement any missing fields, as a database migration using Flask-Migrate


# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

    
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
   
@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  vns = db.session.query(Venue).group_by(Venue.id, Venue.city, Venue.state).all()
  ls = []
  for i in range(len(vns)):
    r = vns[i]
    dict1 = {"city":r.city,
              "state":r.state,
              "venues": [{
                "id": r.id,
                "name": r.name,
                "num_upcoming_shows": len(db.session.query(Venue).join(Shows, Shows.venue_id == Venue.id).filter(Shows.venue_id==r.id).all()),
              }]
             }
    ls.append(dict1)
   # [print(vns)]
   
  return render_template('pages/venues.html',  areas=ls); 

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  vnls ={}
  res = {}
  data=[]
  try:
    vn = db.session.query(Venue).all()
    error = False
    
    for v in vn:
        #print("My v",v.name)
        data.append({
                      "id": v.id,
                      "name": v.name,
                      "num_upcoming_shows": len(db.session.query(Shows).join(Venue).filter(Shows.venue_id==v.id).filter(Shows.start_time > datetime.now()).all()),
         })
    
    vnls.update({"count": len(vn),'data':data})
    #print(vnls)
  except:
     flash('Venue with title " ' + request.form['search_term'] + '" does not exit!')
  finally:
    db.session.close()
  return render_template('pages/search_venues.html', results=vnls, search_term=request.form.get('search_term', ''))
def get_artist_show(artist_data):
   arr = []
    
   for a in artist_data:
      dt = db.session.query(Artist).filter(Artist.id == a).all()
      for d in dt:
       
        arr.append(d.name)   

   return arr
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
 
    oneVenues = db.session.query(Venue).filter(Venue.id==venue_id).all()
    shws =  db.session.query(Shows).join(Venue, Venue.id == Shows.venue_id).filter(Shows.venue_id == venue_id).all()
    #shws = db.session.query(Venue).filter(Venue.id==venue_id).join(Shows, Shows.venue_id==Venue.id).all()
    shows_count = len(shws)
    past_shows = db.session.query(Shows).join(Venue).filter(Shows.venue_id==venue_id).filter(Shows.start_time < datetime.now()).all()
    upcoming_shows = db.session.query(Shows).join(Venue).filter(Shows.venue_id==venue_id).filter(Shows.start_time > datetime.now()).all()
    
    """ upcoming_shows =[]
    past_shows=[]
    artst = []
    myDate = datetime.now()
    for shw in shws:
        #print(shw)
        dtt = shw.start_time.strftime("%m/%d/%Y")
        artst.append(shw.artist_id)
        if( datetime.strptime(dtt,"%m/%d/%Y") > myDate ):
           upcoming_shows.append(shw) 
        else:
           past_shows.append(shw)
           
  """

       
    ls = []
    
    for oneVenue in oneVenues:
       dt={
          "id": oneVenue.id,
          "name": oneVenue.name,
          "genres":[oneVenue.genres],
          "address": oneVenue.address,
          "city": oneVenue.city,
          "state": oneVenue.state,
          "phone": oneVenue.phone,
          "website": oneVenue.website_link,
          "facebook_link": oneVenue.facebook_link,
          "seeking_talent": oneVenue.seeking_talent,
          "image_link":oneVenue.image_link,
          "past_shows":past_shows,                  #get_artist_show(past_shows),
          "upcoming_shows":upcoming_shows,               #get_artist_show(upcoming_shows),
          "past_shows_count": len(past_shows),            #len(get_artist_show(past_shows)),
          "upcoming_shows_count":len(upcoming_shows)         #len(get_artist_show(upcoming_shows)),
        }
       ls.append(dt)
       
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
    form = VenueForm(request.form)

    if form.validate():
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
 
  return render_template('pages/artists.html', artists=ls)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
   artls ={}
   data =[]
   try:
      art = db.session.query(Artist).all()
      error = False
      for a in art:
          data.append({
                        "id": a.id,
                        "name": a.name,
                        "num_upcoming_shows": len(db.session.query(Shows).join(Artist).filter(Shows.artis_id==a.id).filter(Shows.start_time > datetime.now()).all())})
      
      artls.update({"count": len(art),'data':data})
   except:
      error = True
      flash('Artist with a name " ' + request.form['search_term'] + '" does not exit!')
   finally:
    db.session.close()
   if error:
     print(error)
   return render_template('pages/search_artists.html', results=artls, search_term=request.form.get('search_term', ''))
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
    oneArtists = db.session.query(Artist).filter(Artist.id==artist_id).all()
    
    shws =  db.session.query(Shows).join(Artist, Artist.id == Shows.artist_id).filter(Shows.artist_id == artist_id).all()
    past_shows = db.session.query(Shows).join(Venue).filter(Shows.artist_id==artist_id).filter(Shows.start_time < datetime.now()).all()
    upcoming_shows = db.session.query(Shows).join(Venue).filter(Shows.artist_id==artist_id).filter(Shows.start_time > datetime.now()).all()
    ls = []
    """ upcoming_shows =[]
    past_shows=[]
    artst = []
    myDate = datetime.now()
    for shw in shws:
        #print(shw)
        dtt = shw.start_time.strftime("%m/%d/%Y")
         
        if( datetime.strptime(dtt,"%m/%d/%Y") > myDate ):
           upcoming_shows.append(shw) 
        else:
           past_shows.append(shw) """
          
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
          "past_shows":past_shows,                  #get_artist_show(past_shows),
          "upcoming_shows":upcoming_shows,               #get_artist_show(upcoming_shows),
          "past_shows_count": len(past_shows),            #len(get_artist_show(past_shows)),
          "upcoming_shows_count":len(upcoming_shows)         #len(get_artist_show(upcoming_shows)),
        }
       ls.append(dt)
    
    data = list(filter(lambda d: d['id'] == artist_id, ls))[0]
    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  #form = ArtistForm()
  oneArtists = db.session.query(Artist).filter(Artist.id==artist_id)
  form = ArtistForm( obj = oneArtists.first() )
  ls = []

  for oneArtist in oneArtists.all():
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
    form = VenueForm(request.form)

    if form.validate():
      db.session.query(Artist).filter(Artist.id==artist_id).update(name=myName, city=myCity, state=myState, phone=myPhone,genres=myGenres,image_link=myImage_link, website_link=myWebsite_link,facebook_link=myFacebook_link, seeking_venue=mySeeking_venue, seeking_description=mySeeking_description)
      db.session.commit()
  except:
    error = True
    db.session.rollback()
    flash('Venue' + request.form['name'] + ' was not updated!')
  finally:
        db.session.close()
  if error:
      print(error)

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  
  oneVenue = db.session.query(Venue).filter(Venue.id==venue_id)
  form = VenueForm( obj = oneVenue.first() )
  ls = []
  for v in oneVenue.all():
 
      venue={
        "id": v.id,
        "name": v.name,
        "genres": [v.genres],
        "address": v.address,
        "city": v.city,
        "state": v.state,
        "phone": v.phone,
        "website": v.website_link,
        "facebook_link": v.facebook_link,
        "seeking_talent": v.seeking_talent,
        "seeking_description": v.seeking_description,
        "image_link": v.image_link     }
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
  myGenres = request.form.getlist('genres[]')
  myFacebook_link = request.form.get('facebook_link')
  myImage_link = request.form.get('image_link')
  myWebsite_link = request.form.get('website_link')
  mySeeking_venue = request.form.get('seeking_venue')
  mySeeking_description = request.form.get('seeking_description')
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  
  try:
    form = VenueForm(request.form)

    if form.validate():
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

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  sdb = db.session.query(Shows).join(Artist, Artist.id==Shows.artist_id).all()
  ls =[]
  data = []
  for i in Shows.query.all():
    data.append({
    "venue_id": i.venue_id,
    "venue_name": Venue.query.filter_by(id =i.venue_id).first().name,
    "artist_id": i.artist_id,
    "artist_name": Artist.query.filter_by(id =i.artist_id).first().name,
    "artist_image_link": Artist.query.filter_by(id =i.artist_id).first().image_link,
    "start_time": i.start_time.strftime("%m/%d/%Y, %H:%M:%S")
    })
 
  return render_template('pages/shows.html', shows=data)

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
  form = VenueForm(request.form)

  if form.validate():
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

