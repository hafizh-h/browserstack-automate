from flask import Flask
import subprocess as sp

app = Flask(__name__)

@app.route("/")
def main():
    out = sp.run(["php", "index.php"], stdout=sp.PIPE)
    return out.stdout

if __name__ == "__main__":
    app.run()
