from .user import create_user, create_club, create_player, join_club
from App.database import db
import os, csv, requests

API_URL = "https://apiv3.apifootball.com/"
API_KEY = "93569dc5d3595dcf5599537b3231d52321b5bac97afecec1ff90afbf90c62975"


def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass', 'Bob', 'Marley', 'Jamaica')

    params = {
        'action': 'get_teams',
        'league_id': 152,
        'APIkey': API_KEY
    }
    color_codes = [{
        'name': 'Manchester City',
        'primary': '#6CABDD',
        'secondary': '#ffffff',
        'tertiary': '#1C2C5B'
    },
    {
        'name': 'Liverpool',
        'primary': '#c8102E',
        'secondary': '#ffffff',
        'tertiary': '#00B2A9'
    },
    {
        'name': 'Chelsea',
        'primary': '#034694',
        'secondary': '#ffffff',
        'tertiary': '#dba111'
    },
    {
        'name': 'Manchester United',
        'primary': '#DA291C',
        'secondary': '#FBE122',
        'tertiary': '#000000'
    },
    {
        'name': 'Arsenal',
        'primary': '#EF0107',
        'secondary': '#9C824A',
        'tertiary': '#FFFFFF'
    },
    {
        'name': 'Leicester City',
        'primary': '#003090',
        'secondary': '#ffffff',
        'tertiary': '#fdbe11'
    },
    {
        'name': 'Tottenham Hotspur',
        'primary': '#132257',
        'secondary': '#ffffff',
        'tertiary': '#ffffff'
    },
    {
        'name': 'AFC Bournemouth',
        'primary': '#DA291C',
        'secondary': '#000000',
        'tertiary': '#A89968'
    },
    {
        'name': 'Southampton',
        'primary': '#d71920',
        'secondary': '#130c0e',
        'tertiary': '#FFC20E'
    },
    {
        'name': 'Everton',
        'primary': '#003399',
        'secondary': '#ffffff',
        'tertiary': '#ffffff'
    },
    {
        'name': 'Wolverhampton Wanderers',
        'primary': '#FDB913',
        'secondary': '#231F20',
        'tertiary': '#ffffff'
    },
    {
        'name': 'Brighton & Hove Albion',
        'primary': '#0057B8',
        'secondary': '#ffffff',
        'tertiary': '#ffffff'
    },
    {
        'name': 'West Ham United',
        'primary': '#7A263A',
        'secondary': '#1bb1e7',
        'tertiary': '#F3D459'
    },
    {
        'name': 'Fulham',
        'primary': '#000000',
        'secondary': '#ffffff',
        'tertiary': '#CC0000'
    },
    {
        'name': 'Brentford',
        'primary': '#D20000',
        'secondary': '#ffffff',
        'tertiary': '#FFB400'
    },
    {
        'name': 'Aston Villa',
        'primary': '#670e36',
        'secondary': '#95bfe5',
        'tertiary': '#fee505'
    },
    {
        'name': 'Nottingham Forest',
        'primary': '#DD0000',
        'secondary': '#ffffff',
        'tertiary': '#ffffff'
    },
    {
        'name': 'Newcastle United',
        'primary': '#241F20',
        'secondary': '#ffffff',
        'tertiary': '#F1BE48'
    },
    {
        'name': 'Ipswich Town',
        'primary': '#3a64a3',
        'secondary': '#ffffff',
        'tertiary': '#de2c37'
    },
    {
        'name': 'Crystal Palace',
        'primary': '#1B458F',
        'secondary': '#a7a5a6',
        'tertiary': '#C4122E'
    }]
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        for team in response.json():
            new_team = create_club(
                name=team['team_name'],
                logo=team['team_badge'],
                country=team['team_country']
            )
            for color in color_codes:
                if new_team.name == color['name']:
                    new_team.primary_color = color['primary']
                    new_team.secondary_color = color['secondary']
                    new_team.tertiary_color = color['tertiary']

            db.session.add(new_team)
            for player in team.get('players', []):
                is_captain = False
                if player['player_is_captain'] == "0" or player['player_is_captain'] == "":
                    is_captain = False
                else:
                    is_captain = True

                player_name = ""
                if not player['player_complete_name']:
                    player_name = player['player_name']
                else:
                    player_name = player['player_complete_name']        
                
                new_player = create_player(
                    name=player['player_name'],
                    role=player['player_type'],
                    country=player['player_country'],
                    image=player['player_image'],
                    captain=is_captain,
                    number=player['player_number'],
                    age=player['player_age'],
                    club_id = new_team.id
                )
                db.session.add(new_player)
        join_club(1,1)        
        db.session.commit()
        print('Teams and Players Imported!')

        

    