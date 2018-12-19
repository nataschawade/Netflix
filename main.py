import os
from bottle import (get, post, redirect, request, route, run, static_file,
                    template, jinja2_view)
import utils

# Static Routes

@get("/js/<filepath:re:.*\.js>")
def js(filepath):
    return static_file(filepath, root="./js")

@get("/css/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root="./css")

@get("/images/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filepath):
    return static_file(filepath, root="./images")

@route('/')
def index():
    sectionTemplate = "./templates/home.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData = {})

@route('/<name>')
def index(name):
    sectionTemplate = "./templates/"+name+".tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData = {})
#
@route('/show/305')
def index():
    sectionTemplate = "./templates/show.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData = {})

# @route('/search')
# def index():
#     sectionTemplate = "./templates/search.tpl"
#     return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData = {})
#
# @route('/404')
# def index():
#     sectionTemplate = "./templates/404.tpl"
#     return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData = {})

#episode
#search_result
#show

run(host='0.0.0.0', port=os.environ.get('PORT', 5000))
