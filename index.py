from flask import Flask, request, redirect, url_for, make_response, render_template
import pydunext
import requests

app=Flask(__name__)

baseurl = "api.kedunext.stiblook.rocks"
protocol = "https"

import time

class User:
    def __init__(self, username, password,request="all"):
        self.username = username
        self.password = password
        if request=="all":
            self.update()
        if request=="hw":
            self.hwlist = requests.post(f"{protocol}://{baseurl}/api/v1/homeworks", data={"username": username, "password": password}).json()
        if request=="circular":
            self.circularlist = requests.post(f"{protocol}://{baseurl}/api/v1/circulars", data={"username": username, "password": password}).json()
        self.photoURL = requests.post(f"{protocol}://{baseurl}/api/v1/photo", data={"username": username, "password": password}).text
    def update(self):
        self.hwlist = requests.post(f"{protocol}://{baseurl}/api/v1/homeworks", data={"username": self.username, "password": self.password}).json()
        self.circularlist = requests.post(f"{protocol}://{baseurl}/api/v1/circulars", data={"username": self.username, "password": self.password}).json()
        self.photoURL = requests.post(f"{protocol}://{baseurl}/api/v1/photo", data={"username": self.username, "password": self.password}).text
        self.retrieved = time.time()

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=="POST":
        # print(request.form)
        # user=pydunext.User(request.form['username'],request.form['password'])
        resp=make_response(redirect(url_for('index')))
        resp.set_cookie("username",request.form['username'])
        resp.set_cookie("password",request.form['password'])
        return resp
    else:
        return render_template('login.html')

@app.route('/homeworks')
def homework():
    if request.cookies.get('username')==None:
        return redirect(url_for('login'))
    # if 'user'+request.cookies['username'] not in globals():# or time.time() - globals()['user'+request.cookies['username']].retrieved > 10:
        # globals()['user'+request.cookies['username']]=(request.cookies['username'],request.cookies['password'])
    user=User(request.cookies['username'],request.cookies['password'],"hw")
    print(sorted(user.hwlist.keys(),reverse=True))
    return render_template('homeworks.html',homeworks=user.hwlist,ids=sorted(user.hwlist.keys(),reverse=True),photoURL=user.photoURL)
    # return render_template('homeworks.html',homeworks=globals()['user'+request.cookies['username']].hwlist,ids=globals()['user'+request.cookies['username']].hwlist.keys(),photoURL=globals()['user'+request.cookies['username']].photoURL)

@app.route('/circulars')
def circular():
    if request.cookies.get('username')==None:
        return redirect(url_for('login'))
    # if 'user'+request.cookies['username'] not in globals():# or time.time() - globals()['user'+request.cookies['username']].retrieved > 10:
    #     globals()['user'+request.cookies['username']]=pydunext.User(request.cookies['username'],request.cookies['password'])
    user=User(request.cookies['username'],request.cookies['password'],"circular")
    return render_template('circulars.html',circulars=user.circularlist,ids=reversed(sorted(user.circularlist.keys())),photoURL=user.photoURL)
    # return render_template('circulars.html',circulars=globals()['user'+request.cookies['username']].circularlist,ids=globals()['user'+request.cookies['username']].circularlist.keys(),photoURL=globals()['user'+request.cookies['username']].photoURL)


@app.route('/')
def index():
    if request.cookies.get('username')==None:
        return redirect(url_for('login'))
    # if 'user'+request.cookies['username'] not in globals():# or time.time() - globals()['user'+request.cookies['username']].retrieved > 10:
    #     globals()['user'+request.cookies['username']]=pydunext.User(request.cookies['username'],request.cookies['password'])
    user=User(request.cookies['username'],request.cookies['password'])
    return render_template('index.html',homeworks=user.hwlist,ids=reversed(sorted(user.hwlist.keys())),photoURL=user.photoURL,circulars=user.circularlist,circularids=reversed(sorted(user.circularlist.keys())))
    # return render_template('index.html',homeworks=globals()['user'+request.cookies['username']].hwlist,ids=globals()['user'+request.cookies['username']].hwlist.keys(),photoURL=globals()['user'+request.cookies['username']].photoURL,circulars=globals()['user'+request.cookies['username']].circularlist,circularids=globals()['user'+request.cookies['username']].circularlist.keys())

if __name__=="__main__":
    app.run(host='0.0.0.0',port=8000, debug=True)
