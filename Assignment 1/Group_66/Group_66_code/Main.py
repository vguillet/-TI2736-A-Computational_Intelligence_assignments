import math

from simple_network.Network import Network
import numpy as np
import matplotlib.pyplot as plt

import sys

np.set_printoptions(threshold=sys.maxsize)

# variables adjustable for testing:

greycode = [[0,0,0],[0,0,1],[0,1,1],[0,1,0],[1,1,0],[1,1,1],[1,0,1]]
learningrate = 0.001
epochs = 1500
neurons1 = 32
stoptraining = False # stop when at a local minimum
wrongepochs = epochs * 2 # set the amount of epochs it can go without setting a new lowest error without stopping
                            # set at epochs * 2 so it doesn't stop

def to_graycode(number):
    return greycode[int(number)-1].copy()


def from_graycode(code):
    if code[0] == 0:
        if code[1] == 0:
            if code[2] == 0:
                return 1
            elif code[2] == 1:
                return 2
        elif code[1] == 1:
            if code[2] == 0:
                return 4
            elif code[2] == 1:
                return 3
    elif code[0] == 1:
        if code[1] == 0:
            if code[2] == 1:
                return 7
        elif code[1] == 1:
            if code[2] == 0:
                return 5
            elif code[2] == 1:
                return 6



def results_to_error(results, desired):
    clone = results.copy() # necessary, otherwise alters the original array
    output = []
    for k in range(len(results)):
        for j in range(len(results[k])):
            if j + 1 == int(desired[k][0]):  # check whether the output being checked is the target output
                clone[k][j] = (1 - results[k][j]) ** 2
            else:
                clone[k][j] = (0 - results[k][j]) ** 2

        # record the mean sum of the errors squared
        output.append(sum(results[k]) / len(results[k]))
    return sum(output) / len(output)

# ___________________________________________________________DATA PRE-PROCESSING


def normalize(array):
    array_normalised = np.zeros(np.shape(array))
    for i in range(len(array[0][:])):
        normalised_value = (array[:][i] - min(array[:][i]))/(max(array[:][i]) - min(array[:][i]))
        array_normalised[:][i] = normalised_value
    return array_normalised


feature_lst = [
        [float(x) for x in lst] for lst in [
            row.strip().split(",") for row in open("../resources/features.txt").read().strip().split("\n")]
]

target_lst = [
    [float(x) for x in lst] for lst in [
        row.strip().split(",") for row in open("../resources/targets.txt").read().strip().replace("\n", ",").split(",")]
]

# set targets
with open("../resources/features.txt") as features:
    target_lst2 = np.zeros((len(features.readlines()), 3))

i = 0
for row in open("../resources/targets.txt").read().strip().replace("\n", ",").split(","):
    target_lst2[i] = to_graycode(row)
    i = i + 1

unknown_lst = [
    [float(x) for x in lst] for lst in [
        row.strip().split(",") for row in open("../resources/unknown.txt").read().strip().split("\n")]
]

feature_array = np.asarray(feature_lst)
target_array = np.asarray(target_lst2)
unknown_array = np.asarray(unknown_lst)

# ___________________________________________________________NETWORK INIT

# split the arrays in 5 parts
feature_array_1 = feature_array[0:math.floor((len(feature_array)/5)*1)]
feature_array_2 = feature_array[math.floor((len(feature_array)/5)*1):math.floor((len(feature_array)/5)*2)]
feature_array_3 = feature_array[math.floor((len(feature_array)/5)*2):math.floor((len(feature_array)/5)*3)]
feature_array_4 = feature_array[math.floor((len(feature_array)/5)*3):math.floor((len(feature_array)/5)*4)]
feature_array_5 = feature_array[math.floor((len(feature_array)/5)*4):math.floor((len(feature_array)/5)*5)]
target_array_1 = target_array[0:math.floor((len(target_array)/5)*1)]
target_array_2 = target_array[math.floor((len(target_array)/5)*1):math.floor((len(target_array)/5)*2)]
target_array_3 = target_array[math.floor((len(target_array)/5)*2):math.floor((len(target_array)/5)*3)]
target_array_4 = target_array[math.floor((len(target_array)/5)*3):math.floor((len(target_array)/5)*4)]
target_array_5 = target_array[math.floor((len(target_array)/5)*4):math.floor((len(target_array)/5)*5)]

# create the neural network
nn = Network(feature_array, target_array, neurons1, 8, 8)


# create two arrays for the plotting of the graphs
train_graph = []
validation_graph = []

lowest_error = 1
previous_error = 1 # initialise to 1, checks the error later in the for loop

decreasing = True
lowarray1 = nn.weightset1.copy()
lowarray2 = nn.weightset2.copy()
count = 0
lowcount = 0
for i in range(epochs):
    count += 1
    print(str(i) + "/" + str(epochs))
    train_errors = [] # since you have to split the training sets in 3 parts, take the average of the 3

    # first training set
    nn.inputs = feature_array_1 # set trainingset 1 as input
    nn.desired_outputs = target_array_1 # set trainingset 1 as output
    nn.feedforward() # run
    nn.backpropagate(learningrate) # edit the weights
    train_errors.append(results_to_error(nn.output, nn.desired_outputs)) # store the errors

    # second training set
    nn.inputs = feature_array_2
    nn.desired_outputs = target_array_2
    nn.feedforward()
    nn.backpropagate(learningrate)
    train_errors.append(results_to_error(nn.output, nn.desired_outputs))

    # third training set
    nn.inputs = feature_array_3
    nn.desired_outputs = target_array_3
    nn.feedforward()
    nn.backpropagate(learningrate)
    train_errors.append(results_to_error(nn.output, nn.desired_outputs))

    train_graph.append(sum(train_errors)/len(train_errors)) # take average of 3 training sets error

    # first validation set
    nn.inputs = feature_array_4
    nn.desired_outputs = target_array_4
    nn.feedforward()
    validation_graph.append(results_to_error(nn.output, nn.desired_outputs))

    if previous_error < results_to_error(nn.output, nn.desired_outputs): # local minimum
        if stoptraining:
            break
        decreasing = False
    else:
        decreasing = True
    previous_error = results_to_error(nn.output, nn.desired_outputs) # edit the error stored to test next time

    # if the validation error is more than before (initialised at 1)
    if lowest_error > results_to_error(nn.output, nn.desired_outputs):
        lowest_error = results_to_error(nn.output, nn.desired_outputs)
        lowcount = count
        lowarray1 = nn.weightset1.copy()
        lowarray2 = nn.weightset2.copy()
    else:
        if (count - lowcount > wrongepochs) and (decreasing == False):
            nn.weightset1 = lowarray1
            nn.weightset2 = lowarray2
            break

nn.inputs = feature_array_5
nn.desired_outputs = target_array_5
nn.feedforward()
calculated_output = nn.output.copy()

for i in range(len(calculated_output)):
    for j in range(len(calculated_output[i])):
        if calculated_output[i][j] > 0.5:
            calculated_output[i][j] = 1
        else:
            calculated_output[i][j] = 0


# Print answers
#print("Outputs of unknown file are: ")
#for i in range(len(calculated_output)):
#    if from_graycode(calculated_output[i]) != None:
#        print(str(from_graycode(calculated_output[i])))
#    else:
#        print(1) # default

# THIS IS FOR TESTING ERRORS WHEN WE HAVE A TARGET SET
c = 0
w = 0
for i in range(len(calculated_output)):
    print(str(from_graycode(calculated_output[i])) + " " + str(from_graycode(target_array_5[i])))
    if from_graycode(calculated_output[i]) == from_graycode(target_array_5[i]):
        c += 1
    else:
        w += 1
print("Correct: " + str(c))
print("Wrong: " + str(w))
print("Percentage right: " + str(c / (c+w)))


# ___________________________________________________________RESULT PROCESSING
# calculate the mse
# error_output = nn.output    # error of output
# mse_output = []         # mean square error per epoch
#
# # check if above a threshold value and record squared of error obtained
# print(mse_output)
# plot the mse per test set
plt.plot(range(len(train_graph)), train_graph)
plt.plot(range(len(validation_graph)), validation_graph)
plt.show()

# # write the mse per epoch obtained on results for easier checking
# open("../resources/results.txt", 'w').close()   # clear result.txt from previous run
# with open("../resources/results.txt", "a") as results:
#     for i in mse_output:
#             results.write(str(i+1) + "\n")
