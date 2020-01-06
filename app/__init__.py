
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
#login.init_app()
app.app_context().push()


from app import routes
from app.models import Contact, Company, FollowUp, User, Amount, Label_service, Email, Contractor, UserManager

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Contact': Contact, 'Company': Company, 'FollowUp': FollowUp, 'User': User, 'Amount': Amount,
            'Label_service': Label_service, 'Email': Email, 'Contractor': Contractor}