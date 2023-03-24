import datetime

class Participant():

    def __init__(self) -> None:
        self.id = ""
        self.nickname = ""

    def create_datafile(self):
        self.datafile = 'data/BART_' + self.id + '_' + datetime.datetime.now().strftime("%Y%m%d") + ".txt"
        with open(self.datafile, 'a') as f:
            f.write('ID; Balloon; Boom; Boom_limit; Presses; Stars; Tot_Stars' + '\n')
