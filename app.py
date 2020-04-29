from flask import Flask, render_template, url_for, flash, redirect, request, abort, jsonify, Response, send_file
# from flask_sqlalchemy import SQLAlchemy
import sys
import spacy
import text as pr
import simi as sm
from forms import RegistrationForm, LoginForm
import csv

app = Flask(__name__)

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
        terms = pr.run_parse_resume("./server_files/" + filename)
        # print(terms)
        nlp = spacy.load("en_core_web_lg")
        sim_index = []

        for p in posts:
            # print("ok")
            doc1 = nlp(terms) 
            doc2 = nlp(p['job_description'])
            search_doc2_no_stop_words = nlp(' '.join([str(t) for t in doc2 if not t.is_stop]))
            # print("without ", doc1.similarity(doc2), p['company'])
            # print("with ", doc1.similarity(search_doc2_no_stop_words))
            info = {"company": p['company'], "si": doc1.similarity(search_doc2_no_stop_words)}
            sim_index.append(info)
        print(sorted(sim_index, key = lambda i: i['si']) )
        # for s in sim_index:
        #     print(s)

            # print(p['job_description'])
        #     sm.prDeets(p['job_description'])
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
        # return render_template('recomm.html')
        return 'ok'
    except:
        print ("you done fucked up")
        return 'not ok'
    #     response = json.dumps([])
    #     return Response(response=response, status=200, mimetype="application/json")

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



if __name__ == '__main__':
    app.run(debug=True)