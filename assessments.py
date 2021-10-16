
from typing import List
import pandas as pd
import numpy as np
from pandas.core import indexing
import random
import csv
import copy
import os
import pickle
from pathlib import Path
from datetime import datetime, time
from tkinter import filedialog
from tkinter import *
import glob
from tkinter import messagebox
import matplotlib.pyplot as plt
from itertools import compress

class EvaluationsAssessment:
    
    def __init__(self) -> None:
        self.__evaluation_data = {}

    def read_directories(self):

        #read the evaluation directories and files. Use
        filename =filedialog.askdirectory(title="Selecciona el directorio de la evaluación actual", initialdir='./archivos')
        ev_files = [x for x in glob.glob(filename + '/*.csv') if x.endswith(".csv")] 
        
        def get_file_name(file, len_dir):
            return file[len_dir:]      
        #read a files and get the main data

        for i, file in enumerate(ev_files):
          with open(file, mode='r', newline='', encoding='utf-8-sig') as readfile:
            filedata = csv.reader(readfile)
            row = []

            #leer las primeras 10 filas

            for j in range(11):
              row.append(next(filedata))
          
          col_evaluation = pd.read_csv(ev_files[i], skiprows=10, encoding='utf-8-sig')

          self.__evaluation_data[row[0][1]] = {
              'file_name': get_file_name(file, len(filename) + 1),
              'file_path': file,
              'status': False,
              'area': row[2][1],
              'completion': 0.0,
              'date' :  datetime.strptime(row[1][1], '%d/%m/%Y'),
              'today' : datetime.now(), 
              'frequency' : 60, #days
              'evaluator' : row[0][1],
              'evaluates': row[10][2:],
              'evaluators': [],
              'log_data': col_evaluation.convert_dtypes(),
              'evaluation_results' : pd.DataFrame(index = col_evaluation['Preguntas']),
              'process_results' : pd.DataFrame(index = col_evaluation['Preguntas']),
              'removed_evaluators': [],
              'autofilled_NA': 0,
              'total_values': 0,
              'out_of_range_evaluations': [],
              'out_of_range_evaluates': []
          }

    #print(evaluation_data['Leona Ellison']['log_data'])        

#Read the dictionaries and complete the degree of completion, the evaluatos and the evaluations results

        for j, k in self.__evaluation_data.items():
          #Percentage of completion of each log file
            log_df = k['log_data'].copy(deep=True)
            log_df.drop(['Preguntas'], axis=1, inplace = True)
            num_na = log_df.isna().sum().sum()
            size = log_df.size
            k['completion'] = (size - num_na) / size * 100
            k['evaluation_results'].insert(0, 'Autoevaluación', list(k['log_data'][j + ' (Autoevaluación)']))
            #k['evaluation_results']['Autoevaluación'] = list(k['log_data'][j + ' (Autoevaluación)'])

            for n in k['evaluates']:
              self.__evaluation_data[n]['evaluators'].append(j)
              self.__evaluation_data[n]['evaluation_results'][j]= list(k['log_data'][n])
              

#       

        #print(self.__evaluation_data['Kelly White'])
        print(self.__evaluation_data['Addie Smith'])

        #self.checkplan()
#---------------------------- ADDITIONAL CHECKING WITH THE DESIGNED PLAN IN EVALUATORS.CSV FILE-------------------
###############################THERE ARE A LOT OF PRINT MESSAGES, TRASNFORM TO GUI#################

    def checkplan(self):

        #optional verification of the consistency of the logged data with the evaluators original design

        #this function compares 2 sets. If they are equal, returns True, else False
        def check_sets(set1, set2):
          return len(set1 - set2) == 0
        
    #First set for comparison. All the names logged, who has the evaluation form in the evaluation forms directory

        set_dict = set(self.__evaluation_data.keys())

        #Second set from the "evaluators file". The file must be readed 
        messagebox.showwarning('Aviso', 'Selecciona el archivo original de evaluadores.\n Verifica que corresponde con la fecha y los archivos que se están analizando \n Formato: yymmdd_evaluators.vX.csv')

        path_evaluators =filedialog.askopenfilename(title="Selecciona el archivo de evaluadores para comprobación:'yymmdd_evaluators.v_.csv", initialdir='./archivos', defaultextension='*.csv')

        row=[]
        with open(path_evaluators,'r',newline='', encoding='utf-8-sig') as editfile:
            readfile = csv.reader(editfile)
            for i in readfile: #pendiente de establecer while notempty()
                row.append(i)
        reading = copy.deepcopy(row[2:])
        #print(reading)
        #First name on each line
        list_of_collabs = set(list(map(lambda x: x[0], reading)))
        #print(list_of_collabs)

        #Set from the logged dictionary should equal the list of collabs from the evaluator file

        if check_sets(set_dict, list_of_collabs):
          print("Número de formularios: OK")
        else:
          print("El número de formularios no coincide con el plan")

        #print(len(set_dict - list_of_collabs))

        #Check that the results files are consistent with the archive of evaluators
        inconsist = 0 
        for line in reading:
          if check_sets(set(line[1:]), set(self.__evaluation_data[line[0]]['evaluation_results'].columns)) == False:
            inconsist +=1
            print(f'Revisar evaluación de {line[0]}')

        if inconsist != 0:
          print(f'Hay una inconsistencia en {consist} archivos de evaluación')
        else:
          print("Comprobación de evaluadores: OK")



if __name__ == '__main__':
    test = EvaluationsAssessment()
    test.read_directories()