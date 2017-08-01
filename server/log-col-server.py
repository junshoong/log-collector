from flask import Flask
from flask import request
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
            f.write(v)


@app.route('/')
def hello_world():
    clients = os.listdir(log_path)
    
    return '\n'.join(clients)
    


@app.route('/collect', methods=['POST'])
def collect():
    print(request)
    if request.method == 'POST':
        save_file(request)
        return 'Collecting!'


@app.route('/<ip>')
def view(ip):
    files = os.listdir(os.path.join(log_path, ip))

    return '\n'.join(files)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)


