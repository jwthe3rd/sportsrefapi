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

    return jsonify({'table': html_table})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

