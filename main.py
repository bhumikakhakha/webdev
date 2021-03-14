from flask import Flask,render_template,url_for,session,request,flash,redirect
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField
from flask_mail import Mail,Message
from threading import Thread
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisissecret'
app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ.get('MAIL_USERNAME')
app.config["MAIL_PASSWORD"] = os.environ.get('MAIL_PASSWORD')

app.config['MAIL_SUBJECT_PREFIX'] = '[Contact]'
app.config['MAIL_SENDER'] = 'ADMIN <bhumikakhakha1010@gmail.com>'
app.config['ADMIN'] = os.environ.get('ADMIN')

mail = Mail(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)

class User(db.Model):
    __tablename__ = "contact"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(64),nullable=False,index=True)
    email = db.Column(db.String(100),nullable=False,unique=True,index=True)
    subject = db.Column(db.String(200),nullable=True)
    query = db.Column(db.String(500),nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name


    
def send_mail_async(app,msg):
    with app.app_context():
        mail.send(msg)

def send_mail(to,subject,template,**kwargs):
    msg=Message(app.config['MAIL_SUBJECT_PREFIX']+subject,sender=app.config['MAIL_SENDER'],recipients=[to]) 
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_mail_async,args=[app,msg])
    thr.start()
    return thr
    
class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    query = TextAreaField('Query', validators=[DataRequired()])
    submit = SubmitField('Send')

@app.route('/',methods=['GET','POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            subject = form.subject.data
            query = form.query.data
          
            person=User(name=name,email=email,subject=subject,query=query)  
            db.session.add(person)
            db.session.commit()
            if app.config['ADMIN']:
                send_mail(app.config['ADMIN'],'New User', 'mail/new_user',person=person)
            flash('Your Query is posted Successfully!')
            
        
        return redirect(url_for('contact'))

    return render_template('contact.html',form=form,name=session.get('name'))


