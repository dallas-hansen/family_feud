from threading import Thread
from time import sleep
import json
import glob
import random




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
        print(json_files)

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


    def display(self, guess = ''):
        answers = sorted(self.answers.items(), reverse=True, key=lambda item: int(item[1]))
        word_box = '-' * 30
        points_box = ('-' * 4)
        print(f'\nTop {self.num_of_answers} answers on the board\n')
        print(f'{self.question}\n')
        for i in range(self.num_of_answers):
            len_points_str = len(str(answers[i][1]))
            answer = answers[i][0]
            points = answers[i][1]
            # prints top of box
            print(' ' + word_box + ' ' + points_box)
            print(f'| {i + 1}. ', end='')
            # prints sides and middle of box
            if self.survey_says(answer, points, guess):
                print(answer + '|'.rjust((len(word_box)-3) - len(answer)) + ' ' + str(points) + '|'.rjust(4 - len_points_str))
            else:
                print((' ' * (len(word_box) - 4)) + '|' + '|'.rjust(5))
                
        print(' ' + word_box + ' ' + points_box)


        
    
    def survey_says(self, answer, points, guess = ''):
        # Sorts dictionary into a list of tuples based off the value
        guess = guess.lower()
        answer = answer.lower()
        if answer in self.correct:
            return True                                
        elif guess == answer:
            self.correct.append(guess)
            self.points += int(points)
            return True
        else:
            return False 


class Family:
    def __init__(self, name):
        self.name = name
        self.members = []
        self.points = 0
        self.strikes = 0
        self.turn = 0
    
    
    def add_players(self):
        num_players = int(input('How many are on your team?: '))
        print('\nNow, let\'s determine turn order.\n')
        for i in range(num_players):
            self.members.append(input(f'Who is in position {i + 1}?: '))
    
    def guess(self):
        guess = input()
        return guess


def main():
    team_1 = Family(input('What is your team name?\n'))
    # team_1.add_players()
    
    game = Game()
    game.fill_up_pool()
    game.get_question()
    game.get_answers()
    game.display()
    print(game.answers)
    end = input('Take a guess: ')
    while end != 'stop':
        game.display(end)
        print(game.answers)
        print(game.points)
        end = input()
    # game.display(team_1.guess())


    # team_2 = Family(input('What is your team name?\n'))

if __name__ == '__main__':
    main()
