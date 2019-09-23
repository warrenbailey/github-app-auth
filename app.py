from flask import Flask, request
import requests
import logging
from kubernetes import client, config
import base64


app = Flask(__name__)

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_client_id_secret():
    config.load_incluster_config()
    v1 = client.CoreV1Api()
    sec = str(v1.read_namespaced_secret("github-app", "jx-staging").data)

    v1_secret = v1.read_namespaced_secret("github-app", "jx-staging")
    logger.info(f"secret {v1_secret}")
    data = v1_secret.data
    logger.info(f"data {data}")
    c_id = base64.b64decode(data['client_id'])
    c_secret = base64.b64decode(data['client_secret'])
    logger.info(f"client_id {c_id}, client_secret {c_secret}")
    return c_id, c_secret



@app.route('/')
def hello_world():
    return 'Hello from Jenkins X deploy!'


@app.route("/callback")
def callback():
    logger.info("callback called")
    logger.info(f"request {request}")

    code = request.args['code']
    setup_action = request.args['setup_action']
    installation_id = request.args['installation_id']

    logger.info(f"code {code}, setup_action {setup_action}, installation_id {installation_id}")

    client_id, client_secret = get_client_id_secret()

    payload = {'code': code, 'client_id': client_id, 'client_secret': client_secret, 'state': 'octonauts', 'redirect_uri' : 'http://jenkins-x.io'}

    r = requests.post("https://github.com/login/oauth/access_token", data=payload)

    logger.info(r.text)

    return f"ok {code} {setup_action} {installation_id}"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
