from flask import Flask, request, redirect, url_for, make_response, render_template
import pydunext

app=Flask(__name__)

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=="POST":
        print(request.form)
        # user=pydunext.User(request.form['username'],request.form['password'])
        resp=make_response(redirect(url_for('index')))
        resp.set_cookie("username",request.form['username'])
        resp.set_cookie("password",request.form['password'])
        return resp
    else:
        return render_template('login.html')

import time

@app.route('/homeworks')
def homework():
    if request.cookies.get('username')==None:
        return redirect(url_for('login'))
    if 'user'+request.cookies['username'] not in globals():# or time.time() - globals()['user'+request.cookies['username']].retrieved > 10:
        globals()['user'+request.cookies['username']]=pydunext.User(request.cookies['username'],request.cookies['password'])
    return render_template('homeworks.html',homeworks=globals()['user'+request.cookies['username']].hwlist,ids=globals()['user'+request.cookies['username']].hwlist.keys(),photoURL=globals()['user'+request.cookies['username']].photoURL)

@app.route('/circulars')
def circular():
    if request.cookies.get('username')==None:
        return redirect(url_for('login'))
    if 'user'+request.cookies['username'] not in globals():# or time.time() - globals()['user'+request.cookies['username']].retrieved > 10:
        globals()['user'+request.cookies['username']]=pydunext.User(request.cookies['username'],request.cookies['password'])
    return render_template('circulars.html',circulars=globals()['user'+request.cookies['username']].circularlist,ids=globals()['user'+request.cookies['username']].circularlist.keys(),photoURL=globals()['user'+request.cookies['username']].photoURL)


@app.route('/')
def index():
    if request.cookies.get('username')==None:
        return redirect(url_for('login'))
    if 'user'+request.cookies['username'] not in globals():# or time.time() - globals()['user'+request.cookies['username']].retrieved > 10:
        globals()['user'+request.cookies['username']]=pydunext.User(request.cookies['username'],request.cookies['password'])
    # return render_template('index.html')
    return render_template('index.html',homeworks=globals()['user'+request.cookies['username']].hwlist,ids=globals()['user'+request.cookies['username']].hwlist.keys(),photoURL=globals()['user'+request.cookies['username']].photoURL,circulars=globals()['user'+request.cookies['username']].circularlist,circularids=globals()['user'+request.cookies['username']].circularlist.keys())


from flask import jsonify

@app.route('/api/v1/homeworks',methods=["POST"])
def homeworksAPI():
    if request.form['username']==None or request.form['password']==None:
        return jsonify({"error":"Invalid Credentials"})
    if 'user'+request.form['username'] not in globals():# or time.time() - globals()['user'+request.form['username']].retrieved > 10:
        user=pydunext.User(request.form['username'],request.form['password'])
        globals()['user'+request.form['username']]=user
    else:
        user=globals()['user'+request.form['username']]
    return jsonify(user.hwlist)

@app.route('/api/v1/circulars',methods=["POST"])
def circularsAPI():
    if request.form['username']==None or request.form['password']==None:
        return jsonify({"error":"Invalid Credentials"})
    if 'user'+request.form['username'] not in globals():
        user=pydunext.User(request.form['username'],request.form['password'])
        globals()['user'+request.form['username']]=user
    else:
        user=globals()['user'+request.form['username']]
    return jsonify(user.circularlist)

@app.route('/api/v1/homework/<int:id>',methods=["POST"])
def homeworkAPI(id):
    if request.form['username']==None or request.form['password']==None:
        return jsonify({"error":"Invalid Credentials"})
    if 'user'+request.form['username'] not in globals():
        user=pydunext.User(request.form['username'],request.form['password'])
        globals()['user'+request.form['username']]=user
    else:
        user=globals()['user'+request.form['username']]
    return jsonify(user.hwlist[str(id)])

if __name__=="__main__":
    app.run(host='0.0.0.0',port=8000, debug=True)
