from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from featureform import FeatureForm
import json
import os
import psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://obqhdeahjywmdj:af3c67ca9d03275979ffed391da4ec7f6a5653e58c4c08101a99b0b335bcb0d1@ec2-50-19-114-27.compute-1.amazonaws.com:5432/d13bal0e4lg27'
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class ProductArea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    productArea = db.Column(db.String(20), nullable=False)


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clientName = db.Column(db.String(20), nullable=False)


class Feature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    targetDate = db.Column(db.Date, nullable=False)
    productArea_id = db.Column(db.Integer, db.ForeignKey('product_area.id'), nullable=False)
    __table_args__ = (db.UniqueConstraint('client_id', 'priority', name='_client_id_uc'),)

db.create_all()
db.session.commit()

@app.route("/index", methods=['POST'])
def index():
    formData = json.loads(request.data)
    if request.method == 'POST':
        our_user = db.session.query(Feature).filter(Feature.client_id == int(formData.get("selectClient")), Feature.priority == int(formData.get("clientPriority"))).first()
        if our_user:
            r_user = db.session.query(Feature).order_by('-priority')\
                                .filter(Feature.priority > int(formData.get("clientPriority")))
            for i in r_user:
                i.priority += 1
                db.session.commit()
            our_user.priority += 1
            db.session.commit()
        request_record = Feature(
            title=formData.get("title"),
            description=formData.get("description"),
            client_id=formData.get("selectClient"),
            priority=formData.get("clientPriority"),
            targetDate=formData.get("targetDate"),
            productArea_id=formData.get("productArea")
        )
        db.session.add(request_record)
        db.session.commit()

    return jsonify(success=True, message="Your data has been saved successfully")


@app.route("/index", methods=['GET'])
def formView():
    form = FeatureForm(request.form)
    cl = Client.query.all()
    pa = ProductArea.query.all()
    return render_template('index.html', form=form, cl=cl, pa=pa)


@app.route("/", methods=['GET', 'POST'])
def home():
    f = Feature.query.all()
    ab = db.session.query(Client)
    return render_template('home.html', f=f, ab=ab, Client=Client)
