
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
              'full_columns': None,
              'use_columns': None,
              'autofilled_NA': 0,
              'total_values': 0,
              'out_of_range_evaluations': [],
              'out_of_range_evaluates': []
          }

      # print(evaluation_data['Leona Ellison'])        

#Read the dictionaries and complete the main dictionary with degree of completion, the evaluators and the evaluations results

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

#---------------------------ONCE BUILD. SECOND ROUND TO INITIATE DE ASSESSMENT AND COMPLETE DATA-----------------------
#TO BE INCLUDED WHNE NEEDED
        for j, k in self.__evaluation_data.items():
            
            k['full_columns'] = k['evaluation_results'].notna().sum() == 18
            k['use_columns'] = k['evaluation_results'].notna().sum() > 9
            k['removed_evaluators'] = [x for x in k['use_columns'].keys() if k['use_columns'][x]==False]
            ev_df = k['evaluation_results'].loc[:,k['use_columns']]
            k['total_values'] = ev_df.size
            k['autofilled_NA'] = ev_df.isna().sum().sum()
            #complete de evaluation df
            ev_df.fillna(method='bfill', inplace=True)
            ev_df.fillna(method='ffill', inplace=True)
            #check and remove out of range evaluators. In principle, 25% of sensibility (then, in may be a chosen option)
            df_mean = ev_df.mean().mean()
            evaluators_mean = ev_df.mean()
            check_mean = (evaluators_mean > df_mean - (0.25*df_mean)) & (evaluators_mean < df_mean + (0.25*df_mean))
            check_mean['Autoevaluación'] = True #Autoevalución must remain even if out of range
            k['out_of_range_evaluations'] = [x for x in check_mean.keys() if check_mean[x]==False]
            [self.__evaluation_data[x]['out_of_range_evaluates'].append(j) for x in k['out_of_range_evaluations']]
            #Include the questión categories in DataFrame for evaluation
            categories = ['Disposición', 'Disposición', 'Disposición', 'Propósito', 'Propósito', 'Colaboración', 'Colaboración', 'Colaboración', 'Colaboración', 'Desempeño', 'Desempeño', 'Desempeño', ' Crecimiento', 'Crecimiento','Proactividad','Proactividad','Proactividad','General']
            ev_df['categorías'] = categories
            #final DataFrame for evaluation
            k['process_results'] = ev_df

            #print(check_mean)
            #print(k['full_columns'])
            #print(k['removed_ev'])

#       

        #print(self.__evaluation_data['Kelly White'])
        #print(self.__evaluation_data['Addie Smith'])

        #self.checkplan()
#---------------------------- ADDITIONAL CHECKING WITH THE DESIGNED PLAN IN EVALUATORS.CSV FILE-------------------
###############################THERE ARE A LOT OF PRINT MESSAGES, TRASNFORM TO GUI#################

    def save_data(self):
       #Save data of each evaluation in a separate pickle file in 'archivos'. These files will serve to conduct the later comparisons among evaluations. So we extract the evaluation name with data 
      
        #read file path and extract
        def last_slash(new_path:str):
        #the functon extracts last position of slash in a path. As such, we will get evaluation
            def check_pos(ls_pos:int=0):
              return check_pos(new_path.find('/', ls_pos+1)) if new_path.find('/', ls_pos+1) != -1 else ls_pos
            return check_pos()
        
        #we get the path from any of the data. We can use the first one, for example
        names  = list(self.__evaluation_data.keys())
        
        path_of_evaluations = self.__evaluation_data[names[0]]['file_path']
        filename= self.__evaluation_data[names[0]]['file_name']
        
        #extract the general path and the name of the evaluation. The one before the last slash
        saving_path = path_of_evaluations[:last_slash(path_of_evaluations)]
        ev_name_pkl = path_of_evaluations[last_slash(path_of_evaluations)+1:].removesuffix(filename)[:-1]
        
        with open(saving_path+'/'+ev_name_pkl+'_pkl', 'wb') as fw:
          pickler = pickle.Pickler(fw)
          pickler.dump(self.__evaluation_data)
    
    def read_data(self): 

      #directory = filedialog.askdirectory(text= 'Selecciona el directorio principal (archivos)', initialdir='.')
      #files will be directly readed from the archivos files
      def check_pckl_file(dirct:str):
        return True if dirct.find('_pkl') !=-1 else False

      pkl_files = [x for x in glob.glob('./archivos/'+'/*') if check_pckl_file(x)] 
      print(pkl_files)
      past_evaluations = []
      for i in pkl_files:
        with open(i, 'rb') as fr:
          past_evaluations.append(pickle.Unpickler(fr).load())

      print(past_evaluations)
        

    def checkplan(self):

        #verification of the consistency of the logged data with the evaluators original design

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
    #test.read_directories()
    #test.save_data()
    test.read_data()