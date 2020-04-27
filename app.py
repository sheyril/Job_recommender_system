from flask import Flask, render_template, url_for, flash, redirect, request, abort, jsonify, Response, send_file
from flask_sqlalchemy import SQLAlchemy
import sys
import text as pr
from forms import RegistrationForm, LoginForm
app = Flask(__name__)
import csv

app.config['SECRET_KEY'] = 'b1b83de6a9239e9d1b057125dd75b1ae ' 

with open('cv_data.csv') as f:
    posts = [{k: v for k, v in row.items()}
        for row in csv.DictReader(f, skipinitialspace=True)]


@app.route('/', methods=['GET', 'POST'])
# @app.route('/home')
def home():
    return render_template('home.html')

@app.route('/browse')
def browse():
    return render_template('browse.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
    	flash(f'Account created {form.username.data}', 'success')
    	return redirect(url_for('home'))
    return render_template('register.html', title = 'Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
    	return render_template('login.html', title = 'Login', form=form)

@app.route("/recomm", methods=['POST'])
def submitcv():
    try:
        resume_file = request.files['file']
        filename = resume_file.filename
        # selected_area = request.form['area'].lower()
    #     cfg = "./indeed/{}/config.toml".format(selected_area)
        print(filename)
        sys.stdout.flush()
        resume_file.save(".//server_files//" + filename, buffer_size=16384)
        resume_file.close()
        pr.run_parse_resume("./server_files/" + filename)
    #     # print(len(query))
    #     # print(cfg)
    #     results = rk.run_ranker(cfg, "./server_files/resume-query.txt", 20)
    #     print(results)
    #     sys.stdout.flush()
    #     json_file = "./indeed/{}/jobs.json".format(selected_area)
    #     json_list = prepare_results(results, json_file)
    #     # print(json_list)
    #     # response = {'message': 'resume received. file name = {}'.format(filename)}
    #     # print ("up here")
        # return Response(response=json_list, status=200, mimetype="application/json")
        return render_template('recomm.html')
        # return 'ok'
    except:
        print ("here!")
    #     response = json.dumps([])
    #     return Response(response=response, status=200, mimetype="application/json")

if __name__ == '__main__':
    app.run(debug=True)