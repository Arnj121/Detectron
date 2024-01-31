from detector import *
import flask
from search import searchq

app = flask.Flask(__name__)

@app.route('/report')
def report():
	return flask.send_file('static/report.pdf')
@app.route('/')
def homepage():
    return flask.send_file('static/index.html')

@app.route('/static/<path:path>')
def sendstyle(path):
    return flask.send_from_directory('static', path)

@app.route('/inputpic',methods=['POST'])
def inputpic():
    if flask.request.method =="POST":
        l = flask.request.files.to_dict()
        l['file'].save("./static/predictionFiles/{}".format(l['file'].filename))
        ret = performImgDet('./static/predictionFiles/{}'.format(l['file'].filename),l['file'].filename)
        return {"status":200,'time':ret[0],'labels':ret[1],'scores':ret[2],'link':'http://localhost:3033/static/predictionFiles/{}_predicted.jpg'.format('.'.join(l['file'].filename.split('.')[:-1]))}
    else:
        print('invalid method')

@app.route('/inputvid',methods=['POST'])
def inputvid():
    if flask.request.method =="POST":
        l = flask.request.files.to_dict()
        l['file'].save("./static/videos/{}".format(l['file'].filename))
        ret = performVidDet('./static/videos/{}'.format(l['file'].filename),l['file'].filename)
        return {"status":200,'objs':ret}
    else:
        print('invalid method')


@app.route('/detectimg',methods=['GET'])
def detectimg():
    if flask.request.method=='GET':
        l = flask.request.args.to_dict()['filename']
        ret=performImgDet('./static/JPEGImages/{}'.format(l),l)
        return {"status":200,'time':ret[0],'labels':ret[1],'scores':ret[2],'link':'http://localhost:3033/static/predictionFiles/{}_predicted.jpg'.format('.'.join(l.split('.')[:-1]))}

@app.route("/search",methods=['GET'])
def search():
    text = flask.request.args.to_dict()['search']
    res=searchq(text)
    return {'res':200,'results':res}

app.run(host='localhost',port=3033)