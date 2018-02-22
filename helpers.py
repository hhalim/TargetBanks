# -*- coding: utf-8 -*-
"""
Utilities
@author: Hartono Halim
"""

class helpers(object):
    """
     https://stackoverflow.com/a/1118507/2437862
     Get a line by line in a text file without the /r/n or /n
     usage:
        f = open("myFile.txt", "r")
        for line in get_line(f):
            print line
    OR
        with open("myfile.txt") as f:
            for line in get_line(f):
                print line
    
    """
    @staticmethod
    def get_line(file):
        for line in file:
            if line[-2] == '\r' and line[-1] == '\n': #EOL \r\n style
                yield line[:-2]
            elif line[-1] == '\n':
                yield line[:-1]
            else:
                yield line
                
    @staticmethod
    #Check if string is empty or whitespace only
    def is_empty (my_string):
        return not (my_string and my_string.strip())                