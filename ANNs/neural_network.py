#!/usr/bin/env python

from math import exp
from random import randrange

from perceptron import Perceptron, plot

class SigmoidPerceptron(Perceptron):
    """
    A sigmoid perceptron =S
    """
    def __init__(self, inputs):
        """
        Initializes all the weights in small random numbers
        between -.05 and .05
        """
        super(SigmoidPerceptron, self).__init__(inputs)
        self.weights = [weight + randrange(-5,5) / 100.
                        for weight in self.weights]
        self.last_evaluation = None

    def evaluate(self, inputs):
        """
        Evaluates the Perceptron output according to the sigmoid function
        """
        self.inputs = inputs
        self.last_evaluation = 1. / (1 + exp(sum([w * x for w, x in zip(self.weights, [1] + inputs)])))
        return self.last_evaluation


class NeuralNetwork(object):
    def __init__(self, inputs, hidden, outputs):
        """
        3 attributes:
          + inputs_number: just a number of inputs
          + hidden: a list of hidden SigmoidPerceptron's
          + outputs: a list of output SigmoidPerceptron's
        """
        self.inputs_number = inputs
        self.hidden = [SigmoidPerceptron(inputs) for i in range(hidden)]
        self.outputs = [SigmoidPerceptron(hidden) for i in range(outputs)]

    # Check this!
    def get_error(self, training_set):
        """
        The addition of all the errors for all the outputs in all the examples.
        assumes at least one previous evaluation.
        """
        error = 0
        for inputs, target_results in training_set:
            #output_results = self.evaluate(inputs)
            error += sum([(target_result - op.last_evaluation)**2
                          for target_result, op
                          in zip(target_results, self.outputs)])
        return error / 2

    def evaluate(self, inputs):
        """
        Propagates forward the inputs through the network and return the
        result in a list
        """
        results = []
        for op in self.outputs:
            results.append(op.evaluate([hp.evaluate(inputs) for hp in self.hidden]))
        return results

    def backpropagation_train(self, training_set, learning_rate=0.05):
        """
        """
        for inputs, target_results in training_set:
            output_results = self.evaluate(inputs)
            delta_outputs = [op.last_evaluation * (1 - op.last_evaluation) * \
                             (target_results[i] - op.last_evaluation)
                             for i, op in enumerate(self.outputs)]
            for i, op in enumerate(self.outputs):
                op.weights = [weight + learning_rate * inp * delta_outputs[i]
                              for weight, inp in zip(op.weights, op.inputs)]

            # Fuck, too much pasta-code
            delta_hidden = [hp.last_evaluation * (1 - hp.last_evaluation) * \
                            sum([op.weights[i] * delta_outputs[j]
                                 for j, op in enumerate(self.outputs)])
                            for i, hp in enumerate(self.hidden)]

def training(neural_network, training_set, learning_rate=.01,
             max_iterations=1000):
    """
    """
    it = 0; log = []
    while it < max_iterations:
        neural_network.backpropagation_train(training_set, learning_rate)
        log.append(neural_network.get_error(training_set))
        print 'Iteration %s - Error: %s' % (it, log[it])
        if not log[it]:
            break
        it += 1
    return log

def load_training_set(file_name):
    """
    Loads the training set in memory, returns
    [([inputs], [results]), ... , ()]
    """
    print 'loading training file \'%s\'' % file_name
    f = open(file_name)
    training_set = []
    for line in f:
        p1, p2, area = line.split()
        training_set.append(([float(p1), float(p2)], [int(area == 'A')]))
    f.close()
    return training_set

if __name__ =='__main__':
    plot(training(NeuralNetwork(2,5,1), load_training_set('bp_training/500.txt')))
