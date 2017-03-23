from flask import render_template, request
from . import app


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/fixjq')
def fixjq():
    return render_template("fixing_jq.html")

@app.route('/reflect')
def reflect():
    param = request.args.get('p', '')
    return render_template("reflect.html", param=param)


@app.route('/badreflect')
def badreflect():
    param = request.args.get('p', '')
    return render_template("badreflect.html", param=param)


@app.route('/domxss1')
def domxss1():
    return render_template("hashreflect.html")


@app.route('/otherheaders')
def otherheaders():
    return render_template("otherheaders.html", request=request)


@app.route('/demoangular')
def demoangular():
    return render_template("demoangular.html")
