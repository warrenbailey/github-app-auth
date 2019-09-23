from flask import Flask, request

import logging

app = Flask(__name__)

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


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

    return f"ok {code} {setup_action} {installation_id}"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
