import helper
from flask import Flask, render_template, session, redirect, request, send_file, jsonify
from flask_session import Session
import os
import json
from authlib.integrations.flask_client import OAuth
import requests
from io import BytesIO
import firebase_admin
from firebase_admin import credentials, firestore

PORT = int(os.environ.get("PORT", 8081))

app = Flask(__name__)
app.config["SECRET_KEY"] = "2e33e4f6-7977-4030-8f0f-3cbf1ccf35e2"
app.config["SESSION_TYPE"] = "filesystem" 

Session(app)

if os.path.exists("GOOGLE_APPLICATION_CREDENTIALS.json"):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "GOOGLE_APPLICATION_CREDENTIALS.json"

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred)
db = firestore.client()

OAuth_config = json.loads(helper.get_secret("OAUTH_SECRET", ".json"))
OAuth_config["web"]["metadata_url"] = "https://accounts.google.com/.well-known/openid-configuration"
OAuth_config["flask_app"] = {
    "flask_port": PORT,
    "flask_secret": "2e33e4f6-7977-4030-8f0f-3cbf1ccf35e2"
}

OAuth_client = OAuth(app)
OAuth_client.register("OAuth_app",
                      client_id = OAuth_config["web"]["client_id"],
                      client_secret = OAuth_config["web"]["client_secret"],
                      server_metadata_url = OAuth_config["web"]["metadata_url"],
                      client_kwargs = {
                          "scope": "openid profile email"
                      })

@app.route("/test")
def test():
    return render_template("index.html")

@app.route("/")
def landing():
    if "user" in session:
        if "userinfo" in session["user"]:
            if "sub" in session["user"]["userinfo"]:
                sub = session["user"]["userinfo"]["sub"]

                if helper.profile_exists(db, sub) is not False:
                    profile = helper.profile_exists(db, sub)

                    sub = session["user"]["profile"] = profile
                else:
                    return redirect("/profile")
    return render_template("landing.html", session=session.get("user"), pretty=json.dumps(session.get("user"), indent=4))

@app.route("/login")
def google_login():
    state = helper.generate_random_state()
    session["OAuth_state"] = state

    return OAuth_client.OAuth_app.authorize_redirect(redirect_uri="http://localhost:8081/sign-in", state=state)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

@app.route("/sign-in")
def google_callback():
    state = session.get("OAuth_state")
    token = OAuth_client.OAuth_app.authorize_access_token()
    session.pop("OAuth_state", None)

    session["user"] = token

    if "user" in session:
        if "userinfo" in session["user"]:
            if "sub" in session["user"]["userinfo"]:
                sub = session["user"]["userinfo"]["sub"]

                if not helper.profile_exists(db, sub):
                    return redirect("/profile")
                else:
                    profile = helper.profile_exists(db, sub)

    return redirect("/")



@app.route("/profile")
def profile():
    sub = session["user"]["userinfo"]["sub"]
    if helper.profile_exists(db, sub) is not False:
        return redirect("/")
    else:
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        session["user"]["userinfo"]["region"] = helper.get_country(client_ip)
        return render_template("profile.html", session=session.get("user"))

# APIs
@app.route("/api/proxy-image")
def proxy_image():
    url = request.args.get('url')
    response = requests.get(url)
    return send_file(BytesIO(response.content), mimetype='image/jpeg')

@app.route("/api/get-profile-letter")
def get_profile_letter():
    letter = request.args.get("letter")

    image_path = helper.get_profile_letter(letter)

    return send_file(image_path, mimetype="image/jpeg")


@app.route("/api/create-profile", methods=["POST"])
def create_profile():
    # Retrieve JSON data from the request
    data = request.get_json()
    
    # Check if data was received
    if not data:
        return jsonify({"error": "No data received"}), 400


    sub = session["user"]["userinfo"]["sub"]
    email = session["user"]["userinfo"]["email"]
    default_predictions = ["Arsenal", "Aston Villa", "AFC Bournemouth", "Brentford", "Brighton & Hove Albion", 
            "Chelsea", "Crystal Palace", "Everton", "Fulham", "Ipswich Town", "Leicester City", "Liverpool", 
            "Manchester City", "Manchester United", "Newcastle United", "Nottingham Forest", "Southampton", 
            "Tottenham Hotspur", "West Ham United", "Wolverhampton Wonderers"]

    profile_data = {
        "given_name": data.get("given_name"),
        "family_name": data.get("family_name"),
        "display_name": data.get("display_name"),
        "favourite_club": data.get("favourite_club"),
        "region": data.get("region"),
        "picture": data.get("picture"),
        "sub": sub,
        "predictions": default_predictions,
        "email": email
    }

    helper.add_profile_to_db(db, sub, profile_data)

    return jsonify({"message": "Profile created successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=PORT)