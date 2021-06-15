import os, git, tempfile, json, string, random, time, requests, msgpack

from flask import flash, Flask, send_file, request, render_template
from forms import CompileForm
from werkzeug.utils import redirect, secure_filename

import logging
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__, static_url_path='')
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

artifacts = {}
api = os.environ['API']

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@app.route("/")
def main():
    comp = '/compile'
    down = '/download'
    return render_template('index.html', compile=comp, download=down)

@app.route('/compile', methods=['POST'])
def compile():
    logging.info("TEST")
    form = CompileForm()

    codefile = tempfile.NamedTemporaryFile(suffix='.zip').name
    codefilepath = os.path.join(codefile)
    
    # link z githuba
    if 'file' not in request.files:
        codedir = tempfile.mkdtemp()
        codedirpath = os.path.join(codedir)

        repo = git.Repo.clone_from(form.link.data, to_path=codedirpath)

        with open(codefilepath, 'wb') as zipfile: 
            repo.archive(zipfile, format='zip')
    
    else:
        file = request.files['file']

        # ani plik ani link
        if file.filename == '':
            return 'No file/link has been provided.'

        # plik
        else:
            file.save(codefilepath)

    compile
    with open(codefilepath, 'rb') as to_compile:
        data = msgpack.packb({'zip': to_compile.read()})
        response = requests.post(
            api, 
            data=data,
            headers={'Content-Type': 'application/octet-stream'}
        )
        response_data = msgpack.unpackb(response.content)
        logging.info("RESPONSE:")
        logging.info(response_data)
        if response_data['success'] == True:
            id = id_generator()
            path = '/uploads/' + id + '.zip'

            artifact = response_data['artifact']
            artifact.save(path)

            global artifacts
            artifacts[id] = path

            return json.dumps({
                'success': True,
                'logs' : response_data['logs'],
                'expires': 5000,
                'id': id
            })

        else:
            return json.dumps({
                'success': False,
                'logs' : response_data['logs']
            })
      

@app.route('/download', methods=['GET'])
def download():
    id = request.args.get('id')
    global artifacts
    zip = artifacts[id]
    if zip:
        return send_file(zip)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)-8s %(message)s'
    )
    
    app.run(host="0.0.0.0", debug=True, port=80)
    
