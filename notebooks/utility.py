from enum import Enum
import numpy as np
import pandas as pd


class Year(Enum):
    year_2018 = 2018
    year_2019 = 2019
    year_2020 = 2020


def get_ranking_file_path(year):
    switch = {
        Year.year_2018: "../data/atp_rankings_10s.csv",
        Year.year_2019: "../data/atp_rankings_10s.csv",
        Year.year_2020: "../data/atp_rankings_current.csv"
    }
    return switch.get(year)


def year_string_to_enum(year):
    switch = {
        "2018": Year.year_2018,
        "2019": Year.year_2019,
        "2020": Year.year_2020
    }
    return switch.get(year)


def get_ranking_data(year):
    ranking_file_path = get_ranking_file_path(year)
    ranking_data = pd.read_csv(ranking_file_path)

    if year == Year.year_2018:
        mask = (ranking_data['ranking_date'] >= 20180000) & (ranking_data['ranking_date'] < 20190000)
    elif year == Year.year_2019:
        mask = (ranking_data['ranking_date'] >= 20190000) & (ranking_data['ranking_date'] < 20200000)

    if year == Year.year_2018 or year == Year.year_2019:
        return ranking_data[mask]
    else:
        return ranking_data


def get_player_rank(player_id, ranking_data):
    ranking_mask = ranking_data['player'] == player_id
    ranking_single_player = ranking_data[ranking_mask]
    ranks = ranking_single_player[['rank']].values
    if ranks.any():
        average_rank = np.round(np.average(ranks), 2)
        std_derivation = np.round(np.std(ranks))
    else:
        average_rank = -1.0
        std_derivation = -1.0

    return average_rank, std_derivation


def add_player_node(graph, player_id, players_data, ranking_data):

    avg_rank, std_der = get_player_rank(player_id, ranking_data)

    player_mask = players_data['player_id'] == str(player_id)
    player = players_data[player_mask].values[0]
    graph.add_node(player_id,
                   name=player[1] + ' ' + player[2],
                   country_code=player[3],
                   hand=player[4],
                   avg_rank=avg_rank,
                   std_der=std_der)
