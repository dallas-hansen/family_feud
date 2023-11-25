import json
import glob
import random
from time import sleep
from threading import Thread




class Game:
    def __init__(self):
        self.seed = 0
        self.pool = []
        self.question = ''
        self.answers = {}
        self.num_of_answers = 0
        self.correct = []
        self.points = 0
        self.countdown = 45
        self.host = ''


    def timer(self):
        seconds = self.countdown
        while seconds:
            timeformat = f'\t:{seconds:02d}'
            print(timeformat, end='\r')
            sleep(1)
            seconds -= 1


    def set_seed(self):
        self.seed = random.randint(0, len(self.pool) - 1)
    

    def fill_up_pool(self, pool_size=50):
        json_files = glob.glob(r'questions_and_answers\json\*.json')
        for file_path in json_files:
            with open(file_path, 'r') as file:
                data = json.load(file)
            
            random_numbers = random.sample(range(len(data)), (pool_size // 5))

            for number in random_numbers:
                self.pool.append(data[number])
    

    def get_question(self):
        self.set_seed()
        self.question = self.pool[self.seed]["Question"]

    
    def get_answers(self):
        seed = self.pool[self.seed]
        self.num_of_answers = (len(seed) - 1) // 2
        for num in range(self.num_of_answers):
            answer = seed[f'Answer {num + 1}']
            self.answers[f'{answer}'] = seed[f'#{num + 1}']


    def display(self, guess = '', round_over=False):
        answers = sorted(self.answers.items(), reverse=True, key=lambda item: int(item[1]))
        word_box = '-' * 30
        points_box = ('-' * 4)
        print(f'\nTop {self.num_of_answers} answers on the board\n')
        print(f'{self.question}\n')
        self.big_x()
        for i in range(self.num_of_answers):
            len_points_str = len(str(answers[i][1]))
            answer = answers[i][0]
            points = answers[i][1]
            # prints top of box
            print(' ' + word_box + ' ' + points_box)
            print(f'| {i + 1}. ', end='')
            # prints sides and middle of box
            if self.survey_says(answer, points, guess) or round_over:
                print(answer + '|'.rjust((len(word_box)-3) - len(answer)) + ' ' + str(points) + '|'.rjust(4 - len_points_str))
                self.host.guess_outcome == 'Correct'
            else:
                print((' ' * (len(word_box) - 4)) + '|' + '|'.rjust(5))
                
        print(' ' + word_box + ' ' + points_box)
        
    
    def survey_says(self, answer, points, guess = ''):
        # Sorts dictionary into a list of tuples based off the value
        guess_lower = guess.lower()
        answer = answer.lower()
        if answer in self.correct:
            return True                                
        elif guess_lower == answer:
            self.correct.append(guess_lower)
            self.points += int(points)
            return True
        elif self.host.guess_outcome == 'Correct':
            return False 
        else:
            self.host.guess_outcome == 'Wrong Answer'
            return False
        
    
    def big_x(self):
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
        guess = input()
        return guess
    
    

class Host:
    # Trying to figure out guess outcome and applying strikes properly
    def __init__(self, game, family1, family2='', name='Heave Starvey'):
        self.name = name
        self.game = game
        self.team_1 = family1
        self.team_2 = family2
        self.current_team = ''
        self.guess = ''
        self.guess_outcome = 'unknown'

    
    def next_round(self):
        if self.current_team == self.team_1:
            self.current_team = self.team_2
        else:
            self.current_team = self.team_1

    
    def chance_to_steal(self):
        self.next_round()
        print(f'Now Team {self.current_team.name} has a chance to steal!')


    def get_guess(self):
        self.guess_outcome = 'unknown'
        self.guess = self.current_team.guess()


    def check_guess(self):
        self.game.display(self.guess)
        print(f'Guess outcome= {self.guess_outcome}')
        if self.guess_outcome == 'Wrong Answer':
            print(f'guess_outcome = {self.guess_outcome}')
            self.add_strike()


    def add_strike(self):
            self.current_team.strikes += 1
            if self.current_team.strikes == 3:
                self.game.big_x()
                sleep(2)
                self.current_team.strikes = 0
                self.chance_to_steal()

def main():
    end_condition = False
    force_end = ''
    team_1 = Family(input('What is your team name?\n'))
    # team_1.add_players()
    team_2 = Family(input('What is your team name?\n'))
    # team_2.add_players()
    game = Game()
    game.fill_up_pool()
    host = Host(game, team_1, team_2)
    game.host = host

    while end_condition is False or force_end != 'stop':
        host.next_round()
        game.get_question()
        game.get_answers()
        while host.current_team.strikes != 3:
            game.display()
            print(game.answers)
            force_end = host.get_guess()
            host.check_guess()


if __name__ == '__main__':
    main()
