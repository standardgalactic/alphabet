from flask import Flask, request, render_template_string
import io
import contextlib

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
  <title>Simple Python Shell</title>
  <style>
    body { background: black; color: lime; font-family: monospace; }
    textarea, pre { width: 100%; background: black; color: lime; border: none; }
  </style>
</head>
<body>
  <h2>Simple Python Shell</h2>
  <form method="POST">
    <textarea name="code" rows="5">{{ code }}</textarea><br>
    <input type="submit" value="Run">
  </form>
  <h3>Output:</h3>
  <pre>{{ output }}</pre>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    code = request.form.get("code", "")
    output = ""
    if code:
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            try:
                exec(code, {})
            except Exception as e:
                print(e)
        output = f.getvalue()
    return render_template_string(TEMPLATE, code=code, output=output)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

