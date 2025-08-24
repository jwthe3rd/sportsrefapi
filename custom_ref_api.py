import pandas as pd
import numpy as np
from urllib.error import HTTPError

STATS_DICT = {"Yards":""}


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

        try:
            df_raw = pd.read_html(f'https://www.sports-reference.com/{league}/schools/{team_name}/{year}-schedule.html')
        except HTTPError:
            return pd.DataFrame({"Error":['HTTP error! No data found with the requested information!']})
        if len(df_raw)>1:
            df = df_raw[1]
        else:
            df = df_raw[0]

        result_added = 1
    else:
        try:
            df_raw = pd.read_html(f'https://www.sports-reference.com/{league}/schools/{team_name}/{gender}/{year}-schedule.html')
        except HTTPError:
            return pd.DataFrame({"Error":['HTTP error! No data found with the requested information!']})
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

    df = df.fillna("-")
    print(df.keys())
    print(df[df.keys()[0]])
    print(location_list)

    df['Opponent'] = location_list# + ' ' + df['Opponent']

    df['Result'] = df[df.keys()[list(df.keys()).index('Conf')+result_added]] #adds the column after Conf to the Result column...
                                                                # deals with the addition of the Time column in 2012

    df.insert(0,'Week #', ['Week ' + str(i + 1) for i in range(len(df))])

    if league == 'cfb':

        df['Rank'] = df['School'].str.extract(r'\((.*?)\)')
        df['Rank'] = [x if not(isinstance(x, float)) else '-' for x in df['Rank']]

    return df.drop(columns=dropped_stats)


def read_ind_stats(league, team_name, year, name, pos, desired_stats):
    league, _ = return_usable_league(league)

    player_name = name.lower().replace(" ","-")


    for i in range(1,1000):
        if league=='nfl':
            try:
                if i >= 11:
                    numb = i-1
                else:
                    numb = f'0{i-1}'
                player_name = name.split()
                print(player_name)
                link_name = f'https://www.pro-football-reference.com/players/{player_name[1][0]}/{player_name[1][0:4]}{player_name[0][0:2]}{numb}/fantasy/{year}/#player_fantasy'
                print(link_name)
                df_raw = pd.read_html(link_name)
                last_three_keys = df_raw[0].keys()[-3:]
                df_fant = df_raw[0]['Unnamed: 1_level_0']['Unnamed: 1_level_1']
                df_fant[df_raw[0]['Unnamed: 2_level_0']['Unnamed: 2_level_1'].keys()[0]] = df_raw[0]['Unnamed: 2_level_0']['Unnamed: 2_level_1'][df_raw[0]['Unnamed: 2_level_0']['Unnamed: 2_level_1'].keys()[0]].values
                df_fant[df_raw[0]['Unnamed: 3_level_0']['Unnamed: 3_level_1'].keys()[0]] = df_raw[0]['Unnamed: 3_level_0']['Unnamed: 3_level_1'][df_raw[0]['Unnamed: 3_level_0']['Unnamed: 3_level_1'].keys()[0]].values
                df_fant[df_raw[0]['Unnamed: 4_level_0']['Unnamed: 4_level_1'].keys()[0]] = df_raw[0]['Unnamed: 4_level_0']['Unnamed: 4_level_1'][df_raw[0]['Unnamed: 4_level_0']['Unnamed: 4_level_1'].keys()[0]].values
                df_fant[df_raw[0]['Unnamed: 5_level_0']['Unnamed: 5_level_1'].keys()[0]] = df_raw[0]['Unnamed: 5_level_0']['Unnamed: 5_level_1'][df_raw[0]['Unnamed: 5_level_0']['Unnamed: 5_level_1'].keys()[0]].values
                df_fant[df_raw[0]['Unnamed: 6_level_0']['Unnamed: 6_level_1'].keys()[0]] = df_raw[0]['Unnamed: 6_level_0']['Unnamed: 6_level_1'][df_raw[0]['Unnamed: 6_level_0']['Unnamed: 6_level_1'].keys()[0]].values
                df_fant[df_raw[0]['Unnamed: 7_level_0']['Unnamed: 7_level_1'].keys()[0]] = df_raw[0]['Unnamed: 7_level_0']['Unnamed: 7_level_1'][df_raw[0]['Unnamed: 7_level_0']['Unnamed: 7_level_1'].keys()[0]].values
                df_fant[df_raw[0][last_three_keys[0][0]]['Fantasy'].keys()[0]] = df_raw[0][last_three_keys[0][0]]['Fantasy'][df_raw[0][last_three_keys[0][0]]['Fantasy'].keys()[0]].values
                df_fant[df_raw[0][last_three_keys[1][0]]['Fantasy'].keys()[0]] = df_raw[0][last_three_keys[1][0]]['Fantasy'][df_raw[0][last_three_keys[1][0]]['Fantasy'].keys()[0]].values
                df_fant[df_raw[0][last_three_keys[2][0]]['Fantasy'].keys()[0]] = df_raw[0][last_three_keys[2][0]]['Fantasy'][df_raw[0][last_three_keys[2][0]]['Fantasy'].keys()[0]].values

                df_raw=[df_fant]

                if df_fant['Tm'][0] != team_name:
                    raise ValueError
                if df_fant['Pos'][0] != pos:
                    raise ValueError

                break
                
            except HTTPError:
                return [pd.DataFrame({"Error":['HTTP error! No data found with the requested information!']})]
            
            #except KeyError:
            #    print(last_three_keys[1][0])
            #    return df_raw
            except ValueError:
                continue
        else:

            try:
                print(f'https://www.sports-reference.com/{league}/players/{player_name}-{i}.html')
                df_raw = pd.read_html(f'https://www.sports-reference.com/{league}/players/{player_name}-{i}.html')
            except HTTPError:
                return [pd.DataFrame({"Error":['HTTP error! No data found with the requested information!']})]

            #print(df_raw[2]['Touchdowns'].keys())
            print(desired_stats)
            break
        



    return df_raw