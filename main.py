#coding:utf-8
import vector
import logistic_regression
import SVM

filename = vector.vector('Congressman David Kustoff has been a champion for the Trump Agenda - I greatly appreciate his support. David is strong on crime and borders, loves our Military, Vets and Second Amendment. Get out and vote for David on Thursday, August 2nd. He has my Full and Total Endorsement!')
print(filename)

print logistic_regression.result(filename)
#print('SVM',SVM.result(filename))