import os, git, tempfile, json, logging

from flask import Flask, send_file, request
from forms import CompileForm
from flask_cors import CORS

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
CORS(app)

@app.route('/api', methods=['POST'])
def api():
    form = CompileForm()

    # codefile = tempfile.NamedTemporaryFile(suffix='.zip').name
    # codefilepath = os.path.join(codefile)
    codefilepath = '/uploads/archive.zip'
    
    # link z githuba
    if 'file' not in request.files:
        codedir = tempfile.mkdtemp()
        codedirpath = os.path.join(codedir)

        if form.branch.data != "":
            repo = git.Repo.clone_from(
                form.link.data, 
                branch=form.branch.data, 
                to_path=codedirpath
            )
            
        else:
            repo = git.Repo.clone_from(
                form.link.data, 
                to_path=codedirpath
            )

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

    # compile
    return json.dumps({
        'id':'1ABCDEFGHI', 
        'logs':'example-logs',
        'expires':10000
    })

@app.route('/artifact', methods=['GET'])
def artifact():
    id = request.args.get('id')
    if id == '1ABCDEFGHI':
        return send_file('/uploads/archive.zip')


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)-8s %(message)s'
    )

    app.run(host="0.0.0.0", debug=True, port=80)
    
