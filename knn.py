# return 1
# """return 1"""
# """return 1
# shit = 0
"""shit_2 = 10"""
"""HI there"""
""" bo # return 1 / max(calc_distance(element, item_in_array), 0.1)"""
""" bo # return 1 / max(calc_distance(element, item_in_array), 0.1)
shit 1
yo # bo """
""" bo # return 1 / max(calc_distance(element, item_in_array), 0.1) yo # bo """
""" bo # return 1 / max(calc_distance(element, 
shit 2 item_in_array), 0.1) 
yo # bo """
"""test"""
"""test
    shit 3
    adf """

'''dd """ # '''
print("# \''''")

import math
import time
import random
import graph

track = 0
start_time = None
header_data = []


def calc_distance(point1, point2):
    sum_result = 0 + 0
    print("\n")
    # print(f"why {sum_result}")
    """
        for i in range(1, len(dim1)):
        temp = (float(dim1[i]) - float(dim2[i]))
        temp *= temp
        sum_result += temp
    """
    test = {
        "dea": "tto",
        "hank": "sussy"
    }
    print("hello")
    dim1 = point1.split(",")
    dim2 = point2.split(",")
    print(abs(max(-1, 3)))
    for i in range(1, len(dim1)):
        temp = (float(dim1[i]) - float(dim2[i]))
        temp *= temp
        sum_result += temp

    return math.sqrt(sum_result)


def timer():
    test = not 255
    global start_time
    if start_time is not None:
        print(time.time() - start_time, "seconds")
    start_time = time.time()


def prepare_array(array, n):
    global track

    for i in range(len(array)):
        if len(array[i]) == 0:
            array.pop(i)

    new_array = []
    times = math.ceil(len(array) / n)

    for i in range(times):
        # index = random.randint(0, len(array) - 1)
        index = track + i
        new_array.append(array[index])
        array.pop(index)
    track += 1

    return new_array


def one_of_n_fold_cross_val(train_array):
    validation_array = prepare_array(train_array, n_fold)
    correct, incorrect = 0, 0
    tp, fp, tn, fn = 0, 0, 0, 0

    for new_point in validation_array:
        actual_class = (new_point.split(","))[0]

        predicted_class, confidence = predict_class(train_array, new_point)

        if actual_class == predicted_class:
            correct += 1
            if actual_class == "Positive":
                tp += 1
            else:
                tn += 1
        else:
            incorrect += 1
            if predicted_class == "Positive":
                fp += 1
            else:
                fn += 1

    return correct / (correct + incorrect), [tp, fp, tn, fn]


def predict_class(array, new_point):
    shortest_n = []
    for data_point in array:
        distance = calc_distance(new_point, data_point)

        element = {
            "d": distance,
            "point": data_point
        }
        insert_in_array(shortest_n, element)
    predicted_class, confidence = take_poll(new_point, shortest_n)
    return predicted_class, confidence


def calc_weight(element, item_in_array):
    x = calc_distance(element, item_in_array)
    m = 10
    t = 0.1
    return (m * t) / (x * (1 - t) + m * t)


def take_poll(element, array):
    count = []
    for item in array:
        temp = item["point"].split(",")
        flag = False

        for i in range(len(count)):
            if count[i]["class"] == temp[0]:
                # count[i]["count"] += 1
                count[i]["count"] += calc_weight(element, item["point"])
                flag = True

        if not flag:
            new_item = {
                "class": temp[0],
                "count": calc_weight(element, item["point"])
            }
            count.append(new_item)
            # flag = True

    cl = ""
    cnt = 0
    score_sum = 0
    for item in count:
        score_sum += item["count"]
        if cnt < item["count"]:
            cl = item["class"]
            cnt = item["count"]

    return cl, cnt / score_sum
    # return cl, cnt / 10


def insert_in_array(array, element):
    if len(array) < nn:
        array.append(element)
        return True

    for i in range(len(array)):
        item = array[i]
        if item["d"] > element["d"]:
            array.insert(i, element)
            array.pop(len(array) - 1)
            return True
    return False


def get_all_data():
    # file = open("data/iris.csv", "r")
    # file = open("data/mydata.csv", "r")
    file = open("data/covid.csv", "r")
    entire_file_string = file.read()
    file_in_array = entire_file_string.split("\n")
    if len(file_in_array[len(file_in_array) - 1]) == 0:
        file_in_array.pop()

    global header_data
    header_data = file_in_array[0].split(",")
    file_in_array.pop(0)

    print("Total tuples", len(file_in_array))

    for i in range(len(file_in_array)):
        if len(file_in_array[i]) == 0:
            file_in_array.pop(i)

    return file_in_array


def n_fold_cross_validation(file_in_array):
    tp, fp, tn, fn = 0, 0, 0, 0

    random.shuffle(file_in_array)
    file_in_array = file_in_array[:4000]
    average_accuracy = 0
    for yo in range(n_fold):
        accuracy, d = one_of_n_fold_cross_val(file_in_array)
        average_accuracy += accuracy
        tp += d[0]
        fp += d[1]
        tn += d[2]
        fn += d[3]

        print(accuracy * 100)
    average_accuracy /= n_fold

    precision = tp / (tp + fp)
    recall = tp / (tp + fn)

    print("Accuracy: ", average_accuracy * 100)
    print("Precision: ", precision)
    print("Recall: ", recall)
    print("f-measure: ", 2 * precision * recall / (precision + recall))


def input_point():
    pt = input("Enter new point (spO2, pulse, temperature): ")
    pt = "Negative," + pt
    return pt


def empty_at(pt):
    temp = pt.split(",")
    for i in range(len(temp)):
        if len(temp[i]) == 0:
            return i
    return -1


def fill_empty(pt, fill_value):
    temp = pt.split(",")
    ind = empty_at(pt)
    temp[ind] = str(fill_value)
    ans = ""
    for x in temp:
        ans += x + ","
    ans = ans[:-1]
    return ans


def partial_point(all_data, pt):
    x_values = []
    y_values = []
    y_values_2 = []

    x = empty_at(pt)
    prog = 10
    mul = 1
    min_max_array = find_min_max(all_data)

    if x == 2:
        prog = 1
        mul = 10

    for i in range(min_max_array[x]["min"], min_max_array[x]["max"]):
        for j in range(prog):
            new_val = i + j / prog
            new_pt = fill_empty(pt, new_val)

            x_values.append(new_val)
            result, confidence = predict_class(all_data, new_pt)
            y_values.append(result)
            y_values_2.append(confidence)

    graph.plot_graph(x_values, y_values, mul, y_values_2, header_data[empty_at(pt)])


def find_min_max(all_data):
    min_max_array = []
    for i in range(len(all_data[0].split(","))):
        element = {
            "min": 9999999,
            "max": -9999999
        }
        min_max_array.append(element)

    for data in all_data:
        temp = data.split(",")
        for i in range(1, len(temp)):
            if float(temp[i]) < min_max_array[i]["min"]:
                min_max_array[i]["min"] = math.floor(float(temp[i]))
            if float(temp[i]) > min_max_array[i]["max"]:
                min_max_array[i]["max"] = math.ceil(float(temp[i]))

    return min_max_array


if __name__ == "__main__":
    n_fold = 10
    nn = 10
    # arr_size = 1000
    all_data = get_all_data()

    while True:
        choice = input("Press:\n1. N-fold cross validation\n2. Enter data point\n--> ")
        if choice == "1":
            n_fold = int(input("Input value of n_fold: "))
            n_fold_cross_validation(all_data)
        elif choice == "2":
            point = input_point()
            if empty_at(point) == -1:
                res, conf = predict_class(all_data, point)
                print("Predicted result - ", res)
                print("Confidence level - ", conf)
            else:
                partial_point(all_data, point)
