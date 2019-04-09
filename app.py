import os

from flask import Flask, abort, render_template, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import models
from models import Base

DATABASE_URL = os.environ['postgres://yraipitobmtkah:a1f09eee6ca129801364fd95fa9c3f5d468714ab6c9f1f3207578a1b00882a91@ec2-79-125-2-142.eu-west-1.compute.amazonaws.com:5432/d5rksg9bnf4fdi
']

# engine = create_engine("postgresql://postgres:postgres@localhost:5432/chinook")
engine = create_engine(DATABASE_URL)

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Base.query = db_session.query_property()

app = Flask(__name__)

cunter = 0

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route("/longest_tracks")
def longest_tracks():
    tracks = db_session.query(models.Track).order_by(models.Track.milliseconds).limit(10).all()
    return jsonify(dict(tracks))

                          
@app.route("/artists")
def artists():
    if request.method == "GET":
        return get_artists()
    abort(405)


def get_artists():
    artists = db_session.query(models.Artist).order_by(models.Artist.name)
    return "<br>".join(
        f"{idx}. {artist.name}" for idx, artist in enumerate(artists)
    )



                          
                          
if __name__ == "__main__":
    app.run(debug=False)
