from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import requests
import json

app = Flask(__name__)
app.secret_key = "secret key"
app.config["MONGO_URI"] = "mongodb://localhost:27017/movies"
mongo = PyMongo(app)


@app.route('/movie', methods=['POST','GET'])
def movie():
    comic_id = request.form['comic_id']
    r = requests.get("http://xkcd.com/"+comic_id+"/info.0.json")
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
    return render_template('movie.html', num=num, title=title, img=img, date=date, alt=alt)

@app.route('/save')
@app.route('/save/<num>', methods=['POST','GET'])
def info(num):
    comic_id = num
    r = requests.get("http://xkcd.com/"+comic_id+"/info.0.json")
    json_object = r.json()

    title = json_object['title']
    img = json_object['img']
    alt = json_object['alt']
    day = json_object['day']
    month = json_object['month']
    year = json_object['year']
    num = json_object['num']

    if request.method == 'POST':
        fav = mongo.db.savedComics.insert({'num' : num, 'title': title, 'img' : img, 'day' : day, 'month' : month, 'year' : year})
        resp = 'Comic added to saved list'
        return resp

    #return json_object
    return render_template('info.html', num=num, title=title, img=img, day=day, month=month, year=year, alt=alt)


@app.route('/delete/<id>', methods=['POST'])
def delete_movie(id):
    mongo.db.userMovies.delete_one({'_id': id})
    resp = 'Movie removed successfully!'
    return resp

@app.route('/userFavs',)
def userFavs():
    favMovies = mongo.db.userMovies.find()
    return render_template('userMovies.html', favMovies=favMovies)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/infosearch')
def infosearch():
	return render_template('info-search.html')


@app.route('/watched/<id>', methods=['POST'])
def watched_movie(id):
    mongo.db.userMovies.update({'_id': id}, {"$set": {"watched": "true"}})
    mongo.db.userMovies.find().sort("watched", 1)
    resp = 'Movie set to watched successfully!'
    return userFavs()

@app.route('/unwatched/<id>', methods=['POST'])
def unwatched_movie(id):
    mongo.db.userMovies.update({'_id': id}, {"$set": {"watched": "false"}})
    mongo.db.userMovies.find().sort("watched", 1)
    resp = 'Movie set to watched successfully!'
    return userFavs()



if __name__ == '__main__':
    app.run(debug=True, port=5000, host='127.0.0.1')