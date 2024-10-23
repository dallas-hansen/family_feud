class Family:
    def __init__(self, name):
        self.name = name
        self.members = []
        self.points = 0
        self.turn = 0
        self.strikes = 0
        self.num_of_guesses = 0


    def add_players(self):
        num_players = int(input(f'\nHow many are on team {self.name}?: '))
        print('\nNow, let\'s determine turn order.\n')
        for i in range(num_players):
            self.members.append(input(f'Who is in position {i + 1}?: '))
        print()

    def guess(self):

        guess = input(f'{self.members[self.turn]}, what is your guess?: ')
        if self.turn + 1 == len(self.members):
            self.turn = 0
        else:
            self.turn += 1
        return guess