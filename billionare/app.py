from flask import Flask, jsonify, request, render_template, redirect, url_for
from utils.db import db
from models.data import *
from flask_sqlalchemy import SQLAlchemy


flask_app = Flask(__name__)
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'






@flask_app.route('/')
def index():
    data = Business.query.all()
    return render_template('index.html', content=data)



@flask_app.route('/help')
def help():
    return render_template('help.html')

@flask_app.route('/modify')
def modify():
    data = Business.query.all()
    return render_template('modify.html', content2=data)




@flask_app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@flask_app.route('/add_data')
def add_data():
    return render_template('add_data.html')

@flask_app.route('/login')
def login():
    return render_template('login.html')

db.init_app(flask_app)


with flask_app.app_context():
    db.create_all()



@flask_app.route('/submit', methods=['POST'])
def submit():
    form_data = request.form.to_dict()
    print(f"form_data: {form_data}")

    personName = form_data.get('personName')
    age = form_data.get('age')
    gender = form_data.get('gender')
    birthdate = form_data.get('birthdate')
    city = form_data.get('city')
    state = form_data.get('state')
    country = form_data.get('country')




    rank = form_data.get('rank')
    source = form_data.get('source')
    finalWorth = form_data.get('finalWorth')
    category = form_data.get('category')
    organization = form_data.get('organization')
    industries = form_data.get('industries')
    title = form_data.get('title')

    person = Person.query.filter_by(personName=personName).first()
    if not person:
        person = Person(personName=personName, age=age, gender=gender,birthdate=birthdate, city=city,state=state,country=country)
        db.session.add(person)
        db.session.commit()

    data = Business(rank=rank, source=source, finalWorth=finalWorth, category=category,organization=organization, industries=industries, title=title,person_id=person.id)
    db.session.add(data)
    db.session.commit()
    person = Person(personName=personName, age=age, gender=gender, birthdate=birthdate, city=city, state=state,country=country)
    db.session.add(person)
    db.session.commit()

    print("sumitted successfully")
    return redirect('/')


@flask_app.route('/register', methods=['POST'])
def register():
    form_data = request.form.to_dict()
    print(f"form_data: {form_data}")

    name = form_data.get('name')
    mobile_id = form_data.get('mobile_id')
    email_id = form_data.get('email_id')
    password = form_data.get('password')

    login = Login.query.filter_by(name=name).first()
    if not login:
        login = Login(name=name,mobile_id=mobile_id,email_id=email_id, password=password)
        db.session.add(login)
        db.session.commit()


    print("Logined successfully")
    return render_template('/add_data.html')

@flask_app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    data = Business.query.get_or_404(id)
    print(data.person.id)
    if not data:
        return jsonify({'message': 'task not found'}), 404

    if request.method == 'POST':

        data.person.personName = request.form['personName']
        data.person.age = request.form['age']
        data.person.gender = request.form['gender']
        data.person.birthdate = request.form['birthdate']
        data.person.city = request.form['city']
        data.person.state = request.form['state']
        data.person.country = request.form['country']

        data.rank = request.form['rank']
        data.source = request.form['source']
        data.finalWorth = request.form['finalWorth']
        data.category = request.form['category']
        data.organization = request.form['organization']
        data.industries = request.form['industries']
        data.title = request.form['title']

        try:
            db.session.commit()
            return redirect('/modify')

        except Exception as e:
            db.session.rollback()
            return "there is an issue while updating the record"
    return render_template('update.html', data=data)


@flask_app.route('/delete/<int:id>', methods=['GET', 'DELETE'])
def delete(id):
    data = Business.query.get(id)
    print("task: {}".format(data))

    if not data:
        return jsonify({'message': 'task not found'}), 404
    try:
        db.session.delete(data)
        db.session.commit()
        return jsonify({'message': 'task deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while deleting the data {}'.format(e)}), 500


if __name__ == '__main__':
    flask_app.run(
        host='127.0.0.1',
        port=8005,
        debug=True
    )