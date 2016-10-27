#special extentions can be uploaded
#MySQL seperate to another file`

import os,zipfile
from flask import Flask, request, redirect, url_for,render_template,send_from_directory,session,flash,escape
from werkzeug import secure_filename
from functools import wraps
import  MySQLdb
from db import ctfnu,ue,anu,uli,db
from os.path import join,getsize
from shutil import copyfile


UPLOAD_FOLDER = '/home/h/uploads/'
ALLOWED_EXTENSIONS = set(['txt','html', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.debug = False
app.debug = True
app.secret_key = 'H'
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 *1024
usermaxspace = 200 * 1024 *1024

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
	else :
	    flash('you need to login first.')
	    return redirect(url_for('login'))
    return wrap


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def sendzip(download_file):
    os.chdir(session['currentpath'])
    z = zipfile.ZipFile('package.zip','w',zipfile.ZIP_DEFLATED)
    for f in download_file:
        z.write(f)
    z.close()

def deletefile(delete_file):
    os.chdir(session['currentpath'])
    for f in delete_file:
        if os.path.isdir(session['currentpath'] + f):
            os.rmdir(session['currentpath'] + f)
        else:
            os.remove(f)


def getdirsize(dir):  
    size = 0L  
    for root, dirs, files in os.walk(dir):  
        size += sum([getsize(join(root, name)) for name in files])  
    return size  

def get_size(fobj):
    pos = fobj.tell()
    fobj.seek(0,2)
    size = fobj.tell()
    fobj.seek(pos)
    return size



@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    os.chdir(session['currentpath'])
    session['userspace'] = getdirsize( app.config['UPLOAD_FOLDER'] + session['username'] +'/')
    space = ("{:10.2f}".format(session['userspace']/1024.00/1024.00)) +'MB'
    if os.path.exists(session['currentpath']+'package.zip'):
        os.remove('package.zip')
    if request.method == 'POST':
        print request.files.getlist('file') 
        get_files = request.form.getlist("multiplefiles")
        if request.files.getlist('file'):
            filelist = request.files.getlist('file')
            if filelist :#and allowed_file(file.filename):  			#if file: can upload anything
                for file in filelist:
                    if (get_size(file) + session['userspace']) > usermaxspace:#100 * 1024 *1024: 
                        flash('your space is full!')
                        return redirect(url_for('upload_file'))
                    filename = secure_filename(file.filename)
                    file.save(session['currentpath']+filename)
                    session['userspace'] = getdirsize( app.config['UPLOAD_FOLDER'] + session['username'] +'/')
                    print os.path.join(app.config['UPLOAD_FOLDER']+session['username'],filename)
	        return redirect(url_for('upload_file'))
        if request.form['submit'] == 'Download':
            if get_files:
                sendzip(get_files)
                return send_from_directory(session['currentpath'],'package.zip',as_attachment=True)            
            else :
                return render_template('upload.html',files=os.listdir(session['currentpath']),space = space)

        if request.form['submit'] == 'Delete': 
            deletefile(get_files)
            session['userspace'] = getdirsize( app.config['UPLOAD_FOLDER'] + session['username'] +'/')
            space = ("{:10.2f}".format(session['userspace']/1024.00/1024.00)) +'MB'           
            return render_template('upload.html',files=os.listdir(session['currentpath']),space=space) 

#        if request.files.getlist('file'):
#            filelist = request.files.getlist('file')
#            if filelist :#and allowed_file(file.filename):  			#if file: can upload anything
#                for file in filelist:
#                    filename = secure_filename(file.filename)
#                    file.save(session['currentpath']+filename)
#                    print os.path.join(app.config['UPLOAD_FOLDER']+session['username'],filename)
#	        return redirect(url_for('upload_file'))
    #test username admin
    if session['username'] == 'admin':
        return render_template('upload.html',files=os.listdir(app.config['UPLOAD_FOLDER']))
    return render_template('upload.html',files=os.listdir(session['currentpath']),space = space)


@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    if os.path.isdir(session['currentpath']+filename):
        session['currentpath'] += filename + '/'
        return redirect(url_for('upload_file'))
    else:
        return send_from_directory(session['currentpath'],filename,as_attachment=True)


@app.route('/downloadmultiple',methods=['GET','POST'])
def downloadmultiple():
    if request.method == 'POST':
        print "11111111"
        print request.form.getlist['multiplefiles']


@app.route('/preview')
@login_required
def preview():
    str = session['currentpath']
    a = str.split('/')
    if a[-3] == 'uploads':
        flash('Already in top directory!')
        return render_template('upload.html',files=os.listdir(session['currentpath']))
    else:
        session['currentpath'] = '/'.join(a[0:-2])+'/'
        return render_template('upload.html',files=os.listdir(session['currentpath']))


@app.route('/newfolder',methods=['GET','POST'])
@login_required
def newfolder():
    if request.method == 'POST':
        if len(request.form['newfolder']) > 6:
            error = "foldername is too long!"
            return render_template('newfolder.html',error = error)
        if os.path.isdir(request.form['newfolder']):
            error = "folder is exists"
            return render_template('newfolder.html',error = error)
        if request.form['newfolder']:
            os.mkdir(session['currentpath']+request.form['newfolder'])
        return redirect(url_for('upload_file'))
    return render_template('newfolder.html')


@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if len(request.form['username']) > 8:
            error = "username is too long!"
            return render_template('login.html',error=error)  

        if uli(request.form['username'],request.form['passwd']):
        	session['logged_in'] = True
                session['username'] = request.form['username']
                #test user admin
                if session['username'] == 'admin':
                    session['currentpath'] = UPLOAD_FOLDER
                else:
                    session['currentpath'] = UPLOAD_FOLDER+session['username']+'/'
                    session['userspace'] = getdirsize(session['currentpath'])
                    print session['userspace']
        	return redirect(url_for('upload_file'))
        else:
	    error = 'Invalid credentials, Please try again!'
    return render_template('login.html', error = error)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in',None)
    flash('You were just logged out!')
    return render_template('bye.html')


@app.route('/register',methods=['GET','POST'])
def register():
    if request.method =='POST':
        if len(request.form['username']) > 8:
            error = "username is too long!"
            return render_template('register.html',error=error)
        if len(request.form['username']) < 3:
            error = "username was too short!"
            return render_template('register.html',error=error)

        if ue(request.form['username']) == True:
            error = "username was uesd!"
            return render_template('register.html',error=error)

        anu(request.form['username'],request.form['passwd'],UPLOAD_FOLDER+request.form['username']+'/')
        flash('You were just register!')
        os.mkdir(UPLOAD_FOLDER+request.form['username'])
        return redirect(url_for('login'))
    return render_template('register.html')

@app.errorhandler(413)
def error413(e):
        return render_template('413.html'), 413


if __name__ == '__main__':
	app.run(host='0.0.0.0')
        db.close()

