
from typing import List
import pandas as pd
import numpy as np
from pandas.core import indexing
import random
import csv

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
        

    def check_matrix(self):
    #This method reads the matrix & checks that the matrix is well build. Transposition of the matrix equals the original one
    #introduce el numbre del archivo
        
        file = 'interacciones.csv' #input("Input the name of the file: ")
        path = './archivos/{}'.format(file)
        self.__matrix = pd.read_csv(path)
        

    #Drop the column of Areas
        self.__matrix.drop(columns=['Areas','Collaborators'], axis=1, inplace=True)    
        
        
    # check that the interactions are well built. The matrix is symmetrical    
        if self.__matrix.values.all() == self.__matrix.values.T.all():
            self.__collaborators = list(self.__matrix.columns)
            self.__num_collaborators = len(self.__collaborators)
            self.read_interactions()
        else:
            print("The matrix is not symetrical. Check the interactions")
#



    def read_interactions(self):
        #We have the matrix. Now we need to rescue the contacts of each collaborator. 
        #We build a list of lists, where each collaborator is the index, and has a list with the index of the colleagues

        #First, we build a DataFrame with the same dimensions of the original and the index in each row
        def concat(mat, line):
            return np.vstack((mat,line))

        ind = np.arange(0, len(self.__collaborators))
        aux_matrix = ind
        #print(ind)
        
        for i in range(self.__num_collaborators):
            aux_matrix = concat(aux_matrix, ind)

        aux_df = pd.DataFrame(aux_matrix, columns= self.__collaborators)
        
    # we can multiply the aux_df, with the original matrix

        self.__matrix = self.__matrix * aux_df
        

    # List of lists with the index of each interaction
        self.__list_interactions = [list(self.__matrix.loc[i,:].dropna()) for i in range(self.__num_collaborators)]
    
    
    #With this list, we will build the evaluators & evaluates...
        self.set_evaluators()
    
    def set_evaluators(self):
    # Every collaborator will be evaluated by a number of evaluators. 
    # The number of evaluator will be the same for each collaborator, unless, he/she interacts with less people
    # No one will conduct more than a specified number of evaluations
        
        #In principle, we will use 10 as the default for the maximum number of evaluations self.__mx_evaluations = 10 
        #Choose de number of evaluators per persons
        while self.__mx_evaluators <3:
            self.__mx_evaluators = input("How many evaluations are required per collaborator?: \n")
            try:    
                self.__mx_evaluators = int(self.__mx_evaluators)
            except:
                print("The input has to be an integer")
            finally:
                if isinstance(self.__mx_evaluators, int):
                    if self.__mx_evaluators >= 3:
                        pass
                    else:
                        print("\nChoose at least 3 evaluator per collaborator\n")
                else:
                    self.__mx_evaluators = 0 

        #inicializar las listas self.__evaluates[] y self.__evaluators[], con su número de elementos
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
                #else:
                #    print("no quedan evaluadores ¿se acaba?")

            
            #First evaluator when the dim is 0
            evaluator = int(random.choice(colb_aux))
            self.__evaluates[evaluator].append(person_index)
            self.__evaluators[person_index].append(evaluator)
            self.__num_evaluates[evaluator] += 1
            colb_aux.remove(evaluator)  
        
            while len(self.__evaluators[person_index]) < num_evaluators and len(self.__evaluators[person_index]) < len(list_colb):
                
                if len(colb_aux) >= 1:
                    evaluator = int(random.choice(colb_aux))
                    
                    if self.__num_evaluates[evaluator] < num_evaluations: #¿cuál es la lista de evaluadores?
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

        def build_frameworks(evaluates):
            #This methof creates the files for each collaborator to conduct the evaluations
            #The evaluations consist in X simple questions to be evaluted from 1 to 4

            #We will build a DataFrame for each evaluator with the questions in row, and the evaluates in row
            #As Headline we will include name of the evaluator, date, number of evaluates and the score system

            #list of questions
            questions = [
                "¿Tiene una disposición constructiva orientada a solucionar problemas sin prejuicios ni opiniones preconcebidas?",
                "¿Contribuye a que haya un ambiente positivo de trabajo y evita los chismes, rumores y políticas perniciosos?",
                "¿Se conduce con respeto a los compañeros de Natura sin ser ofensivo?",
                "¿Tiene actitud analítica respecto de los problemas, aporta perspectiva y considera los objetivos del equipo o la empresa?",
                "¿Antepone los objetivos grupales o de equipo a los personales?",
                "¿Tiene disposición a consultar y pedir consejo y opinión a los demás, admitiendo otras sugerencias y puntos de vista?",
                "¿Agradece la contribución a los compañeros y colaboradores y reconoce sus méritos?",
                "¿Se ofrece y se involucra en las problemáticas de los demás?",
                "¿Escucha a los demás y admite otras sugerencias y puntos de vista?",
                "¿Sus tareas las realiza en tiempo?",
                "¿Domina los aspectos técnicos de sus trabajo?",
                "¿Es concienzudo en su desempeño y se preocupa de asegurar y mejorar la calidad en cuanto hace?",
                "¿Tiene disposición a crecer y formarse de manera continua?",
                "¿Comparte sus conocimientos y colabora en la formación de los demás?",
                "¿Hace propuestas y sugerencias de mejora?",
                "¿Se implica en las mejoras, tiene iniciativa y emprende acciones aunque no se le hayan solicitado?",
                "¿Anima y motiva a los demás a participar y hacer propuestas?",
                "Teniendo todo en cuenta ¿cómo valoraría el compromiso y las contribución del colaborador a los objetivos globales, como equipo y como empresa?"
            ]
        
            for i in range(self.__num_collaborators):
                form = pd.DataFrame(index=questions, columns=evaluates[i][1:])
                print(form)
                evaluator = evaluates[i][0]
                path = './archivos/Evaluaciones/{}_form.csv'.format(evaluator)    
                form.to_csv(path, header=True, index=True, encoding='utf-8-sig')            


        for i in range(self.__num_collaborators):
            random_evaluators(self.__list_interactions[i], i,self.__mx_evaluators, self.__mx_evaluations) #no need to pass general parameters
        

        def prepare_4_writing(list_of_people):
            #This function introduces the evaluate & evaluators in the first position of the lists and turn index into the actual names
            first_list =list_of_people.copy()
            [first_list[i].insert(0, i) for i in range(self.__num_collaborators)] # inserts the evaluate or evaluator
            list4writing = [list(map(lambda x: self.__collaborators[x], first_list[i])) for i in range(self.__num_collaborators)]
            return list4writing
           

        with open('./archivos/evaluations.csv', 'w', newline='') as ev_file:
            map_evaluations = csv.writer(ev_file)
            map_evaluations.writerow(['This file includes de evaluations to be conducted by each collaborator'])
            map_evaluations.writerow(['Evaluator','Evaluates'])
            map_evaluations.writerows(prepare_4_writing(self.__evaluates))
        
        with open('./archivos/evaluators.csv', 'w', newline='') as evt_file:
            map_evaluations = csv.writer(evt_file)
            map_evaluations.writerow(['This file includes de evaluators of each collaborator'])
            map_evaluations.writerow(['Collaborator','Evaluators'])
            map_evaluations.writerows(prepare_4_writing(self.__evaluators))
        
        build_frameworks(prepare_4_writing(self.__evaluates))

    def fill_evaluations(self):
        #This function sets a randomly list of grades for each of the question in the forms according to randomly selected scores
        #For consistency, employees respond to different types of behabiours
        types_of_employees = ["bad", "average", "good"]
        self.cont = 0
        grades = []
        print("hola")

        #ranges of score
        
        def score(empl_type, type):     

            def wrapper():        
                
                if type == 4:
                    return 4
                elif type == 3:
                    return random.randint(3,4)
                elif type == 2:
                    return random.randint(1,2)
                elif type == 1:
                    return 1
            return wrapper
                        
        #randomly chooses a type of employee
        type_of_employee = random.choice(types_of_employees)
        
        for i in range(1, 19):
            if i % 3 == 0 or i == 1:
                if type_of_employee == "good":
                    type_range = random.randint(3,4)
                elif type_of_employee =="average":
                    type_range = random.randint(2,3)
                else:
                    type_range = random.randint(1,2)       
            results = score(type_of_employee, type_range)
            grades.append(results())
        
        print("El empleado es ", type_of_employee)
        print(grades)
        

if __name__ == '__main__':

    test1 = Evaluation()
    test1.fill_evaluations()



        #There are 18 question. Every 3 questions, the level of score changes ramdomly
        # If good employee, level of score may be 3 or for
        # # IF average, level of score 2 or 3
        # if bad, leve 1 or 2




                
        

    