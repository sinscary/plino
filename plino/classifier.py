# -*- coding: utf-8 -*-
# @Author: Tasdik Rahman
# @Date:   2016-03-12
# @Last Modified by:   Tasdik Rahman, Nitesh Sharma
# @Last Modified time: 2016-04-05 22:49:40
# @GPLv3 License
# @http://tasdikrahman.me
# @Source Git Repository:: https://github.com/prodicus/spamfilter


from __future__ import division
from collections import defaultdict
import math
import logging

from tabulate import tabulate

logging.basicConfig(
    filename='logfiles/logfile.txt',
    level=logging.DEBUG,
    filemode='w',
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class NaiveBayesClassifier(object):

    """
    Inherits from the 'object' class. Nothing special
    """

    def __init__(self):
        """
        Initializes the Naive Bayes object

        :param self: class object
        """
        self.total = 0
        self.label_count = defaultdict(int)
        self.feature_count = defaultdict(int)
        self.feature_label = defaultdict(lambda: defaultdict(int))
        # Reason? Refer:  [1]
        # self.feature_label = defaultdict(lambda: defaultdict(int))
        self.classification = defaultdict(int)

    def train(self, featurelist, label):
        """
        Trains the classifier for gods sake!

        Trying to emulate the API which the NLTK wrapper tries to provide for
        its nltk.NaiveBayesClassifier.train() gives

        .. note::

        `defaultdict` is used bacause when we try to acces a key which is not
        there in the `dictionary`, we get a `KeyError`. Whereas in
        `defaultdict`.It will try to return a default value if the key is not
        found.

        For more on `defaultdict`,
        Refer: http://stackoverflow.com/a/5900634/3834059

        :param self: class object
        :param featurelist: the list of the features
        :param label: class of the feature
        """

        # set() clears out all the duplicate objects inside the 'featurelist'
        featurelist = list(set(featurelist))

        for feature in featurelist:
            self.feature_count[feature] += 1
            self.feature_label[feature][label] += 1

        # incrementing label counts and the like
        self.label_count[label] += 1
        self.total = self.total + 1

    def feature_probability(self, feature, label):
        """
        This function calculates the probability of a feature to belong to a
        particular label. (i.e class of 'spam' or 'ham' for us.)

        #TO-DO
        for an unseen featurem I can assign a random probability, let's say
        0.5

        :param self: class object
        :param feature: The feature for which we will be calculating the
                        probailty.
        :param label: spam or ham
        :returns: The probability of the feature being in the label.
        """
        # nothing but a ternary operator
        # returns spam, label == "ham" and the other way around
        rev_class = "spam" if label == "ham" else "ham"  # or opp_label

        # or I could use a lambda function, let's see how
        # rev_class = lambda label: "spam" if label == "ham" else "ham"
        # looks same to me!

        # *---------------------------------------------------------------------
        # P ( S | token ) =         no_in_spam / no_of_spam    <--- NUMERATOR
        #                     _______________________________________________
        #  DENOMINATOR --->    no_in_spam / no_of_spam + no_in_ham / no_of_ham
        # ----------------------------------------------------------------------

        feature_count = self.feature_label[feature][label]
        rev_class_count = self.feature_label[feature][rev_class]
        label_count = self.label_count[label]

        probability = 0  # or basicBayes

        if feature_count and label_count:
            NUMERATOR = feature_count / label_count
            DENOMINATOR = feature_count / label_count + \
                rev_class_count / self.label_count[rev_class]
            probability = NUMERATOR / DENOMINATOR

        return probability

    def document_probability(self, features, label):
        """
        Finds `document_probability()` by looping over the documents and
        calling `feature_probability()`

        :param self: class object
        :param features: List of features
        :param label: Label whose probability needs to be classified
        :returns: the probability of the document in being in a particular
                  class
        """

        if not self.total:
            return 0

        probability = 1.00
        features = list(set(features))
        for feature in features:
            # store the feature_probability
            fp = self.feature_probability(feature, label)
            if fp != 0:
                probability += fp

        try:
            op = probability
            return op
        except:
            # for ham to not be put in the spam box
            if label == "spam":
                return 0
            else:
                return 1

    def classify(self, features):
        """
        Writing the actual interface for the class here. Thi will classify our
        documents when called from the terminal

        ## TO-DO
        >>>NaiveBayesClassifier.classify(<document_to_be_classified>)
        <returns the class of the Document>
        >>>

        :param self: class object
        :param features: The feaures of the document passed
        :returns: The classification result!. *phew*
        """

        probability = {}
        for label in self.label_count.keys():
            probability[label] = self.document_probability(features, label)

        self.classification = probability

        if len(probability.items()) > 0:
            return sorted(
                probability.items(),
                key=lambda (k, v): v,
                reverse=True
            )[0][0]
        else:
            return "Bad day bruh! No classification done! Come next time."

    # for testing puposes
    def print_classification(self):
        """
        Prints classification object which stores a score for labels

        :param self: class object
        """
        list_of_lists = [list(elem) for elem in self.classification.items()]
        print tabulate(
            list_of_lists,
            headers=['Label', 'Score'],
            tablefmt='orgtbl'
        )

    def __str__(self):
        """
        Overriding the default `__str__` function for better readability

        :param self: class object
        """
        logging.info("No of Features : {feature}, \nNumber of spam email : {spam}, \nNumber of ham email : {ham}, \nTotal number of emails:  {total}".format(
            feature=len(self.feature_count),
            spam=self.label_count['spam'],
            ham=self.label_count['ham'],
            total=self.total
        ))
        return "No of Features : {feature}, \nNumber of spam email : {spam}, \nNumber of ham email : {ham}, \nTotal number of emails:  {total}".format(
            feature=len(self.feature_count),
            spam=self.label_count['spam'],
            ham=self.label_count['ham'],
            total=self.total
        )
