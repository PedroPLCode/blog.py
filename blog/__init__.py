from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__, static_folder='templates')
app.config.from_object(Config)
app.config['TEMPLATES_AUTO_RELOAD'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
  return {
      "db": db,
      "Favorite": models.Favorite,
      "Entry": models.Entry,
      "Comment": models.Comment,
      "Category": models.Category,
  }

from blog import routes, models