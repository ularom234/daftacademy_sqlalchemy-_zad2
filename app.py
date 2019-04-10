import os

from flask import Flask, abort, render_template, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import models
from models import Base

DATABASE_URL = os.environ['DATABASE_URL']

# engine = create_engine("postgresql://postgres:postgres@localhost:5432/chinook")
engine = create_engine(DATABASE_URL)

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Base.query = db_session.query_property()

app = Flask(__name__)

class InvalidUsage(Exception):
    status_code = 404

    def __init__(self, error, status_code=None, payload=None):
        super().__init__(self)
        self.error = error
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error'] = self.error
        return rv

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
    
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
 

@app.route("/longest_tracks")
def longest_tracks():
    tracks = db_session.query(models.Track).order_by(models.Track.milliseconds.desc()).limit(10)
    print (tracks)
    result_dict = []
    for u in tracks.all():
        result_dict.append(u.__dict__)
    for i in result_dict:
        del i['_sa_instance_state']
        dic = list(i.keys())
        for di in dic:
            i[di] = str(i[di])
    return jsonify(result_dict)

@app.route("/longest_tracks_by_artist")
def longest_tracks_by_artist():
    a = request.args
    if ('artist' in a):
        art = a['artist']
    else:
        abort(404)
        #raise InvalidUsage('missing artist')
        #return 404
        
    try:
        tracks = db_session.query(models.Track).join(models.Track.album).join(models.Album.artist).filter(models.Artist.name == art).order_by(models.Track.milliseconds.desc()).limit(10)

        result_dict = []
        for u in tracks.all():
            result_dict.append(u.__dict__)
        for i in result_dict:
            del i['_sa_instance_state']
            dic = list(i.keys())
            for di in dic:
                i[di] = str(i[di])

    except:
        abort(404)

    return jsonify(result_dict)


                          
                          
if __name__ == "__main__":
    app.run(debug=False)
