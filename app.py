from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import requests
import json
from random import randint

app = Flask(__name__)
app.secret_key = "secret key"
app.config["MONGO_URI"] = "mongodb://localhost:27017/comics"
mongo = PyMongo(app)

@app.route('/info', methods=['POST'])
def info():
    comic_id = request.form['comic_id']
    r = requests.get("http://xkcd.com/" + comic_id + "/info.0.json")
    json_object = r.json()

    title = json_object['title']
    img = json_object['img']
    alt = json_object['alt']
    day = json_object['day']
    month = json_object['month']
    year = json_object['year']
    num = json_object['num']
    date = day+'/'+month+'/'+year

    #return a
    #return str(items)
    return render_template('comic_info.html', num=num, title=title, img=img, date=date, alt=alt)

@app.route('/random', methods=['POST'])
def random_comic():
    comic_id = str(randint(1,2440))
    r = requests.get("http://xkcd.com/" + comic_id + "/info.0.json")
    json_object = r.json()

    title = json_object['title']
    img = json_object['img']
    alt = json_object['alt']
    day = json_object['day']
    month = json_object['month']
    year = json_object['year']
    num = json_object['num']
    date = day+'/'+month+'/'+year

    return render_template('comic_info.html', num=num, title=title, img=img, date=date, alt=alt)


@app.route('/save',defaults={'num': '1'})
@app.route('/save/<num>', methods=['POST','GET'])
def save(num):
    comic_id = num
    r = requests.get("http://xkcd.com/" + comic_id + "/info.0.json")
    json_object = r.json()

    title = json_object['title']
    img = json_object['img']
    alt = json_object['alt']
    day = json_object['day']
    month = json_object['month']
    year = json_object['year']
    num = json_object['num']
    date = day+'/'+month+'/'+year
    read = 'false'


    if request.method == 'POST':
        fav = mongo.db.userComics.insert({'num': num, 'title': title, 'img': img, 'alt': alt, 'day': day, 'month': month, 'year': year, 'date': date, 'read': read})
        resp = 'Added to Favourites'
        return resp 

    #return json_object
    return render_template('comic_info.html', num=num, title=title, img=img, alt=alt, date=date)


@app.route('/delete/<int:num>', methods=['POST'])
def delete_comic(num):
    mongo.db.userComics.delete_one({'num': num})
    return userFavs()

@app.route('/userComics',)
def userFavs():
    favComics = mongo.db.userComics.find()
    return render_template('userComics.html', favComics=favComics)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/read/<int:num>', methods=['POST'])
def read(num):
    mongo.db.userComics.update_one({'num': num }, {"$set": {"read": "true"}})
    resp = 'Comic set to read successfully!'
    return userFavs()
    #return num

#Not Communicating with db

@app.route('/unread/<int:num>', methods=['POST'])
def unread(num):
    mongo.db.userComics.update_one({'num': num}, {"$set": {"read": "false"}})
    resp = 'Comic set to unread successfully!'
    return userFavs()



if __name__ == '__main__':
    app.run(debug=True, port=5000, host='127.0.0.1')