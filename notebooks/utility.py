def add_player_node(graph, player_id, selected_players_data):
    player_mask = selected_players_data['player_id'] == str(player_id)
    player = selected_players_data[player_mask].values[0]
    graph.add_node(player_id,
                   name=player[1] + ' ' + player[2],
                   country_code=player[3],
                   hand=player[4])
