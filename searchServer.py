import flask
from search import searchq

app = flask.Flask(__name__)


@app.route('/static/<path:path>')
def sendstyle(path):
    return flask.send_from_directory('static', path)

@app.route("/search",methods=['GET'])
def search():
    text = flask.request.args.to_dict()['search']
    res=searchq(text)
    return {'res':200,'results':res}

app.run(host='localhost',port=3034)
