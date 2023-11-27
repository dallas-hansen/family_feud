import json
import glob
import random
from time import sleep
from threading import Thread


class Game:
    game_over = False
    #TODO: implement a fast money round
    fast_money = False
    def __init__(self):
        self.seed = 0
        self.previous_seeds = []
        self.pool = []
        self.question = ''
        self.answers = {}
        self.num_of_answers = 0
        self.correct_guesses = []
        self.points = 0
        self.countdown = 45
        self.host = ''


    def timer(self):
        # Countdown timer
        seconds = self.countdown
        while seconds:
            timeformat = f'\t:{seconds:02d}'
            print(timeformat, end='\r')
            sleep(1)
            seconds -= 1


    def set_seed(self):
        # Sets seed to a random number
        while self.seed in self.previous_seeds:
            self.seed = random.randint(0, len(self.pool) - 1)
        self.previous_seeds.append(self.seed)
    

    def fill_up_pool(self, pool_size=50):
        # Creates pool of questions. Pool_size is the number of questions in the pool.        
        json_files = glob.glob(r'questions_and_answers\json\*.json')
        for file_path in json_files:
            with open(file_path, 'r') as file:
                data = json.load(file)
            
            random_numbers = random.sample(range(len(data)), (pool_size // 5))

            for number in random_numbers:
                self.pool.append(data[number])
    

    def get_question(self):
        # Set seed and get question
        self.set_seed()
        self.question = self.pool[self.seed]["Question"]

    
    def get_answers(self):
        # Gets number of answers and parses answers from seed
        self.answers = {}
        seed = self.pool[self.seed]
        self.num_of_answers = (len(seed) - 1) // 2
        for num in range(self.num_of_answers):
            answer = seed[f'Answer {num + 1}']
            self.answers[f'{answer}'] = seed[f'#{num + 1}']
        self.answers = sorted(self.answers.items(), reverse=True, key=lambda item: int(item[1])) 
        
        
    def display(self, round_over=False):
        guess = self.host.guess
        word_box = '-' * 30
        points_box = ('-' * 4)
        print(f'\nTop {self.num_of_answers} answers on the board\n')
        print(f'{self.question}\n')
        for i in range(self.num_of_answers):
            len_points_str = len(str(self.answers[i][1]))
            answer = self.answers[i][0]
            points = self.answers[i][1]
            # prints top of box
            print(' ' + word_box + ' ' + points_box)
            print(f'| {i + 1}. ', end='')
            # prints sides and middle of box
            if self.survey_says(answer, points, guess) or round_over:
                print(answer + '|'.rjust((len(word_box)-3) - len(answer)) + ' ' + str(points) + '|'.rjust(4 - len_points_str))
            else:
                print((' ' * (len(word_box) - 4)) + '|' + '|'.rjust(5))
                
        print(' ' + word_box + ' ' + points_box)
        self.big_x()
        
    
    def survey_says(self, answer: str, points: int, guess = '') -> bool:
        """
        Checks if the guess is correct or not.

        Args:
            answer (str): The answer to the question.
            points (int): The amount of points it's worth.
            guess (str, optional): Current guess. Defaults to ''.

        Returns:
            bool: Whether or not the guess was correct.
        """
        # Sorts dictionary into a list of tuples based off the value
        # guess_lower = guess.lower()
        # answer = answer.lower()
        # if answer in self.correct_guesses:
        #     return True                                
        # elif guess_lower == answer:
        #     self.correct_guesses.append(guess_lower)
        #     self.points += int(points)
        #     self.host.guess_outcome = 'Correct'
        #     return True
        # elif self.host.guess_outcome == 'Correct':
        #     return False 
        # else:
        #     self.host.guess_outcome = 'Wrong Answer'
        #     return False
        guess_lower = self.host.guess.lower()
        
        for i, item in enumerate(self.answers):
            if item[0] == guess_lower:
                self.correct_guesses.append(i)
    
    def big_x(self):
        # Prints a big X for each strike
        top = '\/ '
        bottom = '/\\ '
        print(top * self.host.current_team.strikes)
        print(bottom * self.host.current_team.strikes)  
        print()    

        

class Family:
    def __init__(self, name):
        self.name = name
        self.members = []
        self.points = 0
        self.turn = 0
        self.strikes = 0
    
    
    def add_players(self):
        num_players = int(input('How many are on your team?: '))
        print('\nNow, let\'s determine turn order.\n')
        for i in range(num_players):
            self.members.append(input(f'Who is in position {i + 1}?: '))
    
    def guess(self):
        guess = input(f'{self.name}, what is your guess?: ')
        return guess
    
    

class Host:
    def __init__(self, game, family1, family2='', name='Heave Starvey'):
        self.name = name
        self.game = game
        self.team_1 = family1
        self.team_2 = family2
        self.current_team = ''
        self.guess = ''
        self.guess_outcome = 'unknown'
        self.strikes_available = 3
        self.is_stealing = False
        
    
    def reset(self):
        self.current_team.strikes = 0
        self.strikes_available = 3

    
    def next_round(self):
        if self.is_stealing:
            self.is_stealing = False
        elif self.current_team == self.team_1:
            self.current_team = self.team_2
        else:
            self.current_team = self.team_1

    
    def chance_to_steal(self):
        self.next_round()
        self.is_stealing = True
        self.strikes_available = 1
        print(f'Now Team {self.current_team.name} has a chance to steal!')


    def get_guess(self):
        self.guess_outcome = 'unknown'
        self.guess = self.current_team.guess()


    def check_guess(self):
        if self.guess_outcome == 'Wrong Answer':
            self.add_strike()


    def add_strike(self):
            self.current_team.strikes += 1
            if self.current_team.strikes == 3:
                self.game.big_x()
                sleep(2)
                self.current_team.strikes = 0
                self.chance_to_steal()

def main():
    team_1 = Family(input('What is your team name?\n'))
    # team_1.add_players()
    team_2 = Family(input('What is your team name?\n'))
    # team_2.add_players()
    game = Game()
    game.fill_up_pool()
    host = Host(game, team_1, team_2)
    game.host = host

    while not game.game_over:
        host.next_round()
        host.reset()
        game.get_question()
        game.get_answers()
        while host.current_team.strikes != host.strikes_available:
            game.display()
            print(game.answers)
            host.get_guess()
            host.check_guess()


if __name__ == '__main__':
    main()
