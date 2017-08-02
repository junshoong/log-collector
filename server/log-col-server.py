import os

from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import send_from_directory
from flask import url_for

app = Flask(__name__)
log_path = app.root_path+'/logs'


def save_file(request):
    data = request.get_json()
    prefix = data.pop('prefix')
    for k, v in data.items():
        filename = prefix + k + '.log'
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
        return


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.root_path,'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/images/<path>')
def images(path):
    return redirect(url_for('static', filename='images/'+path))


@app.route('/<filename>')
def viewer(filename):
    log = os.path.join(log_path, filename)
    text = ''
    with open(log, 'rb') as f:
        text = f.read()
    text = text.decode('utf-8')
    text = ''.join(['<p>' + s + '</p>' for s in text.split('\n')])
    return render_template('log.html', text=text)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

