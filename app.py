from flask import Flask, render_template, request, redirect
import random
import string

app = Flask(__name__)

# Store links in memory
links = {}


def create_code(length=6):
    chars = string.ascii_letters + string.digits

    while True:
        code = "".join(random.choices(chars, k=length))
        if code not in links:
            return code


def check_url(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url


@app.route("/", methods=["GET", "POST"])
def index():

    short_link = None

    if request.method == "POST":

        original_url = request.form["url"].strip()

        if original_url:

            original_url = check_url(original_url)

            code = create_code()

            links[code] = {
                "url": original_url,
                "visits": 0
            }

            short_link = request.host_url + code

    history = []

    for code, data in links.items():
        history.append({
            "code": code,
            "url": data["url"],
            "visits": data["visits"]
        })

    history.reverse()

    return render_template(
        "index.html",
        short_link=short_link,
        history=history
    )


@app.route("/<code>")
def open_link(code):

    if code in links:

        links[code]["visits"] += 1

        return redirect(links[code]["url"])

    return "<h2>404 | Link not found</h2>"


if __name__ == "__main__":
    app.run(debug=True)