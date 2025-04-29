from questionBoard import *
from questionSet import *
from gamestats import *
import random

class AreYouSigma():
    def __init__(self, stdscr):
        #initialize classes and curses
        curses.resize_term(30, 120)
        curses.curs_set(0)
        stdscr.clear()
        stdscr.refresh()

        self.board = QuestionBoard(stdscr)
        self.gamestats = Gamestats()
        
        music = mixer.music.load('sounds/bgTheme.ogg')
        mixer.music.set_volume(0.25)
        mixer.music.play(-1)

        self.opening(stdscr, self.board)

    def opening(self, stdscr, board):
        stdscr.addstr(0, 0, str("#" * 119))
        stdscr.addstr(29, 0, str("#" * 119))
        board.print_big_text(stdscr, 3, 32, open_text_one)
        board.print_big_text(stdscr, 12, 36, open_text_two)
        rectangle(stdscr, 24, 29, 26, 89)
        stdscr.addstr(25, 32, "Play [Press 1]")
        stdscr.addstr(25, 55, "Play Without Tutorial [Press 2]")
        board.awaitResponse(stdscr, ["1", "2"])
        board.transition(stdscr)
        if board.selectedResponse == "1":
            self.tutorial(stdscr, board)

    def tutorial(self, stdscr, board):
        board.gradual_print(2, 4, "You will be presented with a question and four answer choices", stdscr)
        board.gradual_print(4, 4, "Select the correct answer with the 1, 2, 3, and 4 keys", stdscr)
        board.gradual_print(6, 4, "If you are right, you get a Sigma Point", stdscr)
        board.gradual_print(8, 4, "Otherwise, you will recieve an Unc Point", stdscr)
        board.gradual_print(10, 4, "Get 15 Sigma Points to win", stdscr)
        board.gradual_print(12, 4, "If you get 5 Unc Points; however, you lose", stdscr)
        board.gradual_print(14, 4, "We are not responsible for any brainrot you experience while playing", stdscr)
        rectangle(stdscr, 17, 4, 19, 25)
        stdscr.addstr(18, 6, "Continue [Press 1]")
        board.awaitResponse(stdscr, ["1"])
        board.transition(stdscr)

    def endSreen(self, stdscr, board, gamestats):
        if gamestats.didPlayerWin():
            stdscr.attron(self.board.correct)
            board.print_big_text(stdscr, 10, 30, win)
        else:
            stdscr.attron(self.board.incorrect)
            board.print_big_text(stdscr, 10, 25, lose)
        stdscr.addstr(0, 0, str("#" * 119))
        stdscr.addstr(29, 0, str("#" * 119))
        
        gamestats.sigma_points = 0
        gamestats.unc_points = 0

        rectangle(stdscr, 24, 29, 26, 89)
        stdscr.addstr(25, 33, "Play Again [Press 1]")
        stdscr.addstr(25, 72, "Quit [Press 2]")
        board.awaitResponse(stdscr, ["1", "2"])
        board.transition(stdscr)
        if board.selectedResponse == "2":
            exit()

    def gameLoop(self, stdscr, board, questions, gamestats):

        #pick question and delete it from list to prevent showing the same question twice
        choice = random.randint(0, len(questions.questions_list) - 1)
        board.assignQuestionSet(questions.questions_list[choice])
        questions.questions_list.pop(choice)

        stdscr.attron(board.default)

        board.displayQuestionSet(stdscr)

        board.awaitResponse(stdscr, ["1", "2", "3", "4"])
        board.verifyResponse(stdscr, gamestats)
        board.transition(stdscr)
        
        board.displayScore(stdscr, gamestats.sigma_points, gamestats.unc_points)
        time.sleep(2.3)
        board.transition(stdscr)
        stdscr.attron(board.default)


def main(stdscr):
    ays = AreYouSigma(stdscr)
    while True:
    #question game loop
        questions = Questions()
        while not ays.gamestats.isGameOver():
            ays.gameLoop(stdscr, ays.board, questions, ays.gamestats)
        ays.endSreen(stdscr, ays.board, ays.gamestats)



wrapper(main)