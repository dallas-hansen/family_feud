

from time import sleep


class Host:
    def __init__(self, game, family1, family2='', name='Heave Starvey'):
        self.name = name
        self.game = game
        self.team_1 = family1
        self.team_2 = family2
        self.current_team = ''
        self.guess = ''
        self.guess_outcome = False
        self.strikes_available = 3
        self.is_stealing = False
        self.fast_money_contestant = ''


    def reset(self, hard_reset=False, soft_reset=False):
        # Resets the game. Changes values to default values again.
        if soft_reset:
            self.game.display_line_count = 0
            return
        if self.team_1.turn > len(self.team_1.members) - 1:
            self.team_1.turn = 0
        if self.team_2.turn > len(self.team_2.members) - 1:
            self.team_2.turn = 0
        self.is_stealing = False
        self.strikes_available = 3
        self.team_1.strikes = 0
        self.team_2.strikes = 0
        self.team_1.num_of_guesses = 0
        self.team_2.num_of_guesses = 0
        self.answers_still_on_board = True
        self.game.display_line_count = 0
        if hard_reset:
            self.game.points = 0
            self.game.correct_guesses = []
            self.guess_outcome = False


    def next_round(self):
        # Changes the current team
        if self.current_team == self.team_1:
            self.current_team = self.team_2
        else:
            self.current_team = self.team_1
            

    def chance_to_steal(self):
        # Makes it so the other team can steal
        self.next_round()
        self.is_stealing = True
        self.strikes_available = 1


    def get_guess(self):
        # Gets guess from player
        self.guess_outcome = False
        self.guess = self.current_team.guess()
        self.current_team.num_of_guesses += 1


    def check_guess(self):
        # Checks if guess is correct
        self.game.survey_says()
        if self.guess_outcome == False:
            self.add_strike()


    def award_points(self):
        # Awards points to the current team
        if self.is_stealing:
            if self.current_team == self.team_1:
                if self.team_1.strikes == self.strikes_available:
                    self.team_2.points += self.game.points
                    self.is_stealing = False
                    return True
                elif self.team_1.num_of_guesses > 0 and self.team_1.strikes == 0:
                    self.team_1.points += self.game.points
                    self.is_stealing = False
                    return True
            elif self.current_team == self.team_2:
                if self.team_2.strikes == self.strikes_available:
                    self.team_1.points += self.game.points
                    self.is_stealing = False 
                    return True
                elif self.team_2.num_of_guesses > 0 and self.team_2.strikes == 0:
                    self.team_2.points += self.game.points
                    self.is_stealing = False
                    return True
            else:
                return False
            
        elif self.game.num_of_answers == len(self.game.correct_guesses):
            self.current_team.points += self.game.points
            return True
        
        else:
            return False


    def add_strike(self):
        # Adds a strike to the current team
            self.current_team.strikes += 1
            if self.current_team.strikes == 3:
                self.game.display()
                sleep(2)
                self.chance_to_steal()
                
                
    def game_over(self):
        # Checks the end condition for the game (200 points)
        if self.team_1.points >= 200:
            self.game.game_over = True
            self.game.line_break('$', '$', 70)
            print(f'{self.team_1.name} has WON with {self.team_1.points} points')
            print('Choose 2 people to play fast money!\n')
            self.current_team = self.team_1
        elif self.team_2.points >= 200:
            self.game.game_over = True
            self.game.line_break('$', '$', 70)
            print(f'{self.team_2.name} has WON with {self.team_2.points} points')
            self.game.line_break('$', '$', 70)
            print('Choose 2 people to play fast money!\n')
            self.current_team = self.team_2