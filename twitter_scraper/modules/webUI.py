from profile import *
from trends import *
from tweets import *

from flask import *

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/profileResult", methods=['POST'])
def profileResult():
    pr = Profile(request.form['username'])
    prTweets = get_tweets(request.form['username'], 1, "profile")

    pr = pr.to_dict()

    prTable = "<tr>"
    for key in pr:
        prTable += f"<th>{key}</th>"
    prTable += "</tr>"

    prTable += "<tr>"
    for column in pr:
        prTable += "<td>" + str(pr[column]) + "</td>"
    prTable += "</tr>"

    result = ""
    result += "<tr>"
    for key in prTweets[0]:
        result += f"<th>{key}</th>"
    result += "</tr>"

    for tweet in prTweets:
        result += "<tr>"
        for column in tweet:
            result += "<td>" + str(tweet[column]) + "</td>"
        result += "</tr>"

    return render_template("profileResult.html", pr = prTable, prTweets = result)


@app.route("/trends")
def trends():
    return render_template("trends.html", trends = get_trends())

@app.route("/tweets")
def tweets():

    return render_template("tweets.html")

@app.route("/tweetsResult", methods=['POST'])
def tweetsResult():
    tweets = get_tweets(request.form['query'], int(request.form['pages']), "query")
    result = ""


    result += "<tr>"
    for key in tweets[0]:
        result += f"<th>{key}</th>"
    result += "</tr>"

    for tweet in tweets:
        result += "<tr>"
        for column in tweet:
            result += "<td>" + str(tweet[column]) + "</td>"
        result += "</tr>"
    return render_template("tweetsResult.html", rs = result)

def launchWeb():
    app.run()

launchWeb()