from random import choice
#from test import Time60

class RandSeq(object):
    def __init__(self, seq):
        self.data =seq
        
    def __iter__(self):
        return self
    
    def next(self):
        return choice(self.data)

for eachItem in RandSeq(('rock', 'paper', 'scissors')):
    print(eachItem)