from email.parser import Parser
import traceback
from unicodedata import name
from flask import Flask, redirect, render_template, request, url_for
from user.form import RegistrationForm
from user.model import User, db
import os
from flask_mail import Mail, Message
import smtplib
import os


app = Flask(__name__)

app.config['SECRET_KEY'] = 'your secret key'

# Setting up Database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Setting up mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)


def send_email(name, recipients):
    msg = Message('Thank you for registering with us!', sender=os.environ.get('EMAIL_USERNAME'), recipients=[recipients])
    msg.html = render_template("email.html", name = name)
    mail.send(msg)

def init_db():
    db.init_app(app)
    db.app = app
    db.create_all()

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/dashboard/")
def dashboard():
    # query DB
    users = User.query.order_by(User.created_at)
    count = User.query.count()
    return render_template("dashboard.html", users=users, count=count)


@app.route("/register/", methods=['GET', 'POST'])
def register():
    registration_form = RegistrationForm(request.form)
    if request.method == "POST" and registration_form.validate_on_submit():
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]

        # Create new user
        user = User(fullname=name, email=email, phone=phone)
        errorMessage = ""

        # push to DB
        try:
            db.session.add(user)
            db.session.commit()

            # Send mail
            send_email(name, email)
            
        except smtplib.SMTPException as e:
            print("SMTP exception")
            errorMessage = 'Error in sending email notification!'
            print(traceback.format_exc())
        
        except Exception as e:
            print("Inexception")
            print(traceback.format_exc())
            errorMessage = 'Error in registering the details!'
        finally:
            return render_template("form.html", form=registration_form, errorMessage=errorMessage)
    else:
        return render_template("form.html", form=registration_form)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)