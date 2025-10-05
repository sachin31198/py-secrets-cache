from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from wtforms import Form, BooleanField, PasswordField, StringField, validators
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, AnyOf

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/sachin/Desktop/website/mydb.db'

app.config['SECRET_KEY']='flaskrocks'
db = SQLAlchemy(app)

class registrants(FlaskForm):
	email = StringField('email', validators=[InputRequired('A email is required!')],render_kw={"placeholder": "email"})
	password = PasswordField('password', validators=[InputRequired('A password is required!')],render_kw={"placeholder": "password"})

class names(db.Model):
	__tablename__ = 'signedusers'
	id = db.Column(Integer, primary_key=True)
	email = db.Column(db.String(100))
	password = db.Column(db.String(100))
	name = db.Column(db.String(100))
	dob = db.Column(db.String(100))
	def __init__(self,email,password,name,dob):
		self.email = email
		self.password = password
		self.name = name
		self.dob =dob 

@app.route('/<username>')
def index(username):
	return 'hello %s'% username

@app.route('/test')
def test():
	return render_template('signup.html')

@app.route('/signup', methods=['GET','POST'])
def form():
	if request.method =='POST':
		if not request.form['email'] or not request.form['password']:
			registered = names.query.all()
			return render_template('request.html', registered = registered)
		else:
			entry = names(request.form['email'],request.form['password'],request.form['name'],request.form['dob'])
			db.session.add(entry)
			db.session.commit()
			return redirect(url_for('login'))
	return render_template("signup.html")

@app.route('/login', methods=['GET','POST'])
def login():
	form=registrants()
	if form.validate_on_submit():
		user_log = names.query.filter_by(email=form.email.data).first()
		if form.password.data == user_log.password: 
			return render_template('dashboard.html',name = form.email.data)
	return render_template('login.html',form=form) 

if __name__ == '__main__':
    app.run(debug=True)
