import csv

class QuestionSet():
    def __init__(self, question, r1, r2, r3, r4, correct):
        self.question = question
        self.responses = [r1, r2, r3, r4]
        self.correct = correct


class Questions():
    def __init__(self):
        
        self.questions_list = []

        with open('questions.csv', 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            
            line = 0

            for row in csv_reader:
                if line == 0:
                    line += 1
                else:
                    if len(row) == 0:
                        break
                    self.questions_list.append(QuestionSet(row[0], row[1], row[2], row[3], row[4], int(row[5])))
                    line += 1
