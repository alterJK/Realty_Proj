from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def realty_main_page():
    return render_template("index.html")

from app_working.start_app_working import start_work_with_data
start_work_with_data()
