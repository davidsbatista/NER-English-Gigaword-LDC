#!/bin/bash
java -mx20g -cp stanford-ner-2015-04-20/stanford-ner.jar edu.stanford.nlp.ie.NERServer -loadClassifier stanford-ner-2015-04-20/classifiers/english.conll.4class.distsim.crf.ser.gz -port 9191
