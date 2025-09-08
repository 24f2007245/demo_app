from flask import Flask,render_template, request, redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
db = SQLAlchemy()
db.init_app(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'chhotukumar99450@gmail.com'
app.config['MAIL_PASSWORD'] = 'xakb qeot jejb rqsy'  
app.config['MAIL_DEFAULT_SENDER'] = 'chhotukumar99450@gmail.com'

mail = Mail(app)

class UserData(db.Model):
    __tablename__='user_data'
    id = db.Column(db.Integer(), primary_key =True, autoincrement=True)
    user_name = db.Column(db.String(60), nullable =False)
    user_email = db.Column(db.String(130), nullable=False)
    message= db.Column(db.String(1000))

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/sampark", methods=["GET","POST"])
def contact():
    if request.method == 'POST':
        user_name= request.form.get('name')
        user_email= request.form.get('email')
        message= request.form.get('message')
        if not message:
           
            return render_template('sampark.html')
        
        # Create an instance of UserData
        new_user = UserData(user_name=user_name, user_email=user_email, message=message)
        db.session.add(new_user)
        db.session.commit()

         # Send email using Flask-Mail
        msg = Message(
            subject="New Contact Form Submission",
            recipients=[user_email],  # Who receives the email
            body=f"""
We received Your information :

Name: {user_name}
Email: {user_email}
Message:
{message}

Thank You for Contacting Us.
"""
        )
        try:
            mail.send(msg)
        except Exception as e:
            print("Error sending email:", e)

        return redirect(url_for('index'))
    return render_template('sampark.html')

if __name__ == '__main__':
    app.run(debug=True)




    

    


