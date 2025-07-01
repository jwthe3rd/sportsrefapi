from flask import Flask, render_template, request, jsonify, render_template_string
from custom_ref_api import read_team_schedule

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/api/get-stats', methods=['POST'])
def get_stats():
    data = request.get_json()
    league = data.get('league')
    team = data.get('team')
    year = data.get('year')
    print(team)

    df = read_team_schedule(league, team, year)


    html_table = df.to_html(classes='table table-striped', index=False)
    print(html_table)

    return jsonify({'table': html_table})

    # Use render_template_string for simplicity (you can use templates if preferred)
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Stats Table</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
    </head>
    <body class="p-4">
        <h2>Team Stats</h2>
        <div>{{ table | safe }}</div>
    </body>
    </html>
    """, table=html_table)

    ## Simulate response (replace this with your actual logic or API calls)
    #response = {
    #    "year": year,
    #    "league": league,
    #    "team": team,
    #}
#
#    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

