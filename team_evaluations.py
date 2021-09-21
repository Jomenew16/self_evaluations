

from Sim_company import Sim_comp

def menu():
    menu =int(input("""¿Qué desea hacer?:
    1. Create a new company \n"""))

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
    option = menu()

# if menu == 1 set matrix
    if option == 1:

    
        Company = Sim_comp()
        Company.set_company()
        
        #Company.set_areas()
        #Company.build_interactions()

    else:
        pass

