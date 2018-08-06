from flask import Flask, render_template, request, jsonify, redirect, session, abort, flash, Markup
import Pins, os, signal

app = Flask(__name__, static_url_path='/static')#setting 

# return index page when IP address of RPi is typed in the browser
@app.route("/")
def home():
        if not session.get('logged_in'):
                return render_template("login.html")
        else:
                name=request.form['username']
                return render_template("home.html",name=name)

@app.route("/home")
def homeret():
        if not session.get('logged_in'):
                return render_template("login.html")
        else:
                name="ret" # Sending 'ret' to indicate returning user
                return render_template("home.html",name=name)

#return the statistics page when asked for it
@app.route("/stats")
def stats():
        if not session.get('logged_in'):
                return render_template("login.html")
        else:
                tot,last = Pins.retStat()
                return render_template("statistics.html",tot=tot,last=last)

#checks the password
@app.route("/login", methods=['POST'])
def do_admin_login():
        if request.form['password'] == 'password':
                session['logged_in'] = True
        else:
                flash('Given Wrong Password, You have.')
        return home()

@app.route("/logout")
def logout():
        session['logged_in'] = False
        return home()   

# ajax GET call this function to set led state
# depeding on the GET parameter sent
@app.route("/_led")
def _led():
        state = request.args.get('state')
        iid = request.args.get('iid')
        if state=="true":
                Pins.LEDon(iid)
        elif state=="false":    
                Pins.LEDoff(iid)
        else:
                print "Error in state"
        return ""

# ajax GET call this function periodically to read button state
# the state is sent back as json data
@app.route("/_button")
def _button():
        iid = request.args.get('iid')
        if Pins.ReadButton(iid):
                  state = 1
        else:
                state = 0
        return jsonify(buttonState=state)
   
# run the webserver on standard port 80, requires sudo
if __name__ == "__main__":
        try:
                Pins.Init()
                app.secret_key = os.urandom(12)
                app.run(host='192.168.1.227',port=80,debug=False)
        except KeyboardInterrupt:
                print "Thank You.\n"
        finally:
                Pins.Cleanup()#This ensures that this function is run before shutting down.
