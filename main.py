from questionBoard import *
from questionSet import *

def gameLoop(stdscr, board):
    testQuestion = QuestionSet("Who is the most Skibidi?", "CaseOh", "Kai Cenat", "Baby Gronk", "The Jonkler", 2)
    board.assignQuestionSet(testQuestion)
    board.displayQuestionSet(stdscr)

    board.awaitResponse(stdscr)
    board.verifyResponse(stdscr)
    board.transition(stdscr)
    
    board.displayScore(stdscr, 10, 5)
    time.sleep(3)
    board.transition(stdscr)
    stdscr.attron(board.default)

def main(stdscr):
    curses.resize_term(30, 120)
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()
    
    board = QuestionBoard(stdscr)
    for i in range(3):
        gameLoop(stdscr, board)


    stdscr.getch()


wrapper(main)