SECRET = 'ABCDEFGH' ## change this to an arbitrary random string to conceal the submissions page (if you want)
DATABASE = 'data/data.db'

from flask import Flask,redirect,request,make_response,render_template
import sqlite3, os, time, urllib, hashlib

if not os.path.exists(DATABASE):
	print "creating new db..."
	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()
	c.execute('CREATE TABLE programs (hash text, team text, problem text, code text, ts int, resubmit boolean, architects text)')
	conn.commit()
	conn.close()

app = Flask(__name__)

@app.route('/')
def homepage():
	return render_template('main.html',team=request.args.get('t',''))

@app.route('/submit',methods=['POST'])
def submit():
	print request.form
	team = request.form.get('team_name','_error_')
	problem = request.form.get('problem_name','_error_')
	program = request.form.get('code','_error_')
	resub = request.form.get('resubmit','_error_') == 'on'
	arch = request.form.get('architects','_error_')
	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()
	c.execute('INSERT INTO programs VALUES (?,?,?,?,?,?,?)',(hashlib.md5(team+problem+program).hexdigest(),team,problem,program,time.time(),resub,arch))
	conn.commit()
	conn.close()
	return redirect('/?t={}'.format(urllib.quote(team)),302)

@app.route('/view/'+SECRET+'/<cs>')
def view(cs):
	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()
	c.execute('SELECT * FROM programs WHERE hash=?',(cs,))
	i = c.fetchone()
	conn.close()
	a = {'hash':i[0],'team':i[1],'problem':i[2],'time':time.strftime('%I:%M:%S %p',time.gmtime(i[4])),'code':i[3],'resub':i[5],'arch':i[6]}
	return render_template('view.html',row=a)

@app.route('/view/'+SECRET)
def submissions():
	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()
	c.execute('SELECT * FROM programs ORDER BY ts DESC') # most recent first?
	table = []
	for i in c.fetchall():
		table.append({'hash':i[0],'team':i[1],'problem':i[2],'time':time.strftime('%I:%M:%S %p',time.gmtime(i[4])),'resub':i[5],'arch':i[6]})
	conn.close()
	return render_template('submissions.html',table=table,root='/view/'+SECRET+'/')

if __name__ == '__main__':
	app.debug=True
	print 'Submission list can be viewed at /view/{}'.format(SECRET)
	app.run(host='0.0.0.0',port=5000)
