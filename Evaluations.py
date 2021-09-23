
from typing import List
import pandas as pd
import numpy as np
from pandas.core import indexing
import random

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
        print(self.__matrix)
        
    # check that the interactions are well built. The matrix is symmetrical    
        if self.__matrix.values.all() == self.__matrix.values.T.all():
            print("The matrix is symmetrical")
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
        print(self.__list_interactions)
    
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
        self.__evaluates = [[]] * self.__num_collaborators
        self.__evaluators = [[]] * self.__num_collaborators
        self.__num_evaluates = [0] * self.__num_collaborators #Num of evaluates of each evaluator (it will help to prioritize those who has less evaluations)
        print(self.__evaluates)
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
                num_eval = [number_evaluates[i] for i in list_top_evaluators] #a list with number of evaluates of the top evaluators
                min_eval = min(num_eval) #provides de minimum number of evaluates among the top evaluators
                final_min =  [list_top_evaluators[k] for k,v in enumerate(num_eval) if v == min_eval] # a list with the top evaluators with less evaluates
                if len(final_min) > 1:
                    return random.choice(final_min)
                else:
                    return int(final_min)

            if len(self.__evaluators[person_index]):
                while len(self.__evaluators[person_index]) < num_evaluators or len(self.__evaluators[person_index]) < len(list_colb):

                    evaluator = int(random.choice(colb_aux))
                    print("aquí: ", colb_aux)
                    print("más: ",evaluator)

                    if len(colb_aux) == 0: #there are no collaborators in the original list, we check the new list with those calobarators with more evaluates
                    #top_evaluator have the people with more evaluates than originally capped. 
                    ##among the top evaluators, we will chose those with less evaluates using __num_evaluates
                        evaluator = filter_min(top_evaluators, self.__num_evaluates)
                        self.__evaluates[evaluator].append(person_index)
                        self.__evaluators[person_index].append(evaluator)
                        self.__num_evaluates[evaluator] += 1
                        top_evaluators.remove(evaluator)

                    elif self.__num_evaluates[evaluator] < num_evaluations: #¿cuál es la lista de evaluadores?
                        self.__evaluates[evaluator].append(person_index)
                        self.__evaluators[person_index].append(evaluator)
                        self.__num_evaluates[evaluator] += 1
                        colb_aux.remove(evaluator)    

                    elif self.__num_evaluates[evaluator] == num_evaluations:
                        top_evaluators.append(evaluator)
                        colb_aux.remove(evaluator)
            else:
                evaluator = int(random.choice(colb_aux))
                self.__evaluates[evaluator].append(person_index)
                self.__evaluators[person_index].append(evaluator)
                self.__num_evaluates[evaluator] += 1
                colb_aux.remove(evaluator)    




        for i in range(self.__num_collaborators):
            random_evaluators(self.__list_interactions[i], i,self.__mx_evaluators, self.__mx_evaluations) #no need to pass general parameters
        
        print(f'Evaluates {self.__evaluates}')
        print(f'Evaluators: {self.__evaluators}')
    #self.__evaluators = [] #It is a list o lists. Index number of people by whom the person on each index is evaluated
    #self.__evaluates = [] #It is a list of list. Index number of people who evaluates the person
        

ev1 = Evaluation()
ev1.check_matrix()  
    