import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_derivative(x):
    return sigmoid(x) * (1 - sigmoid(x))


class Network:
    def __init__(self, inputs, desired_outputs, layer1neurons, layer2neurons, layer3neurons):
        self.inputs = inputs  # inputs as an array, dimensions are Inputs x Training lines
        self.desired_outputs = desired_outputs  # desired outputs encoded so that a single bit is 1
        self.output = np.zeros(self.desired_outputs.shape)  # output used for error calculation

        self.weightset1 = np.random.rand(self.inputs.shape[1], layer1neurons)  # weights from inputs to hidden layer
        self.weightset2 = np.random.rand(layer1neurons, len(desired_outputs[0]))  # weights from hidden layer 1 to 2
        self.output = np.zeros(self.desired_outputs.shape)  # output used for error calculation

    def feedforward(self):
        self.hiddenlayer1 = sigmoid(np.dot(self.inputs, self.weightset1))   # feedforward inputs to 1st layer
        self.output = sigmoid(np.dot(self.hiddenlayer1, self.weightset2))

    def backpropagate(self, learning_rate):
        # calculating the change of the weights, calculating first and adding later since the calculation
        # for every layer has to be done first
        # 2 hidden layers:
        weights2_change = np.dot(self.hiddenlayer1.T, (
                    learning_rate * (self.desired_outputs - self.output) * sigmoid_derivative(self.output)))

        weights1_change = np.dot(self.inputs.T, (
                    np.dot(learning_rate * (self.desired_outputs - self.output) * sigmoid_derivative(self.output),
                           self.weightset2.T) * sigmoid_derivative(self.hiddenlayer1)))

        self.weightset1 += weights1_change
        self.weightset2 += weights2_change