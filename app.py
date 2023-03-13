import logging
import os

import openai
from flask import Flask, redirect, render_template, request, url_for
import logging

app = Flask(__name__)
handler = logging.FileHandler('chat.log')
logging_format = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(logging_format)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        animal = request.form["animal"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(animal),
            temperature=0.6,
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(animal):
    return """Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        animal.capitalize()
    )

@app.route("/chat", methods=("GET",))
def chat():
    keyword = request.args.get("keyword", "")
    response_txt = ""
    if keyword != "":
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": keyword}]
        )
        response_txt = completion.choices[0].message.content
        app.logger.info('-------- 聊天 -------')
        app.logger.info(keyword)
        app.logger.info(response_txt)

    return render_template("chat.html", keyword=keyword, result=response_txt)

@app.route("/draw", methods=("GET",))
def draw():
    keyword = request.args.get("keyword", "")
    response_urls = []
    if keyword != "":
        image_resp = openai.Image.create(prompt=keyword, n=4, size="512x512")
        it = iter(image_resp['data'])
        app.logger.info('-------- 画图 -------')
        app.logger.info(keyword)
        for x in it:
            response_urls.append(x['url'])
        app.logger.info(response_urls)
    return render_template("draw.html", keyword=keyword, result=response_urls)

if __name__ == "__main__":
    # app.run(host, port, debug, options)
    # 默认值：host="127.0.0.1", port=5000, debug=False
    app.run(host="0.0.0.0", port=5000)