"""Twitter type data model"""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User """

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(40))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s x>" % (self.user_id)


class Followship(db.Model):
    """One user follows another"""

    __tablename__ = "followships"

    followship_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    followee_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    followee = db.relationship("User",
                           foreign_keys='Followship.follower_id',
                           backref=db.backref('followee_followships'))
    follower = db.relationship("User",
                           foreign_keys='Followship.followee_id', 
                           backref=db.backref('follower_followships'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Followship followship_id=%s follower=%s followee=%s>" % (self.followship_id, self.follower_id, self.followee_id)

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///followers.db'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
