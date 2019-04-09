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

cunter = 0

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route("/longest_tracks")
def longest_tracks():
    tracks = db_session.query(models.tracks).order_by(desc(models.tracks.Milliseconds)).limit(10)
    return jsonify(dict(tracks))

if __name__ == "__main__":
    app.run(debug=False)
