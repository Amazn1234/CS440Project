from flask import Flask, render_template, request, redirect, flash
from database import createApp

# refernce this file
app = Flask(__name__)

# initialize datbase
createApp(app)

# run as main
if __name__ == "__main__":
    app.run(debug=True)