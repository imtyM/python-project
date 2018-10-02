from Classes.serialClass import serialClass
from Classes.mongoDB import mongoDB
from serial.tools import list_ports
from Classes.algorithms import algorithms
import os

myDB = mongoDB('lab')

res = myDB.findAll()

known_list = []

for x in res:
    for y in x:
        for z in x['primary_print']:
            if z not in known_list:
                known_list.append(z)
                print('appending ', z)

print(known_list)