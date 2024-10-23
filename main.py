from tkinter import *
from classes.game import Game
from classes.family import Family
from classes.host import Host


def loop_condition(host):
    if not host.is_stealing and host.current_team.strikes == host.strikes_available:
        return False
    elif host.team_1.points > 200 or host.team_2.points > 200:
        return False
    elif host.award_points():
        return False
    else:
        return True            

def main(debug=False):
    team_1 = Family(input('What is your team name?\n'))
    team_1.add_players()
    team_2 = Family(input('What is your team name?\n'))
    team_2.add_players()
    game = Game()
    game.fill_up_pool()
    host = Host(game, team_1, team_2)
    game.host = host
    
    while not game.game_over:
        host.next_round()
        host.reset(hard_reset=True)
        game.get_question()
        game.get_answers()
        game.face_off(host.team_1.members[host.team_1.turn], host.team_2.members[host.team_2.turn], debug=debug)
        host.reset()
        # head to head
        while loop_condition(host):
            host.reset(soft_reset=True)
            game.line_break()
            game.display(debug=debug)
            host.get_guess()
            host.check_guess()
        game.display(round_over=True)
        host.game_over()
    game.fast_money()


if __name__ == '__main__':
    main()
