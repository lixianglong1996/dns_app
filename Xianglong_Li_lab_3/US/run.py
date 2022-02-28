import requests
import socket
import json
from socket import *
from flask import Flask, request, abort

app = Flask(__name__)


def parse_arg(arg):
    hostname = arg.get('hostname')
    fs_port = arg.get('fs_port')
    number = arg.get('number')
    as_ip = arg.get('as_ip')
    as_port = arg.get('as_port')
    return hostname, fs_port, number, as_ip, as_port


def query_fs_ip(hostname, as_ip, as_port):
    client = socket(AF_INET, SOCK_DGRAM)
    data = json.dumps({"Type": "A", "Name": hostname}).encode()
    client.sendto(data, (as_ip, as_port))
    response, _ = client.recvfrom(2048)
    response = json.loads(response.decode())
    fs_ip = response.get('Value')
    return fs_ip


def get_result(fs_ip, fs_port, number):
    url = "http://{}:{}/fibonacci?number={}".format(fs_ip, fs_port, number)
    response = requests.get(url).text
    return response

@app.route('/')
def hello_world():
    return 'US'

@app.route('/fibonacci')
def fibonacci():
    hostname, fs_port, number, as_ip, as_port = parse_arg(request.args)
    if (hostname is None) or (fs_port is None) or (number is None) or (as_ip is None) or (as_port is None):
        abort(400)
    else:
        fs_ip = query_fs_ip(hostname, as_ip, int(as_port))
        result = get_result(fs_ip, fs_port, number)
        return result

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
