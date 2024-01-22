from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import random

app = Flask(__name__)



@app.route('/')
def home():
    return render_template('index.html')




if __name__ == "__main__":
    app.run(port=2000)