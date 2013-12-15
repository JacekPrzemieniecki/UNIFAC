'''
Created on 11-10-2012

@author: Jacek Przemieniecki
'''

class ValueNotFound(LookupError):
    '''
    Raised by database.Database object if 
    the request is correct, but DB lacks required data
    '''

    def __init__(self):
        pass
        