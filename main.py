from questionBoard import *
from questionSet import *
from gamestats import *
import random


def opening(stdscr, board):
    stdscr.addstr(0, 0, str("#" * 119))
    stdscr.addstr(29, 0, str("#" * 119))
    board.print_big_text(stdscr, 3, 32, open_text_one)
    board.print_big_text(stdscr, 12, 36, open_text_two)
    rectangle(stdscr, 24, 29, 26, 89)
    stdscr.addstr(25, 35, "1. Play")
    stdscr.addstr(25, 60, "2. Play Without Tutorial")
    board.awaitResponse(stdscr)
    board.transition(stdscr)


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
    
    music = mixer.music.load('sounds/bgTheme.ogg')
    mixer.music.set_volume(0.25)
    mixer.music.play(-1)

    opening(stdscr, board)


    #question game loop
    while not gamestats.isGameOver():
        gameLoop(stdscr, board, questions, gamestats)


    mixer.music.stop()
    stdscr.getch()


wrapper(main)