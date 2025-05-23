from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(50), nullable=False, default="Bob")
    last_name = db.Column(db.String(50), nullable=False, default="James")
    country = db.Column(db.String(80), nullable=False, default="JM")
    club = db.relationship('Club', back_populates='manager', uselist=False)

    def __init__(self, username, password, first_name, last_name, country):
        self.username = username
        self.set_password(password)
        self.first_name = first_name
        self.last_name = last_name
        self.country = country

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    
class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    logo = db.Column(db.String(150))
    country = db.Column(db.String(80), nullable=False)
    primary_color = db.Column(db.String(50))
    secondary_color = db.Column(db.String(50))
    tertiary_color = db.Column(db.String(50))

    manager_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    manager = db.relationship('User', back_populates='club')
    players = db.relationship('Player', back_populates='club', lazy=True)

    def __init__(self, name, logo, country):
        self.name = name
        self.logo = logo
        self.country = country

# class ClubPlayer(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     club_id = db.Column(db.Integer, db.ForeignKey('club.id'))
#     club_name = db.Column(db.String(100), nullable=False, unique=True)
#     player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
#     player_name = db.Column(db.String(100), nullable=False)
#     players = db.relationship('Player')

#     def __init__(self, club_id, club_name, player_id, player_name):
#         self.club_id = club_id
#         self.club_name = club_name
#         self.player_id = player_id
#         self.player_name = player_name
    

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(80), nullable=True)
    image = db.Column(db.String(150))
    captain = db.Column(db.Boolean, default=False)
    number = db.Column(db.Integer)
    age = db.Column(db.String(150))
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'))

    club = db.relationship('Club', back_populates='players', lazy=True)


    def __init__(self, name, role, country, image, captain, number, age, club_id):
        self.name = name
        self.role = role
        self.country = country
        self.image = image
        self.captain = captain
        self.number = number
        self.age = age
        self.club_id = club_id





