from flask import Flask
from boggle import Boggle

app = Flask(__name__)

boggle_game = Boggle()
