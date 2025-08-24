from flask import Flask, render_template, request, jsonify, render_template_string
from custom_ref_api import read_team_schedule, read_ind_stats
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/team-schedule')
def team_sched():
    return render_template('team_sched.html')

@app.route('/individual-stats')
def individual_stats():
    return render_template('individual_stats.html')

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

@app.route('/api/get-ind-stats', methods=['POST'])
def get_ind_stats():
    data = request.get_json()
    league = data.get('league')
    team = data.get('team')
    year = data.get('year')
    name = data.get('name')
    pos = data.get('pos')
    selected_stats = data.get('stats', [])
    print(team)

    df = read_ind_stats(league, team, year, name, pos, selected_stats)
    tables = []
    for dataf in df:
        tables.append({'title': 'Stats', 'html': dataf.fillna('-').to_html(index=False, classes="table table-bordered table-striped table-hover", border=0)})

    #js = jsonify({'table': tables})
    #for tab in tables:
    #    print(json.dumps(tab, indent=2))


    #html_table = df.to_html(classes='table table-striped', index=False)

    return jsonify({'tables': tables})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

