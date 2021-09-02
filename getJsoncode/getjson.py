import flask
import requests
import yaml
import jsonify
import json
app = flask.Flask(__name__)
app.config["DEBUG"] = True

a = {'Status':'I am healthy' }
python2json = json.dumps(a)
@app.route('/health', methods=['GET'])
def health():
    return "Healthy"

@app.route("/getStatus", methods=["GET"])
def starting_url():
    mystatus = "Healthy"
    return python2json 

app.run(host="0.0.0.0", port=8080)

@app.route('/data', methods=['GET'])
def getData():
    response = requests.get(cfg["url"]["prefix"] + "://" + cfg["url"]["host"] + ":" + cfg["url"]["port"] + "/" + cfg["url"]["path"])
    print(response.content)
    return response.content

app.run(host='0.0.0.0')
