from flask import Flask
from flask import request
from flask import render_template
import os
app = Flask(__name__)
log_path = app.root_path+'/clients'

def save_file(request):
    client_ip = request.remote_addr
    full_path = os.path.join(log_path,client_ip)
    data = request.get_json()
    if not os.path.isdir(full_path):
        os.mkdir(full_path)
    for k, v in data.items():
        with open(full_path +'/'+k+'.log', 'wb') as f:
            print(k, v)
            v = v.encode('utf-8')
            f.write(v)


@app.route('/')
def index():
    clients = os.listdir(log_path)
    return render_template('index.html', clients=clients)
    


@app.route('/collect', methods=['POST'])
def collect():
    print(request)
    if request.method == 'POST':
        save_file(request)
        return 'Collecting!'


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
    print(text)

    return render_template('log.html', text=text)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)


