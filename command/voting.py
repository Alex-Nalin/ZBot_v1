import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt


def vote_main():
    title = input("Create title: ")
    objects = input("Create voting options separated by a comma: ")
    members = input("@mention users you would like to get responses from separated by a comma: ")
    vote(title, objects, members)


def vote(chart_title, x_values, mentions_of_users):
    mentions_of_users = separate_string_by_comma(mentions_of_users)
    x_values = separate_string_by_comma(x_values)
    y_pos = np.arange(len(x_values))

    performance = {}

    for item in x_values:
        performance[item.strip()] = 0

    num_of_response = 0

    while num_of_response < len(mentions_of_users):
        performance = get_preference(performance)
        num_of_response += 1

    values = performance.values()

    plt.bar(y_pos, values, align='center')
    plt.xticks(y_pos, x_values)
    plt.ylabel('# of votes')
    plt.title(chart_title)

    plt.show()


def get_preference(performance):
    key = input("What do you chose? ")
    if key in performance:
        value = int(performance.get(key)) + 1
        performance[key] = value
    else:
        print("No such value, try again ")
        get_preference(performance)
    return performance


def separate_string_by_comma(string):
    return string.split(',')


vote_main()
