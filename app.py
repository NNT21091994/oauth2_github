from flask import Flask, request, redirect, session, url_for, render_template
from requests_oauthlib import OAuth2Session
from flask.json import jsonify
import os
import sys
import logging

app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

client_id = "9msGHt3q5FVTu95FWs"
client_secret = "RB95DEgJckReDz2QRJ7uCBuf8cN32Brn"
authorization_base_url = "https://bitbucket.org/site/oauth2/authorize"
token_url = "https://bitbucket.org/site/oauth2/access_token"
redirect_uri="https://immense-ravine-87169.herokuapp.com/myapp/callback"

@app.route("/myapp")
def myapp():
	return render_template('view.js')


@app.route("/myapp/view")
def demo():
	try:
		bitbucket = OAuth2Session(client_id)
		authorization_url, state = bitbucket.authorization_url(authorization_base_url)
		session['oauth_state'] =  state
		return redirect(authorization_url)
	except Exception as e:
		return render_template('err.html', err=str(e))



@app.route("/myapp/callback", methods=['GET'])
def callback():
	bitbucket = OAuth2Session(client_id, state=session["oauth_state"])
	token = bitbucket.fetch_token(token_url, username=client_id, password=client_secret, authorization_response=redirect.uri)
	session["oauth_token"] = token
	return redirect(url_for('.profile'))


@app.route("/myapp/profile", methods=["GET"])
def profile():
	bitbucket = OAuth2Session(client_id, token=session["oauth_token"])
	return jsonify(bitbucket.get("https://api.bitbucket.org/1.0/user").json())

if __name__ == "__main__":
	os.environ['DEBUG'] = "1"
	app.secret_key = os.urandom(24)
	app.run(debug=True) 
