import os

from flask import (
    Flask,
    request,
    render_template,
    redirect,
    send_from_directory,
    url_for
)

app = Flask(__name__)
LOG_PATH = app.root_path+'/logs'


def save_file(request):
    data = request.get_json()
    prefix = data.pop('prefix')
    for k, v in data.items():
        filename = prefix + k + '.log'
        with open(os.path.join(LOG_PATH, filename), 'wb') as f:
            v = v.encode('utf-8')
            f.write(v)


@app.route('/')
def index():
    files = os.listdir(LOG_PATH)
    return render_template('index.html', files=files)
    

@app.route('/collect', methods=['POST'])
def collect():
    if request.method == 'POST':
        save_file(request)
        return 'Collecting!'


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.root_path,'static/favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/images/<path>')
def images(path):
    return redirect(url_for('static', filename='images/'+path))


@app.route('/<filename>')
def viewer(filename):
    log = os.path.join(LOG_PATH, filename)
    text = ''
    with open(log, 'rb') as f:
        text = f.read()
    text = text.decode('utf-8')

    if 'sar' in filename:
        text = '<pre class="sar">'+text+'</pre>'
        return render_template('sar.html', text=text)

    elif 'httpd_access' in filename:
        text = ''.join(['<p>' + s + '</p>' for s in text.split('\n')])
        return render_template('httpd_access.html', text=text)


    text = ''.join(['<p>' + s + '</p>' for s in text.split('\n')])
    return render_template('log.html', text=text)


@app.route('/download')
def download():
    f = request.args.get('f')
    if f in ['selog.service', 'selog-client.py', 'selog.sh']:
        return send_from_directory(os.path.join(app.root_path,'client'), f,
                as_attachment=True, mimetype='text/plain')
    return send_from_directory(LOG_PATH, f, as_attachment=True, mimetype='text/plain')
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

