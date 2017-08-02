import os
import time

from flask import Flask
from flask import request
from flask import render_template
from flask import send_from_directory

app = Flask(__name__)
log_path = app.root_path+'/clients'


def save_file(request):
    client_ip = request.remote_addr
    now = time.strftime("%Y%m%dT%H%M%S")
    data = request.get_json()
    for k, v in data.items():
        filename = '-'.join([now, client_ip, k])+'.log'
        with open(os.path.join(log_path, filename), 'wb') as f:
            v = v.encode('utf-8')
            f.write(v)


@app.route('/')
def index():
    files = os.listdir(log_path)
    return render_template('index.html', files=files)
    

@app.route('/collect', methods=['POST'])
def collect():
    if request.method == 'POST':
        save_file(request)
        return 'Collecting!'


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.root_path,'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/<filename>')
def viewer(filename):
    log = os.path.join(log_path, filename)
    text = ''
    with open(log, 'rb') as f:
        text = f.read()
    text = text.decode('utf-8')
    return render_template('log.html', text=text)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

