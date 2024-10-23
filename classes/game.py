import glob
import json
import random
from time import sleep


class Game:
    game_over = False
    fast_money = False #TODO: implement a fast money round
    timer_on = False
    def __init__(self):
        self.seed = 0
        self.previous_seeds = []
        self.pool = []
        self.question = ''
        self.answers = {}
        self.num_of_answers = 0
        self.correct_guesses = []
        self.points = 0
        self.countdown = 5
        self.host = ''
        self.display_line_count = 0

# TODO: create a working timer
    # def timer(self):
    #     # Countdown timer
    #     self.timer_on = True
    #     seconds = self.countdown
    #     while self.timer_on and seconds >= 0:
    #         timeformat = f'\t:{seconds:02d}'
    #         print(timeformat, end='\r')
    #         sleep(1)
    #         seconds -= 1
    #     if seconds == 0:
    #         print(f'\n there are {seconds} left')
    #         self.timer_on = False
    #         self.host.add_strike()

    
    def face_off(self, player_1, player_2, debug=False):
        rebuttle = False
        won = False
        guesses = 0
        self.line_break()
        print('\n HEAD TO HEAD, FIRST TO ANSWER!')
        print(f'\n Would {player_1} and {player_2} please get ready\n')
        print(input('\nPress "Enter" to continue\n'))
        while not won:
            while 0 not in self.correct_guesses:
                self.line_break()
                self.display(debug=debug)
                self.host.guess = input('What is your guess?\n')
                self.survey_says()
                if rebuttle:
                    break
                elif self.host.guess_outcome:
                    rebuttle = True
                elif guesses > 3:
                    print('Dang! Tough question, huh? Rock, Paper, Scissors to see who won!')
                    sleep(6)
                    break
                if debug:
                    print(self.correct_guesses)
                guesses += 1
            self.display(debug=debug)
            won = True
        
        self.host.team_1.turn += 1 
        self.host.team_2.turn += 1
        face_off_winner = input(f'\nWho won? (1 for {self.host.team_1.name}, 2 for {self.host.team_2.name})\n').lower()
        pass
        is_playing = True
        pass_or_play = input('Pass or play? (p for pass, anything else for play)\n').lower()
        if pass_or_play == 'p':
            is_playing = False
        if is_playing:
            self.host.current_team = self.host.team_1 if face_off_winner == '1' else self.host.team_2   
        else:
            self.host.current_team = self.host.team_2 if face_off_winner == '1' else self.host.team_1   

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


    def print_team_scores(self):
        # Prints team scores
        print(f'{self.host.team_1.name.upper()} score: {self.host.team_1.points}', end='\t')
        print(f'\t{self.host.team_2.name.upper()} score: {self.host.team_2.points}')

    def line_break(self, symbol1='*', symbol2='*', length=70, second_symbol=True):
        # Prints a line break
        if second_symbol:
            print()
        print(symbol1 * length)
        if second_symbol:
            print(symbol2 * length)
            print()
    
    def increase_display_line_count(self, amount=1):
        self.display_line_count += amount


    def display(self, round_over=False, debug=False):
        # Displays the gameboard#
        word_box = '-' * 30
        points_box = ('-' * 4)
        area_between_displays = f'\t\t   '
        # Prints the team that is stealing
        # if self.host.is_stealing:
        #     self.line_break('/', '\\', 28 + len(self.host.current_team.name))
        #     print(f'Team {self.host.current_team.name} has a chance to steal!')
        #     self.line_break('/', '\\', 28 + len(self.host.current_team.name))
        print(f'\t\tPOINTS: {self.points}\n')
        self.print_team_scores()
        print(f'\nTop {self.num_of_answers} answers on the board\n')
        print(f'{self.question}\n')
        # Loops through the answers and prints ones that were guessed correctly
        # Also prints the board around the answers
        
        
        for i in range(self.num_of_answers):
            len_points_str = len(str(self.answers[i][1]))
            answer = self.answers[i][0]
            points = self.answers[i][1]
            # prints top of box
            print('\t ' + word_box + ' ' + points_box + area_between_displays, end='')
            self.right_display()
            self.increase_display_line_count()
            print(f'\t| {i + 1}. ', end='')
            # prints sides and middle of box
            if i in self.correct_guesses or round_over:
                print(answer + '|'.rjust((len(word_box)-3) - len(answer)) + ' ' \
                    + str(points) + '|'.rjust(4 - len_points_str) + f'{area_between_displays}', end='')
                self.right_display()
                self.increase_display_line_count()
            else:
                print((' ' * (len(word_box) - 4)) + '|' + '|'.rjust(5) + f'{area_between_displays}', end='')
                self.right_display()
                self.increase_display_line_count()
        print('\t ' + word_box + ' ' + points_box + f'{area_between_displays}', end='')
            
        for i in range(7 - self.num_of_answers):
            print('\t ' + (' ' * 37), end='')
            self.right_display()
            self.increase_display_line_count()
            

        self.right_display()
        self.big_x()
        if debug:
            print(f'strikes available = {self.host.strikes_available}')
            print(self.answers)
            
    def right_display(self, round_over=False, debug=False):
        if self.host.is_stealing:
            if self.display_line_count in [3, 8]:
                self.line_break('/', '\\', 28 + len(self.host.current_team.name), second_symbol=False)
            elif self.display_line_count in [4, 9]:
                self.line_break('\\', '\\', 28 + len(self.host.current_team.name), second_symbol=False)
            elif self.display_line_count in [5, 7]:
                print()
            elif self.display_line_count == 6:
                print(f'Team {self.host.current_team.name} has a chance to steal!')
            else:
                return print()
        else:
            return print()


    def survey_says(self): # TODO: see if generative AI can help do this better
        pass

    def big_x(self):
        # Prints a big X for each strike
        top = '\/ '
        bottom = '/\\ '
        print('\t   ' + top * self.host.current_team.strikes)
        print('\t   ' + bottom * self.host.current_team.strikes)
        print()
        
    
    def fast_money(self):
        self.line_break('$', '$', 70)
        print('congrats you made it fast money! Unfortunately nothing is here because I have not made it yet!')
        print("\n you're honestly pretty lucky this code even let us get this far...\n")
