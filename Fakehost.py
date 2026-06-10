from flask import Flask, request, redirect

app = Flask(__name__)

servers = {}

GAMES = ["SA-MP", "CRMP", "Minecraft", "GTA V"]

MODS = {
    "SA-MP": ["Admiral RP", "Arizona RP"],
    "CRMP": ["Black Russia", "Majestic RP"],
    "Minecraft": ["Forge", "Pixelmon"],
    "GTA V": ["FiveM RP", "RageMP"]
}

POLICY = """
<h1>📜 Privacy Policy</h1>

<p>Этот проект является симуляцией хостинг-панели.</p>

<p>Все серверы и моды являются <b>не настоящими</b>.</p>

<p>Это учебный/шутливый проект.</p>

<p>Никакие реальные серверы не запускаются.</p>

<a href='/'>← Back</a>
"""

def page(content):
    return f"""
    <html>
    <head>
    <title>MEM AI FakeHost</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    body {{
        background:#0f0f0f;
        color:white;
        font-family:Arial;
        text-align:center;
    }}
    h1 {{color:#00ff99;}}
    .card {{
        background:#1c1c1c;
        margin:10px;
        padding:10px;
        border-radius:10px;
    }}
    a, button {{
        color:#00ff99;
        margin:5px;
        text-decoration:none;
    }}
    input,select {{
        padding:8px;
        margin:5px;
    }}
    </style>
    </head>
    <body>
    {content}
    </body>
    </html>
    """

@app.route("/")
def home():
    html = "<h1>🐐 MEM AI FakeHost</h1>"
    html += "<a href='/policy'>Policy</a><hr>"

    html += """
    <form method='POST' action='/create'>
    <input name='name' placeholder='Server name'>
    <select name='game'>
    """

    for g in GAMES:
        html += f"<option>{g}</option>"

    html += """
    </select>
    <button>Create</button>
    </form>
    <hr>
    """

    for name, data in servers.items():
        html += f"""
        <div class='card'>
        <h2>{name}</h2>
        <p>Game: {data['game']}</p>
        <p>Status: {data['status']}</p>

        <a href='/start/{name}'>▶ Start</a>
        <a href='/stop/{name}'>⛔ Stop</a>
        <a href='/join/{name}'>🎮 Join</a>

        <form method='POST' action='/mod/{name}'>
        <select name='mod'>
        """

        for m in MODS[data["game"]]:
            html += f"<option>{m}</option>"

        html += "</select><button>Add</button></form>"

        html += f"<p>{data['mods']}</p></div>"

    return page(html)

@app.route("/create", methods=["POST"])
def create():
    name = request.form["name"]
    game = request.form["game"]

    servers[name] = {
        "game": game,
        "status": "offline",
        "mods": []
    }

    return redirect("/")

@app.route("/start/<name>")
def start(name):
    servers[name]["status"] = "online"
    return redirect("/")

@app.route("/stop/<name>")
def stop(name):
    servers[name]["status"] = "offline"
    return redirect("/")

@app.route("/mod/<name>", methods=["POST"])
def mod(name):
    servers[name]["mods"].append(request.form["mod"])
    return redirect("/")

@app.route("/join/<name>")
def join(name):
    return page(f"""
    <h1>Connecting to {name}</h1>
    <p>Loading...</p>
    <h2 style='color:red;'>Error 404</h2>
    <p>Missing files</p>
    <a href='/'>Back</a>
    """)

@app.route("/policy")
def policy():
    return page(POLICY)

app.run(host="0.0.0.0", port=5000, debug=True)
