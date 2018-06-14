from flask import Flask, render_template, request, redirect, jsonify, \
    url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Franchise, TeamPlayer, User

# Import Login session

from flask import session as login_session
import random
import string

# imports for gconnect

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

# import login decorator

from functools import wraps

app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json', 'r')
                       .read())['web']['client_id']
APPLICATION_NAME = 'Franchise Application'

engine = create_engine('sqlite:///indianfranchises.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_name' not in login_session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
@app.route('/login')
def showlogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():

    # validate state token

    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application-json'
        return response

    # Obtain authorization code

    code = request.data

    try:

        ''' upgrade the authorization code in credentials object '''

        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response =\
                   make_response(json.dumps('Failed to upgrade\
                   the authorization  code'), 401)
        response.headers['Content-Type'] = 'application-json'
        return response

    # Check that the access token is valid.

    access_token = credentials.access_token
    url = \
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' \
        % access_token
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1].decode('utf-8'))
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = \
            make_response(json.dumps("user ID doesn't match\
            givenuser ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    if result['issued_to'] != CLIENT_ID:
        response = \
            make_response(json.dumps("client ID does not match app's."), 401)
        print "client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = \
            make_response(json.dumps('Current user is already\
            connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    response = make_response(json.dumps('Succesfully connected', 200))

    # Get user information

    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    print 'User email is' + str(login_session['email'])
    user_id = getUserID(login_session['email'])
    if user_id:
        print 'Existing user#' + str(user_id) + 'matches this email'
    else:
        user_id = createUser(login_session)
        print 'New user_id#' + str(user_id) + 'created'
    login_session['user_id'] = user_id
    print 'Login session is tied to :id#' + str(login_session['user_id'])

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += \
        ' " style = "width: 300px; height: 300px;border-radius:150px;- \
      webkit-border-radius:150px;-moz-border-radius: 150px;">'
    flash('you are now logged in as %s' % login_session['username'])
    print 'done!'
    return output


def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).first()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).first()
        return user.id
    except:
        return None
''' DISCONNECT - Revoke a current user's token and reset their login_session'''


@app.route('/gdisconnect')
def gdisconnect():

    # only disconnect a connected User

    access_token = login_session.get('access_token')
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
        % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is'
    print result
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:

        response = \
            make_response(json.dumps('Failed to revoke token for\
            given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/logout')
def logout():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash('you have succesfully been logout')
        return redirect(url_for('showFranchises'))
    else:
        flash("you were not logged in")
        return redirect(url_for('showFranchises'))


@app.route('/franchise/<int:franchise_id>/team/JSON')
def franchiseTeamJSON(franchise_id):
    franchise = session.query(Franchise).filter_by(id=franchise_id).one()
    players = \
        session.query(TeamPlayer).filter_by(franchise_id=franchise_id).all()
    return jsonify(TeamPlayers=[s.serialize for s in players])


@app.route('/franchise/<int:franchise_id>/team/<int:team_id>/JSON')
def teamPlayerJSON(franchise_id, team_id):
    Team_Player = session.query(TeamPlayer).filter_by(id=team_id).one()
    return jsonify(Team_Player=Team_Player.serialize)


@app.route('/franchise/JSON')
def franchisesJSON():
    franchises = session.query(Franchise).all()
    return jsonify(franchises=[r.serialize for r in franchises])


# Show all franchise teams

@app.route('/')
@app.route('/franchise/')
def showFranchises():
    franchises = session.query(Franchise).all()
    # return "This page will show all my franchises"
    return render_template('franchises.html', franchises=franchises)
# Create a new Franchise


@app.route('/franchise/new/', methods=['GET', 'POST'])
def newFranchise():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newFranchise = Franchise(name=request.form['name'])
        session.add(newFranchise)
        session.commit()
        return redirect(url_for('showFranchises'))
    else:
        return render_template('newFranchise.html')
# return "This page will be for making a new franchise"

# Edit a franchise


@app.route('/franchise/<int:franchise_id>/edit/', methods=['GET', 'POST'])
def editFranchise(franchise_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedFranchise = \
        session.query(Franchise).filter_by(id=franchise_id).one()
    if editedFranchise.user_id != login_session['user_id']:
        return "<script>function myFunction(){alert('You are not authorized to\
        edit this franchise. please create your own franchise in order\
        to edit.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['name']:
            editedFranchise.name = request.form['name']
        return redirect(url_for('showFranchises'))
    else:
        return render_template('editFranchise.html',
                               franchise=editedFranchise)

# return 'This page will be for editing franchise %s' % franchise_id

# Delete a franchise


@app.route('/franchise/<int:franchise_id>/delete/', methods=['GET', 'POST'])
def deleteFranchise(franchise_id):
    if 'username' not in login_session:
        return redirect('/login')
    franchiseToDelete = \
        session.query(Franchise).filter_by(id=franchise_id).one()
    if franchiseToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('you are not authorized to\
         delete this franchise.please create your own franchise to delete');}\
         </script><body onLoad = 'myFunction()'>"
    if request.method == 'POST':
        session.delete(franchiseToDelete)
        session.commit()
        return redirect(url_for('showFranchises', franchise_id=franchise_id))
    else:
        return render_template('deleteFranchise.html',
                               franchise=franchiseToDelete)

# return 'This page will be for deleting franchise %s' % franchise_id

# Show a franchise TEAM


@app.route('/franchise/<int:franchise_id>/')
@app.route('/franchise/<int:franchise_id>/team/')
def showTeam(franchise_id):
    franchise = session.query(Franchise).filter_by(id=franchise_id).one()
    players = session.query(TeamPlayer).filter_by(
        franchise_id=franchise_id).all()
    return render_template('team.html', players=players, franchise=franchise)
    # return 'This page is the team for franchise %s' % franchise_id

# Create a new team player


@app.route('/franchise/<int:franchise_id>/team/new/', methods=['GET', 'POST'])
def newTeamPlayer(franchise_id):
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newPlayer = TeamPlayer(name=request.form['name'],
                               description=request.form['description'],
                               price=request.form['price'],
                               course=request.form['course'],
                               franchise_id=franchise_id)
        session.add(newPlayer)
        session.commit()

        return redirect(url_for('showTeam', franchise_id=franchise_id))
    else:
        return render_template('newteamplayer.html', franchise_id=franchise_id)

    return render_template('newTeamPlayer.html', franchise=franchise)
    # return 'This page is for making a new team player for franchise %s'
    # %franchise_id

# Edit a team player


@app.route('/franchise/<int:franchise_id>/team/<int:team_id>/edit',
           methods=['GET', 'POST'])
def editTeamPlayer(franchise_id, team_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedPlayer = session.query(TeamPlayer).filter_by(id=team_id).one()
    if login_session['user_id'] != editedPlayer.user_id:
        return "<script>function myFunction() {alert('You are not authorized to\
          edit  this team player.Please create your own tourist in\
          order to edit players.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['name']:
            editedPlayer.name = request.form['name']
        if request.form['description']:
            editedPlayer.description = request.form['name']
        if request.form['price']:
            editedPlayer.price = request.form['price']
        if request.form['course']:
            editedPlayer.course = request.form['course']
        session.add(editedPlayer)
        session.commit()
        return redirect(url_for('showTeam', franchise_id=franchise_id))
    else:

        return render_template('editteamplayer.html',
                               franchise_id=franchise_id,
                               team_id=team_id, player=editedPlayer)
# return 'This page is for editing team player %s' % team_id

# Delete a team player


@app.route('/franchise/<int:franchise_id>/team/<int:team_id>/delete',
           methods=['GET', 'POST'])
def deleteTeamPlayer(franchise_id, team_id):
    if 'username' not in login_session:
        return redirect('/login')
    playerToDelete = \
        session.query(TeamPlayer).filter_by(id=team_id).one()
    if login_session['user_id'] != playerToDelete.user_id:
        return "<script>function myFunction() {alert ('you are not authorized to\
         delete team player.please create your own franchise\
         in order to delete player');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(playerToDelete)
        session.commit()
        return redirect(url_for('showTeam', franchise_id=franchise_id))
    else:
        return render_template('deleteteamplayer.html',
                               player=playerToDelete)

    # return "This page is for deleting team player %s" % team_id

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
