#!/usr/bin/env python3
# Copyright 2018 DxChain(https://www.dxchain.com). All Rights Reserved.

"""
Lottery script for DxChain whitelist.
"""

from os import path
import sys
import csv
import random
from argparse import ArgumentParser

NUM_ROUND_A = 300
NUM_ROUND_B = 1000
NUM_ROUND_C = 12000


def args_parse():
    """
    Option parser to parse the seed, input and output
    """
    usage = "usage: %prog [options]"
    parser = ArgumentParser(usage)
    parser.add_argument('seed', help='The seed used for random')
    parser.add_argument('-i', '--input', dest='input', default='user_list.csv',
                        help='The input file', metavar='FILE')
    parser.add_argument('-o', '--output', dest='output', default='winners.csv',
                        help='The output file', metavar='FILE')
    args = parser.parse_args()
    if args.seed:
        return args
    parser.print_help()
    sys.exit(1)


def read_user(csv_file):
    """
    Read the user_list csv file into list of [refer_hash, kyc_point]
    """
    with open(csv_file, 'r') as data:
        rows = csv.reader(data, delimiter=',', quotechar=',')
        # user_list = [[row[0], int(row[1])] for row in list(rows)[1:]]
        # user_list.sort(key=lambda row: row[1], reverse=True)
        user_dict = dict()
        for row in list(rows)[1:]:
            user_dict[row[0]] = int(row[1])
        return user_dict


def write_user(winners_classes, csv_file):
    """
    Write the winners to CSV file
    """
    with open(csv_file, 'w') as data:
        writer = csv.writer(data, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['winner_refer_hash', 'white_list_score', 'class'])
        for winners_class in winners_classes:
            winners, class_name = winners_class
            for winner in winners:
                winner.append(class_name)
                writer.writerow(winner)


def select_players_assign_tickets(all_players, excluded_players, num_players):
    """
    Select the players from all player excluded from excluded_players and assign chips.
    num_players or more players are selected.

    all_players:        List of all players [user_refer_hash, kyc_point]
    excluded_players:   Set of users refer code that have been selected as winners before
    num_players:        Target number of users to be selected

    :return             players {user_refer_hash : (ticket_start, ticket_end)}
                        tickets {ticket_index : owner}
    """
    num_user_selected = 0
    num_tickets = 0
    tickets = dict()        # chip_index -> user refer hash
    players = dict()        # user refer hash -> (start chip_index, end chip_index)
    # If players of size num_players has been selected, all players with the
    # same points as the last selected users will also be picked.
    last_point = -1
    # Start selection
    for player_hash, kyc_point in all_players.items():
        if num_user_selected >= num_players \
                and kyc_point != last_point:
            break
        if player_hash in excluded_players:
            continue
        # The ticket number a player holds is the same as the kyc_point
        for ticket_index in range(num_tickets, num_tickets + kyc_point):
            tickets[ticket_index] = player_hash
        players[player_hash] = (num_tickets, num_tickets + kyc_point)
        num_tickets += kyc_point
        num_user_selected += 1
        if num_user_selected == num_players:
            last_point = kyc_point
    print('cut off point: {}'.format(last_point))
    return players, tickets


def start_lottery(players, tickets, num_winners):
    """
    Extract num_winners of players from players based on random.sample on tickets.

    players:        Users who are involved in the lottery {refer_code_hash: (ticket_start,
                    ticket_end)}
    tickets:        Ticket pool {ticket_index: owner_refer_hash}
    num_winners:    Number of winners to pick in this round
    return          list [winners of this lottery]
    """
    winners = []
    for _ in range(num_winners):
        winning_ticket = random.sample(tickets.keys(), 1)
        winner = tickets[winning_ticket[0]]
        ticket_start, ticket_end = players[winner]
        winners.append([winner, ticket_end - ticket_start])
        for ticket_index in range(ticket_start, ticket_end):
            tickets.pop(ticket_index)
    return winners


def not_selected_user(all_players, excluded_players):
    """
    return all not selected users
    """
    res = []
    for user, kyc_point in all_players.items():
        if user in excluded_players:
            continue
        res.append([user, kyc_point])
    return res


def main():
    """
    This is the main body of the lottery.

    The process mainly follows the following procedure:
    1. Parse the arguments
    2. Read in the data file
    3. Start lottery (3 rounds)
    4. Write to the data file
    """
    # Initialize random seed
    arguments = args_parse()
    seed = arguments.seed
    random.seed(seed)
    # Read users
    input_file = arguments.input
    dir_path = path.dirname(path.realpath(__file__))
    input_full_path = path.join(dir_path, input_file)
    users = read_user(input_full_path)

    chosen_user = set()
    # Start round A
    print('-' * 88)
    print('round A')
    candidates, ticket_pool = select_players_assign_tickets(users, chosen_user, NUM_ROUND_A)
    winner_tier1 = start_lottery(candidates, ticket_pool, NUM_ROUND_A)
    chosen_user = chosen_user.union(set([winner[0] for winner in winner_tier1]))

    # Start round B
    print('-' * 88)
    print('round B')
    candidates, ticket_pool = select_players_assign_tickets(users, chosen_user, NUM_ROUND_B)
    winner_tier2 = start_lottery(candidates, ticket_pool, NUM_ROUND_B)
    chosen_user = chosen_user.union(set([winner[0] for winner in winner_tier2]))
    # Start round C

    print('-' * 88)
    print('round C')
    candidates, ticket_pool = select_players_assign_tickets(users, chosen_user, NUM_ROUND_C)
    winner_tier3 = start_lottery(candidates, ticket_pool, NUM_ROUND_C)
    chosen_user = chosen_user.union(set([winner[0] for winner in winner_tier3]))

    not_selected = not_selected_user(users, chosen_user)

    output_file = arguments.output
    write_full_path = path.join(dir_path, output_file)
    write_user([(winner_tier1, 'TIER1'), (winner_tier2, 'TIER2'), (winner_tier3, 'TIER3'),
                (not_selected, 'NOT_SELECTED')], write_full_path)

    print('result file: {}'.format(write_full_path))


if __name__ == '__main__':
    main()
