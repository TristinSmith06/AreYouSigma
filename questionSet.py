class QuestionSet():
    def __init__(self, question, r1, r2, r3, r4, correct):
        self.question = question
        self.responses = [r1, r2, r3, r4]
        self.correct = correct
