import os
from flask import Flask

from db import get_db
import endpoints

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, "data", "data.db"),
    DEBUG=True
))
app.config.from_envvar("FLASKR_SETTINGS", silent=True)

if __name__ == "__main__":
    app.run()
