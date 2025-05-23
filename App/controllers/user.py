from App.models import User, Club, Player
from App.database import db


def create_user(username, password, first_name, last_name, country):
    newuser = User(username=username, password=password, first_name=first_name, last_name=last_name, country=country)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None

#Club Functions

def create_club(name, logo, country):
    newClub = Club(name=name, logo=logo, country=country)
    db.session.add(newClub)
    db.session.commit()
    return newClub

def get_club(id):
    return Club.query.get(id)

def get_all_clubs():
    return Club.query.all()

def search_clubs(page):
    matching_club = Club.query
    return matching_club.paginate(page=page, per_page=5)

def current_club(id):
    current_club = Club.query.get(id)
    return current_club

def next_club(id):
    next_club = Club.query.filter(Club.id > id).order_by(Club.id.asc()).first()
    return next_club

def prev_club(id):
    prev_club = Club.query.filter(Club.id < id).order_by(Club.id.desc()).first()
    return prev_club

#User Functions

def join_club(user_id, club_id):
    user = get_user(user_id)
    club = get_club(club_id)

    club.manager = user
    db.session.commit()

def leave_club(user_id, club_id):
    user = get_user(user_id)
    club = get_club(club_id)

    if club.manager == user and user.club == club:
        club.manager = None
        user.club = None
        db.session.commit()
    return None


#Player Functions
def create_player(name, role, country, image, captain, number, age, club_id):
    new_player = Player(name=name,role=role,country=country,image=image,captain=captain,number=number,age=age, club_id=club_id)
    new_player.club = get_club(club_id)

    db.session.add(new_player)
    db.session.commit()
    # player_id = new_player.id
    # player_name = new_player.name
    # club = get_club(club_id)
    # club_name = club.name
    # new_club_player = ClubPlayer(club_id=club_id, club_name=club_name, player_id=player_id, player_name=player_name)
    # db.session.add(new_club_player)
    # db.session.commit()
    return new_player
    
def get_all_players():
    return Player.query.all()

def get_club_players(club_id):
    players = Player.query.filter_by(club_id=club_id).all()
    return players
    

