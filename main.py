import os
from bottle import (get, request, route, run, static_file,
                    template, error, response)
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
        browser.append(json.loads(utils.getJsonFromFile(show)))
    sectionData = browser
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData=sectionData)

@route('/ajax/show/<show_number>')
def shows(show_number):
    shows = json.loads(utils.getJsonFromFile(show_number))
    return template("./templates/show.tpl", version=utils.getVersion(), result=shows)

@route('/show/<show_number>')
def shows(show_number):
    sectionTemplate = "./templates/show.tpl"
    shows = json.loads(utils.getJsonFromFile(show_number))
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData=shows)


@route('/show/<show_number>/episode/<episode_number>')
def show(show_number, episode_number):
    sectionTemplate = "./templates/episode.tpl"
    show = json.loads(utils.getJsonFromFile(show_number))
    episodes = show["_embedded"]["episodes"]
    for episode in episodes:
        if str(episode["id"]) == episode_number:
            episode_shown = episode

        else:
            response.status = 404
            sectionTemplate = "./templates/404.tpl"
            return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                            sectionData={})
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData=episode_shown)



@route('/ajax/show/<show_number>/episode/<episode_number>')
def show(show_number, episode_number):
    show = json.loads(utils.getJsonFromFile(show_number))
    episodes = show["_embedded"]["episodes"]
    for episode in episodes:
        if str(episode["id"]) == episode_number:
            result_episode = episode
    return template("./templates/episode.tpl", result=result_episode)


@route('/search')
def search_page():
    sectionTemplate = "./templates/search.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData={})


@route('/search', method="POST")
def search_page():
    sectionTemplate = "./templates/search_result.tpl"
    user_input = request.forms.get("q")
    shows_list = []
    for show in utils.AVAILABE_SHOWS:
        shows_list.append(json.loads(utils.getJsonFromFile(show)))
    show_ep = []
    for show in shows_list:
        for episode in show["_embedded"]["episodes"]:
            ep = {}
            if type(episode['summary']) == str and user_input in episode['summary'] or type(episode['name']) == str and user_input in episode['name']:
                ep["showid"] = show["id"]
                ep['episodeid'] = episode["id"]
                ep['text'] = show['name'] + " : " + episode["name"]
                show_ep.append(ep)
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData={}, results=show_ep, query=user_input)

@error(404)
def error404(error):
    sectionTemplate = "./templates/404.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData={})

run(host='0.0.0.0', port=os.environ.get('PORT', 5000))
