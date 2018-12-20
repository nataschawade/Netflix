import os
from bottle import (get, post, redirect, request, route, run, static_file,
                    template, jinja2_view)
import utils
import json


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
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData={})


@route('/<name>')
def browse(name):
    sectionTemplate = "./templates/"+name+".tpl"
    browser = []
    for show in utils.AVAILABE_SHOWS:
        json_show = utils.getJsonFromFile(show)
        dict_show = json.loads(json_show)
        browser.append(dict_show)
    sectionData = browser
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData=sectionData)
#
# @route('/search')
# def index():
#     sectionTemplate = "./templates/search.tpl"
#     return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData={})
#

# @route('/<name>')
# def index(name):
#     sectionTemplate = "./templates/"+name+".tpl"
#     return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData = {})

@route('/show/<number>')
def shows(number):
    sectionTemplate = "./templates/show.tpl"
    json_show = utils.getJsonFromFile(number)
    shows = json.loads(json_show)
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData=shows)


# @route('/browse')
# @jinja2_view('browse.html', template_lookup=['templates'])
# def test():
#     return {}

# @route('/search')
# def index():
#     sectionTemplate = "./templates/search.tpl"
#     return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData = {})
#
@route('/404')
def index():
    sectionTemplate = "./templates/404.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData={})

run(host='0.0.0.0', port=os.environ.get('PORT', 5000))
