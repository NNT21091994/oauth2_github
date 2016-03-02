from flask import Flask, request, redirect, session, url_for, render_template
from requests_oauthlib import OAuth2Session
from flask.json import jsonify
import os
import traceback
import sys
import logging
app = Flask(__name__)

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

client_id = "475f6645dbeae7705619"
client_secret = "da53ed6a6f596834145d45ca805532b9aeb58519"
authorization_base_url = "https://github.com/login/oauth/authorize"
token_url = "https://github.com/login/oauth/access_token"

@app.route("/myapp")
def myapp():
	return render_template('view.js')


@app.route("/myapp/view")
def demo():
	try:
		github = OAuth2Session(client_id)
		authorization_url, state = github.authorization_url(authorization_base_url)
		session['oauth_state'] =  state
		return redirect(authorization_url)
	except Exception as e:
		traceback.print_exc(file=sys.stdout)
		return render_template('err.html',err=str(e))


@app.route("/myapp/callback", methods=['GET'])
def callback():
	github = OAuth2Session(client_id, state=session["oauth_state"])
	token = github.fetch_token(token_url, client_secret=client_secret, authorization_response=request.url)
	session["oauth_token"] = token
	return redirect(url_for('.profile'))


@app.route("/myapp/profile", methods=["GET"])
def profile():
	github = OAuth2Session(client_id, token=session["oauth_token"])
	return jsonify(github.get("https://api.github.com/user").json())

if __name__ == "__main__":
	os.environ['DEBUG'] = "1"

	app.secret_key = os.urandom(24)
	app.config['SESSION_TYPE'] = 'filesystem'
	app.run(debug=True) 