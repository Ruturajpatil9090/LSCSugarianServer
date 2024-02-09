from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Set the database URI directly in your code
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pymssql://sa:1234@localhost/Sugarian'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# The rest of your application configuration and routes

from app.routes.tender_routes import *
from app.Helpers.AccountMasterHelp import *
from app.Helpers.SystemMasterHelp import *
from app.Helpers.CityMasterHelp import *
from app.Helpers.GroupMasterHelp import *
from app.Helpers.GstRateMasterHelp import *
from app.Helpers.GstStateMasterHelp import *
from app.Helpers.BrandMasterHelp import *
from app.Helpers.TenderUtilityHelp import *