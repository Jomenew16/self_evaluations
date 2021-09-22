
import pandas as pd
import numpy as np
from pandas.core import indexing

class Evaluation:
 

    def __init__(self) -> None:
    # parameter evaluators represents the desired number of evaluators of each collaborator. 
    # max_evaluations is the maximum number of evaluations that each colaborator will make. 
        self.__mx_evaluators: int = 0
        self.__mx_evaluations:int = 0
        self.__evaluators = [] #It is a list o lists. Index number of people by whom the person on each index is evaluated
        self.__evaluates = [] #It is a list of list. Index number of people who evaluates the person
        self.__matrix: pd.DataFrame
        self.__collaborators = [] #list of all the collaborators in the order of the original matrix
        self.__list_interactions = []
        

    def check_matrix(self):
    #This method reads the matrix & checks that the matrix is well build. Transposition of the matrix equals the original one
    #introduce el numbre del archivo
        
        file = 'interacciones.csv' #input("Input the name of the file: ")
        path = './archivos/{}'.format(file)
        print(path)
        self.__matrix = pd.read_csv(path)
        

    #Drop the column of Areas
        self.__matrix.drop(columns=['Areas','Collaborators'], axis=1, inplace=True)    
        print(self.__matrix)
        
    # check that the interactions are well built. The matrix is symmetrical    
        if self.__matrix.values.all() == self.__matrix.values.T.all():
            print("The matrix is symmetrical")
            self.__collaborators = list(self.__matrix.columns)
            print(self.__collaborators)
            self.read_interactions()
        else:
            print("The matrix is not symetrical. Check the interactions")
#

    def set_evaluators(self, evaluators, mx_evaluations):
    # Every collaborator will be evaluated by a number of evaluators. 
    # The number of evaluator will be the same for each collaborator, unless, he/she interacts with less people
    # No one will conduct more than a specified number of evaluations
        pass

    def read_interactions(self):
        #We have the matrix. Now we need to rescue the contacts of each collaborator. 
        #We build a list of lists, where each collaborator is the index, and has a list with the index of the colleagues

        #First, we build a DataFrame with the same dimensions of the original and the index 
        def concat(mat, line):
            return np.vstack((mat,line))

        ind = np.arange(0, len(self.__collaborators))
        aux_matrix = ind
        print(ind)
        
        for i in range(len(self.__collaborators)):
            aux_matrix = concat(aux_matrix, ind)

        aux_df = pd.DataFrame(aux_matrix, columns= self.__collaborators)
        print(aux_df)    

    # we can multiply the aux_df, with the original matrix

        self.__matrix = self.__matrix * aux_df
        print(self.__matrix)

    # List of lists with the index of each interaction
        self.__list_interactions = [list(self.__matrix.loc[i,:].dropna()) for i in range(len(self.__collaborators))]
        print(self.__list_interactions)
    
    #With this list, we will build the evaluators & evaluates...


        

ev1 = Evaluation()
ev1.check_matrix()  
    