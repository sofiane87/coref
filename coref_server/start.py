import json
import flask
from pprint import PrettyPrinter
from flask import request, jsonify, render_template
from core import get_sentences
from formatting import format_text

app = flask.Flask(__name__)
app.config["DEBUG"] = True
pp = PrettyPrinter(indent=1)


def process_form(result):
    expressions = []
    for key, value in result.items():
        if key.startswith("expression"):
            _, counter = key.split("_")
            if value.strip():
                case_sensitive = result.get(f"case_sensitive_{counter}", False)
                expression = value.strip()
                if not case_sensitive:
                    expression = expression.lower()
                expressions.append((expression, case_sensitive))
    return expressions


@app.route('/analyse', methods=['GET'])
def analyse():
    raw_data = json.loads(request.args.get("result"))
    # Extract info
    text = raw_data["text"]
    expressions = process_form(raw_data["expressions"])
    # Analyse
    analysis = get_sentences(text, expressions)

    # Getting Formatted output
    fmt_text = format_text(text=text, sentences=analysis)
    return {"html": fmt_text}


@app.route('/', methods=['GET'])
def home():
    return render_template("index.jinja")


app.run()
