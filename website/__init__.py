from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

#this is the object we're going to use when we want to create a new user etc
db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__) #__name__ reps the name of the file/initializes flask
    app.config['SECRET KEY'] = 'test'

    #My SQLALCHEMY DB is located at this location f'sqllite:///{DB_NAME}
    app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_NAME}' #This f string will only work for python 3.6 and above

    #initialize our DB by giving it our Flask App
    db.init_app(app)


    from .views import views
    from .auth import auth

    #register our blueprints w/ our flask application
    app.register_blueprint(views, url_prefix='/')
    #url_prefix is saying all of the urls that are stored inside of this "auth" file, how do i access them?
    #do i have to go to a prefix specifically?
        #Eg. if it were url_prefix='/auth'), whatever routes are in the "auth" file would 
            # be prefixed by what ever is define as the url_prefix. So a route defined as 'hello' would be 
            # prefixed as /auth/hello
    app.register_blueprint(auth, url_prefix='/') 

    from .models import User, Note
    #import .models as models 

    create_database(app)

    
    login_manager = LoginManager() 
    login_manager.login_view = 'auth.login' #Flask redirect us to here if the user is not logged in and there's login required
    login_manager.init_app(app) #This tells the login manager which app we are using

    #This tells flask how we load a user
    #We are looking for the user model and we are going to reference the user by their ID
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) #This looks for the primary key and check if its equal to whatever we pass


    return app

#This checks if the DB already exists, and if it does not, it is going to create it.
#It will not override what's already in the DB
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
