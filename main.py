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


    def display(self):
        pass
        

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


def main():
    # team_1 = Family(input('What is your team name?\n'))
    # team_1.add_players()
    game = Game()
    game.fill_up_pool()
    game.get_question()
    print(game.question)
    game.get_answers()
    print(f'Top {game.num_of_answers} answers on the board')
    print(game.answers)

    # team_2 = Family(input('What is your team name?\n'))

if __name__ == '__main__':
    main()
