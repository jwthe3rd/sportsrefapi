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

        df_raw = pd.read_html(f'https://www.sports-reference.com/{league}/schools/{team_name}/{year}-schedule.html')
        if len(df_raw)>1:
            df = df_raw[1]
        else:
            df = df_raw[0]
        print(df)
    else:
        df_raw = pd.read_html(f'https://www.sports-reference.com/{league}/schools/{team_name}/{gender}/{year}-schedule.html')
        if len(df_raw)>1:
            df = df_raw[1]
        else:
            df = df_raw[0]


    dropped_stats = []

    for stat in df.keys():
        if stat not in desired_stats:
            dropped_stats.append(stat)
    

    df = df.rename(columns={'Unnamed: 8': 'Result'})

    return df.drop(columns=dropped_stats)

