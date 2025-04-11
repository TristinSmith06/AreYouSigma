from questionBoard import *
from questionSet import *
from gamestats import *
import random

def gameLoop(stdscr, board, questions, gamestats):
    testQuestion = QuestionSet("Who is the most Skibidi?", "CaseOh", "Kai Cenat", "Baby Gronk", "The Jonkler", 2)

    #pick question and delete it from list to prevent showing the same question twice
    choice = random.randint(0, len(questions.questions_list) - 1)
    board.assignQuestionSet(questions.questions_list[choice])
    questions.questions_list.pop(choice)


    board.displayQuestionSet(stdscr)

    board.awaitResponse(stdscr)
    board.verifyResponse(stdscr, gamestats)
    board.transition(stdscr)
    
    board.displayScore(stdscr, gamestats.sigma_points, gamestats.unc_points)
    time.sleep(2.8)
    board.transition(stdscr)
    stdscr.attron(board.default)




def main(stdscr):
    #initialize classes and curses
    curses.resize_term(30, 120)
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()

    questions = Questions()
    board = QuestionBoard(stdscr)
    gamestats = Gamestats()

    #question game loop
    while not gamestats.isGameOver():
        gameLoop(stdscr, board, questions, gamestats)


    stdscr.getch()


wrapper(main)