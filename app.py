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

#Displays information for search comic
@app.route('/info', methods=['GET', 'POST'])
def info():
    comic_id = request.form['comic_id']
    r = requests.get("http://xkcd.com/" + comic_id + "/info.0.json")
    json_object = r.json()
    #gets comic info
    title = json_object['title']
    img = json_object['img']
    alt = json_object['alt']
    day = json_object['day']
    month = json_object['month']
    year = json_object['year']
    num = json_object['num']
    date = day+'/'+month+'/'+year

    return render_template('comic_info.html', num=num, title=title, img=img, date=date, alt=alt)

#Gives a random comic id and displays info
@app.route('/random', methods=['POST','GET'])
def random_comic():
    comic_id = str(randint(1,2443))
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

#Saves comic info for specified comic number to mongoDB database
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
        print('Added to Favourites')
        return render_template('index.html')
         
    return render_template('comic_info.html', num=num, title=title, img=img, alt=alt, date=date)

#deletes comic info for specified comic number
@app.route('/delete/<int:num>', methods=['POST'])
def delete_comic(num):
    mongo.db.userComics.delete_one({'num': num})
    return userFavs()

#Lists all enteries in the mongoDB database
@app.route('/userComics')
def userFavs():
    favComics = mongo.db.userComics.find()
    return render_template('userComics.html', favComics=favComics)

@app.route('/')
def index():
    return render_template('index.html')

#Mark comic as read
@app.route('/read/<int:num>', methods=['POST'])
def read(num):
    mongo.db.userComics.update_one({'num': num }, {"$set": {"read": "true"}})
    return userFavs()

#Unmark comic as read
@app.route('/unread/<int:num>', methods=['POST'])
def unread(num):
    mongo.db.userComics.update_one({'num': num}, {"$set": {"read": "false"}})
    return userFavs()

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='127.0.0.1')