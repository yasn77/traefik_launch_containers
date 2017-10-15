#!/usr/bin/env python

import os
import docker
import json
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    image = 'training/webapp'
    (backend, domain) = (request.host.split('.')[0],
                         '.'.join(request.host.split('.')[1:]))
    print("Launching {}.{}".format(backend, domain))
    labels = {
        "traefik.enable": "true",
        "traefik.docker.network": "traefik_default",
        "traefik.backend": backend,
        "traefik.domain": domain,
        "traefik.frontend.priority": "10",
        "traefik.{}.backend".format(backend): backend,
        "traefik.{}.frontend.rule".format(backend):
            "Host:{}.{};PathPrefix: /".format(backend, domain),
        "traefik.{}.port".format(backend): "5000"
    }
    docker_client = docker.from_env()
    docker_client.containers.run(image,
                                 detach=True,
                                 network='traefik_tst',
                                 labels=labels,
                                 publish_all_ports=True)
    return render_template('index.j2',
                           appurl="http://{}.{}".format(backend, domain))


@app.route("/status/<backend>")
def app_status(backend):
    docker_client = docker.from_env()
    filter = {'label': 'traefik.backend={}'.format(backend)}
    try:
        container = docker_client.containers.list(all=False, filters=filter)[0]
        status = container.status
    except IndexError:
        status = 'down'
    return jsonify({backend: status})


def entrypoint():
    from wsgiserver import WSGIServer
    port = int(os.environ.get("PORT", 8081))
    server = WSGIServer(app, host='127.0.0.1', port=port)
    server.start()


if __name__ == '__main__':
    entrypoint()
