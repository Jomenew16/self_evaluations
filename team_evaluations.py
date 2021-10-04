

from Sim_company import Sim_comp
from Evaluations import *

def menu():
    menu =int(input("""¿What do you want to do?:
    1. Simulate a new company \n
    2. Setup the team evaluations\n
    3. Fill autoevaluations\n
    4. Exit program\n"""))

    return menu
    
    
    #We will requests the data to set the matrix, read matrix, etc
    #1 create matrix
        #Data: number of employees
    #2 read matrix
    #3 New evaluation
       #2.1 Evaluations by employee
       #2.2 Evaluators of an employeer
       #2.3 set forms
     
    pass


if __name__ == '__main__':

# Read menu
    option = 0
    while option != 4:
        option = menu()

    # if menu == 1 set matrix
        if option == 1:

            Company = Sim_comp()
            Company.set_company()

            #Company.set_areas()
            #Company.build_interactions()

        elif option == 2:
            ev1 = Evaluation()
            ev1.check_matrix()  
        
        elif option == 3:
            test1 = Evaluation()
            test1.autoevaluations()


