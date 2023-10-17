import flask
from flask import render_template, url_for, redirect


def apology(message, code=400):
    def escape(s):
        for old, new in [("-", "--"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("404.html", top=code, bottom=escape(message))
