from flask import Flask
from config import Configuration


app = Flask(__name__, static_url_path='/static')
app.config.from_object(Configuration)
