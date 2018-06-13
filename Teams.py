from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Franchise, Base, TeamPlayer, User
 
engine = create_engine('sqlite:///indianfranchises.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# create a user
User1 = User(name="RAM", email="krishnavarmaindukuri@gmail.com")

#Menu for UrbanBurger
franchise1 = Franchise(name = "Royal Challangers Banglore")

session.add(franchise1)
session.commit()

teamPlayer1 = TeamPlayer(name = "Virat Kohli", description = "Right hand batsman", price = "$10000", course = "BATSMAN", franchise = franchise1)

session.add(teamPlayer1)
session.commit()

teamPlayer2 = TeamPlayer(name = "AB Deviliars", description = "Right hand batsman", price = "$9000", course = "BATSMAN", franchise = franchise1)

session.add(teamPlayer2)
session.commit()

teamPlayer3 = TeamPlayer(name = "Brendon Mucclum", description = "Right hand batsman", price = "$8500", course = "BATSMAN", franchise = franchise1)

session.add(teamPlayer3)
session.commit()

teamPlayer4 = TeamPlayer(name = "Mooean Ali", description = "Left hand batsman", price = "$7990", course = "ALLROUNDER", franchise = franchise1)

session.add(teamPlayer4)
session.commit()

teamPlayer5 = TeamPlayer(name = "Colum De Grandhome", description = "Right hand batsman", price = "$6998", course = "WICKETKEEPER", franchise = franchise1)

session.add(teamPlayer5)
session.commit()

teamPlayer6 = TeamPlayer(name = "Tim southee", description = "Right arm medium fast", price = "$7899", course = "BOWLER", franchise = franchise1)

session.add(teamPlayer6)
session.commit()

teamPlayer7 = TeamPlayer(name = "Umesh Yadav", description = "Right arm medium fast", price = "$4566", course = "BOWLER", franchise = franchise1)

session.add(teamPlayer7)
session.commit()

teamPlayer8 = TeamPlayer(name = "Chahal", description = "Right leg spin", price = "$5990", course = "BOWLER", franchise = franchise1)

session.add(teamPlayer8)
session.commit()



#CSK TEAM
franchise1 = Franchise(name = "CHENNAI SUPER KINGS")

session.add(franchise1)
session.commit()

teamPlayer1 = TeamPlayer(name = "M S DHONI", description = "Right hand batsman", price = "$10000", course = "BATSMAN", franchise = franchise1)

session.add(teamPlayer1)
session.commit()

teamPlayer2 = TeamPlayer(name = "DUPLESIS", description = "Right hand batsman", price = "$9000", course = "BATSMAN", franchise = franchise1)

session.add(teamPlayer2)
session.commit()

teamPlayer3 = TeamPlayer(name = "DWAYNE BRAVO", description = "Right hand batsman", price = "$8500", course = "BATSMAN", franchise = franchise1)

session.add(teamPlayer3)
session.commit()

teamPlayer4 = TeamPlayer(name = "SHANE WATSON", description = "Right hand batsman", price = "$7990", course = "WICKETKEEPER", franchise = franchise1)

session.add(teamPlayer4)
session.commit()

teamPlayer5 = TeamPlayer(name = "SURESH RAINA", description = "Left hand batsman", price = "$6998", course = "ALLROUNDER", franchise = franchise1)

session.add(teamPlayer5)
session.commit()

teamPlayer6 = TeamPlayer(name = "lungi Nigidi", description = "Right arm medium fast", price = "$7899", course = "BOWLER", franchise = franchise1)

session.add(teamPlayer6)
session.commit()

teamPlayer7 = TeamPlayer(name = "Deepak chahar", description = "Right arm medium fast", price = "$4566", course = "BOWLER", franchise = franchise1)

session.add(teamPlayer7)
session.commit()

teamPlayer8 = TeamPlayer(name = "Harbajan", description = "Right off spin", price = "$5990", course = "BOWLER", franchise = franchise1)

session.add(teamPlayer8)
session.commit()




#MI TEAM

franchise1 = Franchise(name = "MUMBAI INDIANS")

session.add(franchise1)
session.commit()

teamPlayer1 = TeamPlayer(name = "Rohit Sharma", description = "Right hand batsman", price = "$10000", course = "BATSMAN", franchise = franchise1)

session.add(teamPlayer1)
session.commit()

teamPlayer2 = TeamPlayer(name = "Ewen Lewis", description = "Left hand batsman", price = "$9000", course = "BATSMAN", franchise = franchise1)

session.add(teamPlayer2)
session.commit()

teamPlayer3 = TeamPlayer(name = "Surya Kumar Yadav", description = "Right hand batsman", price = "$8500", course = "BATSMAN", franchise = franchise1)

session.add(teamPlayer3)
session.commit()

teamPlayer4 = TeamPlayer(name = "Hardik Pandya", description = "Right hand batsman", price = "$7990", course = "ALLROUNDER", franchise = franchise1)

session.add(teamPlayer4)
session.commit()

teamPlayer5 = TeamPlayer(name = "Krunal Pandya", description = "Left hand batsman", price = "$6998", course = "WICKETKEEPER", franchise = franchise1)

session.add(teamPlayer5)
session.commit()

teamPlayer6 = TeamPlayer(name = "Bumrah", description = "Right arm medium fast", price = "$7899", course = "BOWLER", franchise = franchise1)

session.add(teamPlayer6)
session.commit()

teamPlayer7 = TeamPlayer(name = "Meclengam", description = "Right arm medium fast", price = "$4566", course = "BOWLER", franchise = franchise1)

session.add(teamPlayer7)
session.commit()

teamPlayer8 = TeamPlayer(name = "krish", description = "Right leg spin", price = "$5990", course = "BOWLER", franchise = franchise1)

session.add(teamPlayer8)
session.commit()

#KKR TEAM

franchise1 = Franchise(name = "KOLKATA KNIGHT RIDERS")

session.add(franchise1)
session.commit()

teamPlayer1 = TeamPlayer(name = "Dinesh Karthik", description = "Right hand batsman", price = "$10000", course = "BATSMAN", franchise = franchise1)

session.add(teamPlayer1)
session.commit()

teamPlayer2 = TeamPlayer(name = "Chris lynn", description = "Left hand batsman", price = "$9000", course = "BATSMAN", franchise = franchise1)

session.add(teamPlayer2)
session.commit()

teamPlayer3 = TeamPlayer(name = "Robin Utappa", description = "Right hand batsman", price = "$8500", course = "BATSMAN", franchise = franchise1)

session.add(teamPlayer3)
session.commit()

teamPlayer4 = TeamPlayer(name = "ANDREW russel", description = "Right hand batsman", price = "$7990", course = "ALLROUNDER", franchise = franchise1)

session.add(teamPlayer4)
session.commit()

teamPlayer5 = TeamPlayer(name = "Sunil naryan", description = "Left hand batsman", price = "$6998", course = "WICKETKEEPER", franchise = franchise1)

session.add(teamPlayer5)
session.commit()

teamPlayer6 = TeamPlayer(name = "kAMLESH", description = "Right arm medium fast", price = "$7899", course = "BOWLER", franchise = franchise1)

session.add(teamPlayer6)
session.commit()

teamPlayer7 = TeamPlayer(name = "Chawla", description = "Right arm medium fast", price = "$4566", course = "BOWLER", franchise = franchise1)

session.add(teamPlayer7)
session.commit()

teamPlayer8 = TeamPlayer(name = "kuldep", description = "Right leg spin", price = "$5990", course = "BOWLER", franchise = franchise1)

session.add(teamPlayer8)
session.commit()




print "Teams are added !"