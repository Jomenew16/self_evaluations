
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
        self.thispath = os.getcwd()

#------------------------- General tools -------------------------------------------------------

    def identify_string (self, path_file: str, string_str) -> bool:
      #identify is a string (file) has a certain substring
          return True if path_file.find(string_str) !=-1 else False
    
    def get_file_name(self, file, len_dir):
      #given a full path and the lenth of the directory, extracts the name of the file
      return file[len_dir:]   
    
    #def get_ev_directory_name(self, file_path: str, file_name: str) -> str:
    ##given a full path and the name of the file, extracts the name of the directory
    #  return file_path.removesuffix(file_name)
#---------------------------------Read the last evaluation in the archivos directory------------------
    
    def read_directories(self):
        #print("aquí tamos")
        #read the last evaluation directory from /archivos
          

        #distinguish directories and files, for we have to find the last directory
        thisdir = os.getcwd()
        #ev_files = [os.path.join(r, file) for r,d,f in os.walk('./archivos') for file in f]
        #identify directories with with *_Evaluacion_* in the name
        directories = [direct for r,d,f in os.walk(thisdir + '/archivos') for direct in d if self.identify_string(direct,'_Evaluacion_')]
        #filename =filedialog.askdirectory(title="Selecciona el directorio de la evaluación actual", initialdir='./archivos')
        last_evaluation_path = thisdir+'/archivos/'+ max(directories)
        #last_evaluation_path = (thisdir+'/archivos/'+ max(directories)).replace('\\','/')
        
        ev_files = [x for x in glob.glob(last_evaluation_path+'/*.csv')]
   
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
              'file_name': self.get_file_name(file, len(last_evaluation_path) + 1),
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
              try:
                self.__evaluation_data[n]['evaluators'].append(j)
                self.__evaluation_data[n]['evaluation_results'][j]= list(k['log_data'][n])
              except:
                messagebox.showinfo('Aviso', f'Puede haber un problema con la evaluación de {j}')
                continue

#---------------------------ONCE BUILD. SECOND ROUND TO INITIATE DE ASSESSMENT AND COMPLETE DATA-----------------------
#TO BE INCLUDED WHNE NEEDED
        for j, k in self.__evaluation_data.items():
            
            k['full_columns'] = k['evaluation_results'].notna().sum() == 18
            k['use_columns'] = k['evaluation_results'].notna().sum() > 9
            k['use_columns']['Autoevaluación'] = True  #even if blank selfevaluation must remain
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
            ev_df=ev_df.loc[:,check_mean]
            #Include the questión categories in DataFrame for evaluation
            categories = ['Disposición', 'Disposición', 'Disposición', 'Propósito', 'Propósito', 'Colaboración', 'Colaboración', 'Colaboración', 'Colaboración', 'Desempeño', 'Desempeño', 'Desempeño', ' Crecimiento', 'Crecimiento','Proactividad','Proactividad','Proactividad','General']
            ev_df['categorías'] = categories
            #final DataFrame for evaluation
            k['process_results'] = ev_df.copy(deep=True)

#       

        #print(self.__evaluation_data['Debra Brown'])
        #print(self.__evaluation_data['Addie Smith'])

        #self.checkplan()
#---------------------------- ADDITIONAL CHECKING WITH THE DESIGNED PLAN IN EVALUATORS.CSV FILE-------------------
###############################THERE ARE A LOT OF PRINT MESSAGES, TRASNFORM TO GUI#################

    @property
    def evaluation_data(self):
      return self.__evaluation_data


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
        
        with open(saving_path+'/1_archivos de trabajo/'+ev_name_pkl+'_pkl', 'wb') as fw:
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
        

#----------------------------Submenu 1. Preliminary checking of the evaluation data with the design. Files are complete---------------
    def checkplan(self):

        #this function compares 2 sets. If they are equal, returns True, else False
        def check_sets(set1, set2):
        #this function compares 2 sets. If they are equal, returns True, else False
          return len(set1 - set2) == 0
        
        
    #First set for comparison. All the names logged, who has the evaluation form in the evaluation forms directory

        set_dict = set(self.__evaluation_data.keys())

        thisdir = os.getcwd()

        path_of_design = thisdir+'/archivos/0_Diseños de evaluación/'
        rd_file = random.choice(list(set_dict)) #just obtain one person to extract file name
        ev_directory = self.__evaluation_data[rd_file]['file_path'][0:len(thisdir+'/archivos/')+20]
        directory_name =ev_directory[-20:]
        path_evaluators = path_of_design + directory_name[0:6] + '_evaluators_v' + directory_name[-1:]+'.csv'


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
          num_formulariosCheck = True
          #num_formulariosCheck = "Número de formularios: OK"
        else:
          num_formulariosCheck = False
          #num_formulariosCheck = "El número de formularios no coincide con el plan"

        #print(len(set_dict - list_of_collabs))

        #Check that the results files are consistent with the archive of evaluators
        problematic_evaluation = []
        inconsist = 0 
        for line in reading:
          if check_sets(set(line[1:]), set(self.__evaluation_data[line[0]]['evaluation_results'].columns)) == False:
            inconsist +=1
            diff = list(set(line[1:]) ^ set(self.__evaluation_data[line[0]]['evaluation_results'].columns))
            for i in diff:
              if i != 'Autoevaluación':
                problematic_evaluation.append(i)

            #problematic_evaluation.append(line[0])

        if inconsist != 0:
          evaluatorsCheck = False
          #evaluatorsCheck= f'Hay una inconsistencia en {consist} archivos de evaluación'
        else:
          evaluatorsCheck = True
          #evaluatorsCheck = "Comprobación de evaluadores: OK"
        
        return num_formulariosCheck, evaluatorsCheck, problematic_evaluation

#----------------------------Submenu 1. Create first check stats and graphs---------------

    def create_first_check_submenu_stats(self):
      #Determinar el porcentaje de completos
      completed = 0
      semicompleted = 0
      semiempties = 0
      empties = 0
      #compile de list of collaborators, to later build de graphs
      colabs = []
      pctg = [] 

      for j, k in self.__evaluation_data.items():
        colabs.append(j)
        pctg.append(k['completion'])
        if k['completion'] == 0:
          empties +=1
        elif k['completion'] < 50:
          semiempties +=1
        elif k['completion'] < 100:
          semicompleted +=1
        else:
          completed +=1

      # pie graph with the formats that are completed, semicompleted, semiempties or empties
      num_filled = [empties, semiempties, semicompleted, completed]
      cat_filled = ['Vacíos', 'Semivacíos', 'Semicompletos', 'Completos']
      colors = ['#FF0000','#FF9000','#C3DB0F','#62EF04']
      offset = (0.1,0.1,0,0)
      plt.figure(figsize=(2,2))
      plt.pie(num_filled,labels = cat_filled, autopct="%0.1f %%",  colors = colors, explode = offset, textprops={'fontsize':6})
      plt.axis("equal")
      thispath = os.getcwd()

      plt.savefig(thispath + '/archivos/1_archivos de trabajo/S1F2_pieCompletion.png', bbox_inches = 'tight')
      
      plt.clf()

      sort_completion = pd.DataFrame(index= colabs)
      sort_completion['Pct'] = pctg
      sort_completion.sort_values('Pct', ascending=False, inplace=True)

      #print(sort_completion.index)
      plt.figure(figsize=(5,3))
      plt.barh(sort_completion.index, sort_completion['Pct'], height=0.8, color = 'blue')
      plt.xticks(fontsize=6)
      plt.yticks(fontsize=6)
      plt.xlabel("Porcentaje de cumplimentación")
      #plt.ylabel("Colaboradores")
      #plt.title("Porcentaje de avance")
      plt.savefig(thispath + '/archivos/1_archivos de trabajo/S1F3_hbars_completion.png', bbox_inches = 'tight')
      
      plt.clf()


    def create_second_allcollabs_submenu_stats(self):

      colabs_mean = []
      colabs = []
      for j, k in self.__evaluation_data.items():
        collabs_df = k['process_results'].drop(['Autoevaluación'], axis=1).copy(deep=True)
        print(collabs_df)
        colabs_mean.append(collabs_df.mean().mean())
        colabs.append(j)

      sort_collabs = pd.DataFrame(index=colabs)
      sort_collabs['means'] = colabs_mean
      sort_collabs.sort_values('means', ascending=False, inplace=True)

      plt.figure(figsize=(6,3))
      plt.bar(sort_collabs.index, sort_collabs['means'], width=0.8)
      plt.xticks(rotation=90, fontsize=7)
      plt.yticks(rotation=90, fontsize=7)
      plt.title('Media global por colaborador', fontdict={'fontsize': 11})
      plt.savefig(self.thispath + '/archivos/1_archivos de trabajo/S2F1_bar_allCollabs.png', bbox_inches = 'tight')

      
#if __name__ == '__main__':
 #   test = EvaluationsAssessment()
    #test.read_directories()
    #test.save_data()
  #  test.read_data()