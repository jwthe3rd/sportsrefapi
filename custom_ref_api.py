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
    desired_stats = ['Type','Opponent', 'Notes']
    league, gender = return_usable_league(league)

    team_name = team_name.lower().replace(" ","-")

    if gender == 0:

        print(f'https://www.sports-reference.com/{league}/schools/{team_name}/{year}-schedule.html')

        df_raw = pd.read_html(f'https://www.sports-reference.com/{league}/schools/{team_name}/{year}-schedule.html')
        if len(df_raw)>1:
            df = df_raw[1]
        else:
            df = df_raw[0]

        result_added = 1
    else:
        df_raw = pd.read_html(f'https://www.sports-reference.com/{league}/schools/{team_name}/{gender}/{year}-schedule.html')
        if len(df_raw)>1:
            df = df_raw[1]
        else:
            df = df_raw[0]

        result_added = 2


    dropped_stats = []
    location_not_found = True

    for stat in df.keys():
        if stat not in desired_stats:
            dropped_stats.append(stat)
        if stat.split()[0] == 'Unnamed:' and location_not_found:
            location_list = [df['Opponent'][i] if isinstance(x, float) else x + ' ' + df['Opponent'][i] for i,x in enumerate(df[stat])]
            location_not_found = False

    df = df.fillna(" ")
    print(df.keys())
    print(df[df.keys()[0]])
    print(location_list)

    df['Opponent'] = location_list# + ' ' + df['Opponent']

    df['Result'] = df[df.keys()[list(df.keys()).index('Conf')+result_added]] #adds the column after Conf to the Result column...
                                                                # deals with the addition of the Time column in 2012

    df.insert(0,'Week #', ['Week ' + str(i + 1) for i in range(len(df))])

    if league == 'cfb':

        df['Rank'] = df['School'].str.extract(r'\((.*?)\)')

    return df.drop(columns=dropped_stats)

