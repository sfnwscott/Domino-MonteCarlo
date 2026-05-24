from itertools import combinations_with_replacement
import time
import random
import pandas as pd
import statistics


class Player:
    def __init__(self,name):
        self.hand = None
        self.points = 0
        self.name = name

    def starting_draw(self, hand):
        self.hand = hand
        return None

    def strategy_choice(self, strat_combo, hand_moves, noscore_counts=None, noscore_indices=None, 
                        noscore_setlengths=None, on_set_name=None,
                        first_move=False):
        # team-2 is 0 index
        if (self.name == 'player-2') or (self.name == 'player-4'):
            strat = strat_combo[0]
            if (on_set_name == 'player-2') or (on_set_name == 'player-4'):
                on_set = True
            else:
                on_set = False
        else:
            strat = strat_combo[1]
            if (on_set_name == 'player-1') or (on_set_name == 'player-3'):
                on_set = True
            else:
                on_set = False

        #['min-count','min-options','max-tile','dynamic-min-count-max-tiles','random']

        # check if it's the first move
        if first_move:
            if strat == 'max_tile':
                argmax_move = max(range(len(hand_moves)), key=lambda x: sum(hand_moves[x]))
                move_index = argmax_move
            else:
                move_index = random.choice(list(range(len(hand_moves))))
            return move_index
        
        match strat:
            case 'min-count':
                argmin_move = min(range(len(noscore_counts)), key=lambda x: noscore_counts[x])
                move_index = noscore_indices[argmin_move]
            case 'min-options':
                argmin_move = min(range(len(noscore_setlengths)), key=lambda x: noscore_setlengths[x])
                move_index = noscore_indices[argmin_move]
            case 'max-tile':
                argmax_move = max(range(len(hand_moves)), key=lambda x: sum(hand_moves[x]))
                move_index = argmax_move  
            case 'dynamic-min-count-max-tiles':
                if on_set:
                    argmin_move = min(range(len(noscore_counts)), key=lambda x: noscore_counts[x])
                    move_index = noscore_indices[argmin_move]
                else:
                    argmax_move = max(range(len(hand_moves)), key=lambda x: sum(hand_moves[x]))
                    move_index = argmax_move
            case 'random':
                move_index = random.choice(noscore_indices)
            
        return move_index


    def play_first(self, strat_combo):
        scoring_inds = []
        for i in range(5):
            tile = self.hand[i]
            if (sum(tile) % 5 == 0) and (sum(tile) > 0):
                scoring_inds.append(i)
        out_tiles = []
        pair_lookup = []
        scoring_lookup = []
        
        if len(scoring_inds) == 0:
            # start with max?
            #move_tile = max(self.hand, key=lambda x: sum(x))
            move_ind = self.strategy_choice(strat_combo, self.hand, first_move=True)
            move_tile = self.hand[move_ind]
            out_tiles.append(move_tile[0])
            out_tiles.append(move_tile[1])
            scoring_lookup.append(True)
            scoring_lookup.append(True)
            if len(set(move_tile)) == 1:
                pair_lookup.append(True)
                pair_lookup.append(True)
            else:
                pair_lookup.append(False)
                pair_lookup.append(False)
        else:
            move_ind = max(scoring_inds, key=lambda x: sum(self.hand[x]))
            move_tile = self.hand[move_ind]
            score_ = sum(move_tile) // 5
            self.points += score_
            out_tiles.append(move_tile[0])
            out_tiles.append(move_tile[1])
            scoring_lookup.append(True)
            scoring_lookup.append(True)
            if len(set(move_tile)) == 1:
                pair_lookup.append(True)
                pair_lookup.append(True)
            else:
                pair_lookup.append(False)
                pair_lookup.append(False)            

        self.hand.remove(move_tile)
        return out_tiles, pair_lookup, scoring_lookup


    def play(self, out_tiles, pair_lookup, scoring_lookup, boneyard, second_move=False, 
             emptycount=0, on_set_name=None, strat_combo=None, p=False, game_num=None,
             round_num=None, num_turns=None):
        # out_tiles = board[0]
        # # only in the case pair is a score tile
        # # same shape as out_tiles
        # pair_lookup = board[1] # [False, True, False, False, ...] # true only for the first of the two

        # scoring_lookup = board[2] # [True, False, True, True, ...]
        #total = sum([out_tiles[l] for l in range(len(out_tiles)) if scoring_lookup[l] == True])
        total = sum([tile for tile, scoring in zip(out_tiles,scoring_lookup) if scoring])
        hand_moves = []
        board_indices = []
        for i in range(len(self.hand)):
            tile = self.hand[i]
            if (tile[0] not in out_tiles) and (tile[1] not in out_tiles):
                continue
            for j in range(len(out_tiles)):
                out = out_tiles[j]
                if (pair_lookup[j-1] == True) and (j > 0):
                    continue
                elif (tile[0] == out) or (tile[1] == out):
                    hand_moves.append(tile)
                    board_indices.append(j)

        # check if going to boneyard
        if len(hand_moves) == 0:
            can_play = False
            while not can_play:
                if len(boneyard) > 1:
                    #print('boneyard')
                    pick = random.choice(boneyard)
                    self.hand.append(pick)
                    boneyard.remove(pick)
                    for j in range(len(out_tiles)):
                        out = out_tiles[j]
                        if (pick[0] == out) or (pick[1] == out):
                            if not (pair_lookup[j-1] == True) and not (j > 0):
                            # if p:
                            #     print('hihi')
                            #     print(pair_lookup)
                            #     print(pick)
                            #     print(j)
                                hand_moves.append(pick)
                                board_indices.append(j)
                                can_play = True
                else:
                    # pass turn
                    #print('empty')
                    emptycount += 1
                    return out_tiles, pair_lookup, scoring_lookup, boneyard, emptycount
        else:
            pass

        # evaluate possible moves
        scoring_indices = []
        score_vals = []
        noscore_indices = []
        noscore_counts = []
        noscore_setlengths = []
        for k in range(len(hand_moves)):
            tile = hand_moves[k]
            out_index = board_indices[k]
            out = out_tiles[out_index]
            # if the out is in an end pair
            if pair_lookup[out_index] == True:
                if tile[0] == out:
                    count_ = total - 2*out + tile[1]
                    if (count_ % 5 == 0) and (count_ > 0):
                        scoring_indices.append(k)
                        score_ = count_ // 5
                        score_vals.append(score_)
                    else:
                        noscore_indices.append(k)
                        noscore_counts.append(count_)
                        # if it's an end pair the out will still be in the set
                        outset = set(out_tiles)
                        outset.add(tile[1])
                        noscore_setlengths.append(len(outset))
                else:
                    count_ = total - 2*out + tile[0]
                    if (count_ % 5 == 0) and (count_ > 0):
                        scoring_indices.append(k)
                        score_ = count_ // 5
                        score_vals.append(score_)
                    else:
                        noscore_indices.append(k)
                        noscore_counts.append(count_)
                        # if it's an end pair the out will still be in the set
                        outset = set(out_tiles)
                        outset.add(tile[0])
                        noscore_setlengths.append(len(outset))
            # check for if hand tile is a double
            elif len(set(tile)) == 1:
                count_ = total - out + 2*tile[0]
                if (count_ % 5 == 0) and (count_ > 0):
                    scoring_indices.append(k)
                    score_ = count_ // 5
                    score_vals.append(score_)
                else:
                    noscore_indices.append(k)
                    noscore_counts.append(count_)
                    outset = set(out_tiles[:out_index] + out_tiles[out_index+1:])
                    outset.add(tile[0])
                    noscore_setlengths.append(len(outset))
            # normal end on end
            else:
                if tile[0] == out:
                    if scoring_lookup[out_index]:
                        count_ = total - out + tile[1]
                    else:
                        count_ = total + tile[1]
                    if (count_ % 5 == 0) and (count_ > 0):
                        scoring_indices.append(k)
                        score_ = count_ // 5
                        score_vals.append(score_)
                    else:
                        noscore_indices.append(k)
                        noscore_counts.append(count_)
                        outset = set(out_tiles[:out_index] + out_tiles[out_index+1:])
                        outset.add(tile[1])
                        noscore_setlengths.append(len(outset))
                else:
                    if scoring_lookup[out_index]:
                        count_ = total - out + tile[0]
                    else:
                        count_ = total + tile[0]
                    if (count_ % 5 == 0) and (count_ > 0):
                        scoring_indices.append(k)
                        score_ = count_ // 5
                        score_vals.append(score_)
                    else:
                        noscore_indices.append(k)
                        noscore_counts.append(count_)
                        outset = set(out_tiles[:out_index] + out_tiles[out_index+1:])
                        outset.add(tile[0])
                        noscore_setlengths.append(len(outset))

        if len(score_vals) != 0:
            # highest points
            argmax_move = max(range(len(score_vals)), key=score_vals.__getitem__)
            move_index = scoring_indices[argmax_move]

            # add points
            self.points += score_vals[argmax_move]

        # use strategy
        else:
            if p:
                print('')
                print(hand_moves)
                print(strat_combo)
                print(self.name)
                print(self.points)
                print(on_set_name)
                print(noscore_indices)
                print('')
            move_index = self.strategy_choice(strat_combo, hand_moves, 
                                              noscore_counts, noscore_indices, 
                                              noscore_setlengths, on_set_name,
                                              first_move=False)
            
   
        # update the board and hand
        board_index = board_indices[move_index]
        move_out = out_tiles[board_index]
        move_tile = hand_moves[move_index]
        # double outside
        if pair_lookup[board_index] == True:
            if move_tile[0] == move_out:
                out_tiles.append(move_tile[1])
            else:
                out_tiles.append(move_tile[0])
            if not second_move:
                pair_lookup[board_index] = False
                pair_lookup[board_index + 1] = False
                scoring_lookup[board_index] = False
                scoring_lookup[board_index + 1] = False
                pair_lookup.append(False)
                scoring_lookup.append(True)
            else: 
                pair_lookup.append(False)
                scoring_lookup.append(True)
        # double tile
        elif len(set(move_tile)) == 1:
            # if (out_tiles == [0,3]) & (pair_lookup == [False,True]) & (scoring_lookup == [True, True]):
            #     print(out_tiles)

            out_tiles.append(move_tile[0])
            out_tiles.append(move_tile[1])
            pair_lookup.append(True)
            pair_lookup.append(True)
            scoring_lookup.append(True)
            scoring_lookup.append(True)
            out_tiles.pop(board_index)
            pair_lookup.pop(board_index)
            scoring_lookup.pop(board_index)
        # standard
        else:
            if move_tile[0] == move_out:
                out_tiles[board_index] = move_tile[1]
            else:
                out_tiles[board_index] = move_tile[0]
            if not scoring_lookup[board_index]:
                scoring_lookup[board_index] = True

        # remove from hand
        self.hand.remove(move_tile)
        if p:
            print(move_tile)
            print('')
        emptycount = 0
        return out_tiles, pair_lookup, scoring_lookup, boneyard, emptycount





def play_round(playerlist, prev_starter, strat_combo, dominos, game_num, round_num, p):
    if prev_starter is None:
        starting_player = random.randint(0,3)
    else:
        starting_player = (prev_starter + 1) % 4
    player_index = starting_player
    for _ in range(4):
        current_player = playerlist[player_index]
        drawn_hand = []
        for __ in range(5):
            tile = dominos.pop()
            drawn_hand.append(tile)
        current_player.starting_draw(drawn_hand)
        player_index += 1
        player_index = player_index % 4
    boneyard = dominos
    round_on = True
    player_index = starting_player

    # count points at start of round
    round_start_points = [player.points for player in playerlist]

    # start with first on the board
    current_player = playerlist[player_index]
    out_tiles, pair_lookup, scoring_lookup = current_player.play_first(strat_combo)
    player_index += 1
    player_index = player_index % 4
    num_turns = 1
    emptycount = 0
    
    while round_on:
        current_player = playerlist[player_index]
        if p:
            #print(num_turns)
            print('game',game_num)
            print('round',round_num)
            print('turn',num_turns)
            print(current_player.name)
            print('board')
            print(out_tiles)
            print(scoring_lookup)
            print(pair_lookup)
            print('player hand:',current_player.hand)
            #print('')
        if num_turns == 1:
            second_move = True
        else:
            second_move = False

        on_set_ind = min(range(len(playerlist)), key=lambda x: len(playerlist[x].hand))
        on_set_name = playerlist[on_set_ind].name

        out_tiles, pair_lookup, scoring_lookup, boneyard, emptycount = current_player.play(
            out_tiles, pair_lookup, scoring_lookup, boneyard, second_move, emptycount, 
            on_set_name, strat_combo, p, game_num, round_num, num_turns, 
        )


    
        # print('points',current_player.points)
        if len(current_player.hand) == 0:
            #winner = current_player
            winnername = current_player.name
            # count points from scoring vs points from end
            personal_points_scored_ingame = current_player.points - round_start_points[player_index]

            count_sum = 0
            if player_index % 2 == 0:
                team_points_scored_ingame = sum([playerlist[i].points - round_start_points[i] for i in [1,3]])

                for playeri in [0,2]: # odd
                    count_sum += sum([sum(tile) for tile in playerlist[playeri].hand])
            else:
                #team_points_scored_ingame = sum([player.points for player in [playerlist[1], playerlist[3]]])
                team_points_scored_ingame = sum([playerlist[i].points - round_start_points[i] for i in [0,2]])
                for playeri in [1,3]: # even
                    count_sum += sum([sum(tile) for tile in playerlist[playeri].hand])
            point_sum = count_sum // 5
            current_player.points += point_sum
            round_on = False
        player_index += 1
        player_index = player_index % 4
        num_turns += 1
        # if num_turns >= 40:
        #     print('broken')
        #     break
        if emptycount == 4:
            #print('')
            winnername = 'none'
            #personal_points_scored_ingame = #current_player.points - round_start_points[player_index]
            personal_points_scored_ingame = sum([playerlist[i].points - round_start_points[i] for i in [1,3]])
            personal_points_scored_end = 0
            
            return num_turns, winnername, playerlist, starting_player, personal_points_scored_end, personal_points_scored_ingame
    try:
        winnername
    except NameError:
        winnername = 'none'
        print('h')
        personal_points_scored_end = 0

    # count points won at end vs throughout
    personal_points_scored_end = point_sum#current_player.points - personal_points_scored_ingame

    return num_turns, winnername, playerlist, starting_player, personal_points_scored_end, personal_points_scored_ingame
       
def play_game(game_seed, game_num, results, strat_combo):
    domino_set = list(combinations_with_replacement(range(7),2))
    random.seed(game_seed)
    random.shuffle(domino_set)
    player1 = Player('player-1')
    player2 = Player('player-2')
    player3 = Player('player-3')
    player4 = Player('player-4')
    playerlist = [player1, player2, player3, player4]
    game_won = False
    num_rounds = 0
    prev_starter = None
    seed = game_seed
    num_turn_counts = []
    round_winners = []
    if game_num == 6:
        p = True
    else:
        p = False
    p = False
    while not game_won:
        random.seed(seed)
        dominos = domino_set.copy()
        random.shuffle(dominos)
        start_time = time.perf_counter()
        #if p:
            #print(num_rounds)

        num_turns, winnername, playerlist, prev_starter, personal_points_scored_end, personal_points_scored_ingame = play_round(playerlist, 
                                                                                                                                prev_starter, 
                                                                                                                                strat_combo, dominos, 
                                                                                                                                game_num=game_num, round_num=num_rounds, p=p)
        end_time = time.perf_counter()
        duration = (end_time - start_time) * 1000

        num_turn_counts.append(num_turns)
        round_winners.append(winnername)

        num_rounds += 1
        seed += game_seed
        even_points = player2.points + player4.points
        odd_points = player1.points + player3.points

        if (even_points >= 100) or (odd_points) >= 100:
            game_won = True
            # print(f'Game {game_num} finished in {num_rounds} rounds')
            # print(f'Player 1 & 3: {odd_points}')
            # print(f'Player 2 & 4: {even_points}')
        results_dict = {'game num': game_num, 'round num': num_rounds, 'num_turns': num_turns, 'duration (ms)': duration,
                        'winner': winnername, 'team-1 strategy': strat_combo[0], 'team-2 strategy': strat_combo[1],
                        'player1 pts': player1.points, 'player2 pts': player2.points,
                        'player3 pts': player3.points, 'player4 pts': player4.points, 
                        'started on set': playerlist[prev_starter].name, 'went out first': winnername,
                        'personal points scored ig': personal_points_scored_ingame, 'personal points scored eog': personal_points_scored_end}
        results.append(results_dict)
    return results


if __name__ == '__main__':
    num_games = 500
    game_seeds = list(range(0,10000,10000//num_games))
    game_nums = list(range(1,num_games+1))

    strategies = ['min-count','min-options','max-tile','dynamic-min-count-max-tiles','random']
    strategy_combos = list(combinations_with_replacement(strategies, 2))
    df_all = pd.DataFrame()
    for combo in strategy_combos:
        results = []
        for game_seed, game_num in zip(game_seeds, game_nums):
            results = play_game(game_seed, game_num, results, combo)
        df = pd.DataFrame(results)
        df_all = pd.concat([df_all, df])
    #print(df)
    #df.to_csv('../results/results_dynamic_oddminmax_evenminoptions.csv',index=False)
    df_all.to_csv('results/results_all_combos.csv',index=False)


  



    


