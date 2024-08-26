from flask import Flask

app = Flask(__name__)

from app.Service import AudioProcessor
from app.Routes import api