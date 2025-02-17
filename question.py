import os
import nextcord
from itertools import zip_longest

from info_command import random_colour

path = os.path.dirname(os.path.abspath(__file__))


# Possible TODO: Refactor this to be server-specific


# Get list of questions
def get_questions():
    q = open(path + "/data/questions.txt", 'r')
    questions = q.read().split('\n')
    q.close()
    questions = [i.replace(r"\n", "\n") for i in questions]
    return questions


# Pop the first question out. Whether the file contains a question is NOT checked.
def pop_first_question():
    questions = get_questions()
    to_write = [i.replace("\n", r"\n") for i in questions[1:]]
    q = open(path + "/data/questions2.txt", 'w')
    q.write("\n".join(to_write))
    q.close()
    os.remove(path + "/data/questions.txt")
    os.rename(path + "/data/questions2.txt", path + "/data/questions.txt")
    return questions[0]


# Get questions to be filtered
def get_filters():
    f = open(path + "/data/filter.txt", 'r')
    questions = f.read().split('\n')
    f.close()
    questions = [i.replace(r"\n", "\n") for i in questions]
    return questions


def remove_question(index: int):
    questions = get_questions()
    f = open(path + "/data/questions2.txt", 'w')
    questions = [i.replace("\n", r"\n") for i in questions]
    f.write("\n".join(questions[:index] + questions[index + 1:]))
    f.close()
    os.remove(path + "/data/questions.txt")
    os.rename(path + "/data/questions2.txt", path + "/data/questions.txt")


# Accept or deny a question
def filter_question(index: int, status: bool):
    questions = get_filters()
    new_q = get_questions()

    # Update questions
    if status:
        new_q.append(questions.pop(index))
        new_q = [i.replace("\n", r"\n") for i in new_q]
        if len(new_q) > 0 and new_q[0] == "":
            new_q.remove("")
        q = open(path + "/data/questions2.txt", 'w')
        q.write("\n".join(new_q))
        q.close()
        os.remove(path + "/data/questions.txt")
        os.rename(path + "/data/questions2.txt", path + "/data/questions.txt")

    # Update filters
    f = open(path + "/data/filter2.txt", 'w')
    questions = [i.replace("\n", r"\n") for i in questions]
    if len(questions) > 0 and questions[0] == "":
        questions.remove("")
    if status:
        f.write("\n".join(questions))
    else:
        f.write("\n".join(questions[:index] + questions[index + 1:]))
    f.close()
    os.remove(path + "/data/filter.txt")
    os.rename(path + "/data/filter2.txt", path + "/data/filter.txt")


def add_to_filter(question: str):
    questions = [i.replace("\n", r"\n") for i in get_filters()]
    if len(questions) > 0 and questions[0] == "":
        questions.remove("")
    questions.append(question.replace("\n", r"\n"))
    f = open(path + "/data/filter2.txt", 'w')
    f.write("\n".join(questions))
    f.close()
    os.remove(path + "/data/filter.txt")
    os.rename(path + "/data/filter2.txt", path + "/data/filter.txt")


def create_approve_list():
    return [list(filter(lambda i: i is not None, que)) for que in list(zip_longest(*[iter(get_filters())] * 10))]


def filter_empty():
    return create_approve_list()[0][0] == ""


def create_question_list():
    return [list(filter(lambda i: i is not None, que)) for que in list(zip_longest(*[iter(get_questions())] * 10))]


def questions_empty():
    return create_question_list()[0][0] == ""


def create_approve_pages(title: str, url: str):
    it = create_approve_list()

    if it[0][0] != "":
        text = [("Approve/Reject questions by selecting below and click the corresponding button!\n"
                 "Questions:\n" +
                 "\n".join(
                    [f"----------{(10 * i + j + 1):02d}----------\n"
                     f"{it[i][j]}" for j in range(len(it[i]))]
                 ) +
                 "\n") for i in range(len(it))]
    else:
        text = ["There are no questions subject to approval!"]

    return [nextcord.Embed(title=title,
                           description=f"```\n{t}```",
                           colour=random_colour(), url=url) for t in text]


def create_question_pages(title: str, url: str):
    it = create_question_list()

    if it[0][0] != "":
        text = [("Questions:\n" +
                 "\n".join(
                    [f"----------{(10 * i + j + 1):02d}----------\n"
                     f"{it[i][j]}" for j in range(len(it[i]))]
                 ) +
                 "\n") for i in range(len(it))]
    else:
        text = ["There are no questions in the system!"]

    return [nextcord.Embed(title=title,
                           description=f"```\n{t}```",
                           colour=random_colour(), url=url) for t in text]


def get_question(index: int):
    return get_questions()[index]


def get_filter_question(index: int):
    return get_filters()[index]
