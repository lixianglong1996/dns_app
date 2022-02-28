import requests
import socket
import json
from socket import *
from flask import Flask, request, abort

app = Flask(__name__)


def parse_arg(arg):
    hostname = arg.get('hostname')
    ip = arg.get('ip')
    as_ip = arg.get('as_ip')
    as_port = arg.get('as_port')
    return hostname, ip, as_ip, as_port


def register_DNS(hostname, ip, as_ip, as_port):
    client = socket(AF_INET, SOCK_DGRAM)
    data = json.dumps({
        "type": "A",
        "Name": hostname,
        "Value": ip,
        "TTL": 10
    }).encode()
    client.sendto(data, (as_ip, as_port))
    response, _ = client.recvfrom(2048)
    response = int(response.decode())
    return response

@app.route('/')
def hello_world():
    return 'FS'

@app.route('/register', methods=['GET', 'PUT'])
def register():
    hostname, ip, as_ip, as_port = parse_arg(request.args)
    response = register_DNS(hostname, ip, as_ip, int(as_port))
    return "Registration is complete!", response

@app.route('/fibonacci')
def fibonacci():
    number = request.args.get('number')
    try:
        number = int(number)
        return '{}'.format(cal_fibonacci(number)), 200
    except:
        abort(400)


def cal_fibonacci(n):
    a, b = 0, 1
    while n > 0:
        a, b = b, a + b
        n -= 1
    return a


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9090, debug=True)

