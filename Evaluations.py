
from typing import List
import pandas as pd
import numpy as np
from pandas.core import indexing
import random
import csv
import copy
import os
from pathlib import Path
from datetime import datetime, time
from tkinter import filedialog
from tkinter import *
import glob
from tkinter import messagebox


class Evaluation:
 

    def __init__(self) -> None:
    # parameter evaluators represents the desired number of evaluators of each collaborator. 
    # max_evaluations is the maximum number of evaluations that each colaborator will make. 
        self.__mx_evaluators: int = 0
        self.__mx_evaluations:int = 10 #each person will conduct a maximum of 10 evaluations, a few more are required to complete the number of evaluations per person
        self.__evaluators =[]  #It is a list o lists. Index number of people by whom the person on each index is evaluated
        self.__evaluates =[] #It is a list of list. Index number of people who evaluates the person
        
        self.__matrix: pd.DataFrame
        self.__collaborators = [] #list of all the collaborators in the order of the original matrix
        self.__num_collaborators: int
        self.__list_interactions = []
        self.__list_areas= []
        
#-----------------------read the interactions matrix---------------------------------------

    def check_matrix(self, num_evaluators):
    #This method reads the matrix & checks that the matrix is well build. Transposition of the matrix equals the original one
    #introduce el numbre del archivo
        
        #%gui tk
        raiz = Tk()
        raiz.withdraw()
        file_path =filedialog.askopenfilename(title="Seleccione el archivo de interacciones", initialdir='./archivos')
        
        raiz.destroy()
        
        self.__matrix = pd.read_csv(file_path)

        self.__list_areas = self.__matrix['Areas']

    #Drop the column of Areas
        self.__matrix.drop(columns=['Areas','Collaborators'], axis=1, inplace=True)    
        
        
    # check that the interactions are well built. The matrix is symmetrical    
        if self.__matrix.values.all() == self.__matrix.values.T.all():
            self.__collaborators = list(self.__matrix.columns)
            self.__num_collaborators = len(self.__collaborators)
            
            self.read_interactions(num_evaluators)
        else:
            messagebox.showwarning('??Aviso!', 'La matriz no es sim??trica. Comprueba las interacciones')
            


    def read_interactions(self, num_evaluators):
        #We have the matrix. Now we need to rescue the contacts of each collaborator. 
        #We build a list of lists, where each collaborator is the index, and has a list with the index of the colleagues

        #First, we build a DataFrame with the same dimensions of the original and the index in each row
        def concat(mat, line):
            return np.vstack((mat,line))

        ind = np.arange(0, len(self.__collaborators))
        aux_matrix = ind

        
        for i in range(self.__num_collaborators):
            aux_matrix = concat(aux_matrix, ind)

        aux_df = pd.DataFrame(aux_matrix, columns= self.__collaborators)
        
    # we can multiply the aux_df, with the original matrix

        self.__matrix = self.__matrix * aux_df
        

    # List of lists with the index of each interaction
        self.__list_interactions = [list(self.__matrix.loc[i,:].dropna()) for i in range(self.__num_collaborators)]
    
    
    #With this list, we will build the evaluators & evaluates...
        self.set_evaluators(num_evaluators)

#------------------------------- random selection of the evaluators --------------------------

    def set_evaluators(self, num_evaluators):
        self.__mx_evaluators = num_evaluators
        
        
    # Every collaborator will be evaluated by a number of evaluators. 
    # The number of evaluator will be the same for each collaborator, unless, he/she interacts with less people
    # No one will conduct more than a specified number of evaluations
        

        #inicializar las listas self.__evaluates[] y self.__evaluators[], con su n??mero de elementos
        self.__evaluates = [[] for i in range(0,self.__num_collaborators)] 
        self.__evaluators = [[] for i in range(0,self.__num_collaborators)]
        self.__num_evaluates = [0] * self.__num_collaborators #Num of evaluates of each evaluator (it will help to prioritize those who has less evaluations)
        
        #For each position (collaborator), in the list self.__list_interactions, choose a random evaluator while
        #cond 1. the number of evaluator is less than self.__mx_evaluators
        #cond 2. The evaluator is conducting to many evaluations
        #cond 3. When a person is chosen, drop it from the list, so it is not repeated 
        #first, we will be build a function that receives the list, number of evaluations and number of evaluators and does the selection

#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        def random_evaluators(list_colb: list, person_index: int, num_evaluators: int, num_evaluations: int):
            colb_aux=list_colb.copy()
            top_evaluators = []

            def filter_min(list_top_evaluators, number_evaluates):
                #this function receives the evaluators who have more than the top number of evaluates and choses 1 with the minimum number among them
                if len(list_top_evaluators) > 1:
                    num_eval = [number_evaluates[i] for i in list_top_evaluators] #a list with number of evaluates of the top evaluators
                    min_eval = min(num_eval) #provides de minimum number of evaluates among the top evaluators
                    final_min =  [list_top_evaluators[k] for k,v in enumerate(num_eval) if v == min_eval] # a list with the top evaluators with less evaluates
                    
                    return random.choice(final_min)
                else:
                    return list_top_evaluators[0]

            #First evaluator when the dim is 0
            evaluator = int(random.choice(colb_aux))
            self.__evaluates[evaluator].append(person_index)
            self.__evaluators[person_index].append(evaluator)
            self.__num_evaluates[evaluator] += 1
            colb_aux.remove(evaluator)  
        
            while len(self.__evaluators[person_index]) < num_evaluators and len(self.__evaluators[person_index]) < len(list_colb):
                
                if len(colb_aux) >= 1:
                    evaluator = int(random.choice(colb_aux))
                    
                    if self.__num_evaluates[evaluator] < num_evaluations: #??cu??l es la lista de evaluadores?
                        self.__evaluates[evaluator].append(person_index)
                        self.__evaluators[person_index].append(evaluator)
                        self.__num_evaluates[evaluator] += 1
                        colb_aux.remove(evaluator)    
                    elif self.__num_evaluates[evaluator] == num_evaluations:
                        top_evaluators.append(evaluator)
                        colb_aux.remove(evaluator)
                    else:
                        colb_aux.remove(evaluator)

                elif len(top_evaluators) >= 1:
                #if len(colb_aux) is 0: #there are no collaborators in the original list, we check the new list with those calobarators with more evaluates
                #top_evaluator have the people with more evaluates than originally capped. 
                ##among the top evaluators, we will chose those with less evaluates using __num_evaluates
                    evaluator = filter_min(top_evaluators, self.__num_evaluates)
                    self.__evaluates[evaluator].append(person_index)
                    self.__evaluators[person_index].append(evaluator)
                    self.__num_evaluates[evaluator] += 1
                    top_evaluators.remove(evaluator)
                else:
                    break


#-------------------------------- build the evaluation forms --------------------------
        
        def build_forms(evaluates, time, vers):
            #This method creates the files for each collaborator to conduct the evaluations
            #The evaluations consist in X simple questions to be evaluted from 1 to 4

            #We will build a DataFrame for each evaluator with the questions in row, and the evaluates in row
            #As Headline we will include name of the evaluator, date, number of evaluates and the score system

            #list of questions
            questions = [
                "??Tiene una disposici??n constructiva orientada a solucionar problemas sin prejuicios ni opiniones preconcebidas?",
                "??Contribuye a que haya un ambiente positivo de trabajo y evita los chismes, rumores y pol??ticas perniciosos?",
                "??Se conduce con respeto a los compa??eros de Natura sin ser ofensivo?",
                "??Tiene actitud anal??tica respecto de los problemas, aporta perspectiva y considera los objetivos del equipo o la empresa?",
                "??Antepone los objetivos grupales o de equipo a los personales?",
                "??Tiene disposici??n a consultar y pedir consejo y opini??n a los dem??s, admitiendo otras sugerencias y puntos de vista?",
                "??Agradece la contribuci??n a los compa??eros y colaboradores y reconoce sus m??ritos?",
                "??Se ofrece y se involucra en las problem??ticas de los dem??s?",
                "??Escucha a los dem??s y admite otras sugerencias y puntos de vista?",
                "??Sus tareas las realiza en tiempo?",
                "??Domina los aspectos t??cnicos de sus trabajo?",
                "??Es concienzudo en su desempe??o y se preocupa de asegurar y mejorar la calidad en cuanto hace?",
                "??Tiene disposici??n a crecer y formarse de manera continua?",
                "??Comparte sus conocimientos y colabora en la formaci??n de los dem??s?",
                "??Hace propuestas y sugerencias de mejora?",
                "??Se implica en las mejoras, tiene iniciativa y emprende acciones aunque no se le hayan solicitado?",
                "??Anima y motiva a los dem??s a participar y hacer propuestas?",
                "Teniendo todo en cuenta ??c??mo valorar??a el compromiso y las contribuci??n del colaborador a los objetivos globales, como equipo y como empresa?"
            ]

            path = './archivos/{}_Evaluacion'.format(time.strftime('%Y%m%d')[2:]) + '_v' + str(vers)
            Path(path).mkdir(parents=True, exist_ok=True)
            for i in range(self.__num_collaborators):
                #form = pd.DataFrame(index=questions, columns=evaluates[i][0:])
                form = pd.DataFrame(columns=evaluates[i][0:])
                form['Preguntas'] = questions
                form.rename(columns={evaluates[i][0]: evaluates[i][0] + ' (Autoevaluaci??n)'}, inplace=True)
                form.set_index(['Preguntas'], inplace=True)
                evaluator = evaluates[i][0]
                path1 = path + '/{}_form.csv'.format(evaluator)    

                with open(path1, 'w', newline='', encoding='utf-8-sig') as ev_file:
                    file = csv.writer(ev_file)
                    file.writerow(["Evaluador:", evaluator])
                    file.writerow(["Date:", time.strftime('%d/%m/%Y')])
                    file.writerow(["Area:", self.__list_areas[i]])
                    file.writerow([])
                    file.writerow(['INSTRUCCIONES'])
                    file.writerow(['Cumplimenta con valores del 1 al 5, donde 1 representa "Totalmente en desacuerdo" y 5 "Totalmente de acuerdo"'])
                    file.writerow(['Si te faltan elementos de juicio para evaluar alg??n aspecto o a alg??n colaborador, deja la/s casilla/s en blanco'])
                    file.writerow([])
                    file.writerow(['EVALUACI??N'])
                    file.writerow([])
                form.to_csv(path1, header=True, index=True, mode='a', encoding='utf-8-sig')            


            #with open(path + '/' + evaluators_day_name + '.csv', 'w', newline='') as evt_file:
                ##map_evaluations = csv.writer(evt_file)
                ##map_evaluations.writerow(['This file includes de evaluators of each collaborator'])
                ##map_evaluations.writerow(['Collaborator','Evaluators'])
                #map_evaluations.writerows(prepare_4_writing(self.__evaluators))



        for i in range(self.__num_collaborators):
            random_evaluators(self.__list_interactions[i], i,self.__mx_evaluators, self.__mx_evaluations) #no need to pass general parameters
        

        def prepare_4_writing(list_of_people):
            #This function introduces the evaluate & evaluators in the first position of the lists and turn index into the actual names
            first_list =copy.deepcopy(list_of_people)
            [first_list[i].insert(0, i) for i in range(self.__num_collaborators)] # inserts the evaluate or evaluator
            list4writing = [list(map(lambda x: self.__collaborators[x], first_list[i])) for i in range(self.__num_collaborators)]
            return list4writing


        mydatetime = datetime.now()
        path = "./archivos/0_Dise??os de evaluaci??n"
        Path(path).mkdir(parents=True, exist_ok=True)

        #if the file already exists, add subsequent versions
        evaluation_files = os.listdir(path)
        version = 0
        evaluations_day_name = '{}_evaluations'.format(mydatetime.strftime('%Y%m%d')[2:]) + '_v' + str(version)
        evaluators_day_name = '{}_evaluators'.format(mydatetime.strftime('%Y%m%d')[2:]) + '_v' + str(version)
    
        while evaluations_day_name + '.csv' in evaluation_files:
            version +=1 
            evaluations_day_name = evaluations_day_name[:-1] + str(version)
            evaluators_day_name = evaluators_day_name[:-1] + str(version)
            
        
        with open(path + '/' + evaluations_day_name + '.csv', 'w', newline='', encoding='utf-8-sig') as ev_file:
            map_evaluations = csv.writer(ev_file)
            map_evaluations.writerow(['This file includes de evaluations to be conducted by each collaborator'])
            map_evaluations.writerow(['Evaluator','Evaluates'])
            map_evaluations.writerows(prepare_4_writing(self.__evaluates))
        

        with open(path + '/' + evaluators_day_name + '.csv', 'w', newline='', encoding='utf-8-sig') as evt_file:
            map_evaluations = csv.writer(evt_file)
            map_evaluations.writerow(['This file includes de evaluators of each collaborator'])
            map_evaluations.writerow(['Collaborator','Evaluators'])
            map_evaluations.writerows(prepare_4_writing(self.__evaluators))

        build_forms(prepare_4_writing(self.__evaluates), mydatetime, version)

    def person_evaluation(self):
        #This function sets a randomly list of grades for each of the question in the forms according to randomly selected scores
        #For consistency, employees respond to different types of behabiours
        types_of_employees = ["bad", "average", "good"]
        self.cont = 0
        grades = []

        #ranges of score

        def score(type):         
            #def wrapper():        
            if type == 4:
                return random.randint(4,5)
            elif type == 3:
                return random.randint(3,4)
            elif type == 2:
                return random.randint(2,3)
            elif type == 1:
                return random.randint(1,2)
            #return wrapper

        #randomly chooses a type of employee
        type_of_employee = random.choice(types_of_employees)

        for i in range(1, 19): #along the questions, the grades may change a step every 3-4 questions, depending on the general type of employee
            if i % 3 == 0 or i == 1:
                if type_of_employee == "good":
                    type_range = random.randint(3,4)
                elif type_of_employee =="average":
                    type_range = random.randint(2,3)
                else:
                    type_range = random.randint(1,2)       
            
            grades.append(score(type_range))
            #results = score(type_of_employee, type_range)
            #grades.append(results())

        return grades   
    
    
    def autoevaluations(self):

        raiz = Tk()
        raiz.withdraw()    
        filename =filedialog.askdirectory(title="Selecciona el directorio con los formularios de evaluaci??n sin cumplimentar", initialdir='./archivos')
        raiz.destroy()
        if filename:
            messagebox.showinfo('??Excelente!','Los archivos ya se est??n rellenando')
            files_names = [x for x in glob.glob(filename + '/*.csv') if x.endswith(".csv")]


            for file in files_names:

                df_aux = pd.read_csv(file, skiprows=10, encoding='utf-8-sig')

                for i in range(len(df_aux.columns)-1):
                    score = self.person_evaluation()
                    for j,k in enumerate(score):
                        df_aux.iloc[j,i+1] = k
                #df_aux.rename(columns={'Unnamed: 0': 'Preguntas'}, inplace=True)

                row=[]
                with open(file,'r',newline='', encoding='utf-8-sig') as editfile:
                    readfile = csv.reader(editfile)                                        
                    for i in range(1,11):
                        row.append(next(readfile))


                with open(file,'w',newline='', encoding='utf-8-sig') as editfile:
                    writefile = csv.writer(editfile)
                    for i in range(10):
                        writefile.writerow(row[i])

                df_aux.to_csv(file, index = False, mode='a', encoding='utf-8-sig') 

# ----------------------------------------- Assessment ----------------------------
# 
    #def assessment():
    #    
    #    filename =filedialog.askdirectory(title="Selecciona el directorio de la evaluaci??n actual", initialdir='./archivos')
    #    files_names = [x for x in glob.glob(filename + '/*.csv') if x.endswith(".csv")]   
        
                
#if __name__ == '__main__':
#    ev = Evaluation()
#    ev.check_matrix()

