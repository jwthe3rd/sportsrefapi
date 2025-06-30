import pandas as pd
import numpy as np


def read_html_to_per_game_df(team_name, year):
    df = pd.read_html(f'https://www.sports-reference.com/cbb/schools/{team_name}/men/{year}.html#all_roster')
    return df[5]

def return_usable_league(raw_league):

    if raw_league[0:3] == 'cbb':
        return raw_league.split('_')
    else:
        return [raw_league, 0]

def read_team_schedule(league, team_name, year):
    desired_stats = ['Type','Opponent','Unnamed: 8']
    league, gender = return_usable_league(league)

    if gender == 0:

        print(f'https://www.sports-reference.com/{league}/schools/{team_name}/{year}-schedule.html')

        df = pd.read_html(f'https://www.sports-reference.com/{league}/schools/{team_name}/{year}-schedule.html')[1]
        print(df)
    else:
        df = pd.read_html(f'https://www.sports-reference.com/{league}/schools/{team_name}/{gender}/{year}-schedule.html')[1]


    dropped_stats = []

    for stat in df.keys():
        if stat not in desired_stats:
            dropped_stats.append(stat)
    

    return df.drop(columns=dropped_stats)

