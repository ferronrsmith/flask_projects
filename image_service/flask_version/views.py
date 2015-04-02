import sqlite3
from flask import Flask, request, g,render_template,\
    url_for, redirect, flash, abort, jsonify
from utils.utils import *
from flask.globals import current_app
import os

SECRET_KEY = "the global object 'g' needs this"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config.from_object(__name__)
app.jinja_env.filters['timesince'] = timesince

def allowed_file(filename):
    return '.' in filename and\
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# database method, which is triggered
# before each request
def connect_db():
    return sqlite3.connect('./imgshare.db')

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/create', methods=['POST'])
def create():
    file = request.files['image']
    if file and allowed_file(file.filename):
        shorturl = save_image(file)
        flash('New entry was successfully posted')
        return redirect('/'+shorturl)
    return redirect(url_for('index'))

@app.route('/', methods=['GET'])
@app.route('/<shorturl>', methods=['GET'])
def index(shorturl=None):
    error = None
    if shorturl :
        imagedata = get_image_data(shorturl)
        if imagedata :
            return render_template('image.html',imagedata=imagedata)
        else :
            error = 'Image does not exist'
    return render_template('index.html', error=error)


@app.route('/image/<shorturl>', methods=['GET'])
def image(shorturl=None):
    if shorturl :
        row = get_image(shorturl)
        if row :
            return current_app.response_class(row[0], mimetype=row[2], direct_passthrough=False)
        else:
            abort(404)
    return render_template('index.html')


@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.route('/update', methods=['POST'])
def update():
    success = False
    title = request.form['title']
    shorturl = request.form['shorturl']
    if shorturl and title :
        g.db.execute('update image set filename=? where shorturl=?',[title, shorturl])
        g.db.commit()
        success = True
    return jsonify(success=success)

@app.route('/delete/<shorturl>')
def delete(shorturl):
    success = False
    if shorturl :
        g.db.execute('delete from image where shorturl = ?', [shorturl])
        g.db.commit()
        success = True
    return jsonify(success=success)


if __name__ == "__main__":
    app.debug = True
    app.run(port=9000)
