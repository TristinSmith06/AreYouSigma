import curses

from curses import wrapper
from curses.textpad import rectangle
import time


from pygame import mixer

from asciiManager import *

class QuestionBoard():
    def __init__(self, stdscr):
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

        self.correct = curses.color_pair(1)
        self.incorrect = curses.color_pair(2)
        self.default = curses.color_pair(3)
        stdscr.attron(self.default)

        self.questionSet = None
        self.selectedResponse = ""

        self.separation_distance = 5 #numbers to specify layout of the question board y coordinate
        self.start = 2
        mixer.init()

    def assignQuestionSet(self, qs): #aggregation of questionset class
        self.questionSet = qs

    def gradual_print(self, y, x, text, stdscr, delay = 0.02): #print text over time with delay
        index = 0
        for i in text:
            stdscr.addstr(y, x + index, i)
            index += 1
            time.sleep(delay)
            stdscr.refresh()
    
    def awaitResponse(self, stdscr, options):
        curses.flushinp() #prevent buffering input
        self.selectedResponse = None

        while self.selectedResponse not in options: #ignore keys that aren't 1234 for input
            self.selectedResponse = stdscr.getkey()
        mixer.Sound.play(mixer.Sound("sounds/select.mp3"))
    
    def instantSelectionRedraw(self, stdscr, selection, wait = 0): #show only question and selected answer
        time.sleep(wait)
        stdscr.clear()
        rectangle(stdscr, 1, 4, 5, 114)
        stdscr.addstr(3, 8, self.questionSet.question)

        begin_y = self.start + ((selection) * self.separation_distance)
        end_y = 4 + begin_y
        rectangle(stdscr, begin_y, 4, end_y, 14)
        stdscr.addstr(2 + begin_y, 9, str(selection) + ".")
        rectangle(stdscr, begin_y, 19, end_y, 114)
        # self.gradual_print(begin_y + 2, 23, self.questionSet.responses[selection - 1], stdscr)
        stdscr.addstr(begin_y + 2, 23, self.questionSet.responses[selection-1])
        stdscr.refresh()

    def verifyResponse(self, stdscr, gamestats): #change color and determine if choice is correct
        self.instantSelectionRedraw(stdscr, int(self.selectedResponse))
        time.sleep(0.2) #breathing room between slection and drumroll
        mixer.Sound.play(mixer.Sound("sounds/drumroll.mp3"))
        if self.selectedResponse == str(self.questionSet.correct):
            stdscr.attron(self.correct) #add sigma point here
            gamestats.addPoint(0)

            '''Very much a hack fix because thr redraw function only changes the color, it doesnt have any specification for being correct
            or not, so a delay was added to sync up the color redraw and the sound instead of trying to pass in a parameter'''
            self.instantSelectionRedraw(stdscr, int(self.selectedResponse), 1.2)
            mixer.Sound.play(mixer.Sound("sounds/correct.mp3"))
        else:
            stdscr.attron(self.incorrect) #add unc point here
            gamestats.addPoint(1)
            self.instantSelectionRedraw(stdscr, int(self.selectedResponse), 1.2)
            mixer.Sound.play(mixer.Sound("sounds/incorrect.mp3"))
        # time.sleep(2)
        # self.instantSelectionRedraw(stdscr, int(self.selectedResponse))
        time.sleep(1)
        stdscr.move(0, 0)

    def transition(self, stdscr): #standard fade
        for i in range(30):
            stdscr.addstr(i, 0, str("#" * 119))
            stdscr.refresh()
            time.sleep(0.03)
        for i in range(30):
            stdscr.addstr(i, 0, str(" " * 119))
            stdscr.refresh()
            time.sleep(0.03)

    def displayScore(self, stdscr, sigma, unc):
        self.print_big_text(stdscr, 5, 15, sigma_text)
        self.print_big_text(stdscr, 5, 80, asciiNumbers[int(str(sigma)[0])])
        if sigma > 9:
            self.print_big_text(stdscr, 5, 87, asciiNumbers[int(str(sigma)[1])])
        self.print_big_text(stdscr, 16, 18, unc_text)
        self.print_big_text(stdscr, 16, 80, asciiNumbers[int(str(unc)[0])])
        stdscr.refresh()

    def displayQuestionSet(self, stdscr):
        rectangle(stdscr, 1, 4, 5, 114)
        self.gradual_print(3, 8, self.questionSet.question, stdscr)

        for i in range(4): #making the question board dynamically resize was a good idea in theory, horrible in practive
            begin_y = self.start + ((i + 1) * self.separation_distance) #where the questions should begin on y
            end_y = 4 + begin_y # number signifies how tall the questions should be
            rectangle(stdscr, begin_y, 4, end_y, 14)
            stdscr.addstr(2 + begin_y, 9, str(i+1) + ".")
            rectangle(stdscr, begin_y, 19, end_y, 114)
            self.gradual_print(begin_y + 2, 23, self.questionSet.responses[i], stdscr)
    
    def print_big_text(self, stdscr, y, x, text): #get the big ascii text and print it
        elem = [] #curses doesn't support coordinate multiline text naturally, so this is a hack fix
        for i in text:
            elem.append(i)
        splits = text.split("\n")
        for index in range(len(splits)):
            stdscr.addstr(y + index, x, splits[index])
            index += 1
        stdscr.refresh()

