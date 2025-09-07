from flask import Flask,render_template, request, redirect,url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
db = SQLAlchemy()
db.init_app(app)

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
            print(request.form.get('message'))
            return render_template('sampark.html')
        
        # Create an instance of UserData
        new_user = UserData(user_name=user_name, user_email=user_email, message=message)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('sampark.html')

if __name__ == '__main__':
    app.run(debug=True)