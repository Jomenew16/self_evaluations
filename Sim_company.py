# This module helps create a made-up company, including different departments, a defined number of employeers, hierarchies and business areas
import names
import random

class Sim_comp():

    # Rules of assigment: Production (40% of employees) General management (Max(1%,1)) Administration (20%) 
    #  Talent (Max(2%, 1)) Sales (Max(4%,1)), Accounts(Max(0.5%,1)), Purchasing(Max(0,5%),1), 
    # IT(Max(2%,1)), R&D (Max(3%,1), Engineering(3%,1), Legal(Max(1%,1)), Customer service(Max(1%,1), 
    # After sales(Max(1%,1)))    
    num_collaborators: int = 0
    _people = []
    departments = ['Production', 'General management','Administration', 'Talent', 'Sales', 'Accounts', 
    'Purchasing', 'IT', 'R&D', 'Engineering', 'Legal', 'Customer service', 'After sales']
    #_dept includes de sets of people. _dept_nums just includes and integer with the amount of people
    _dept = {}
    _dept_nums = {}


    def __init__(self) -> None:
        pass
 
    
    def set_people(self):
        
        self.num_collaborators = int(input("How many collaborators are there: "))
        assert self.num_collaborators > 0, "The number of collaborators has to be a positive number"
        self._people = [names.get_full_name() for i in range(self.num_collaborators)]    
        print(self._people)
    

    def set_areas(self):
    # Tis method builds a random matriz of interactions.
    #iniciates the dictionary with the different departments and the sets of people blank
    #initiates a sencond dictionario with the number of collaborators in each area
        for i in range(len(self.departments)):
            self._dept[self.departments[i]] = set()
            self._dept_nums[self.departments[i]] = 0
        print(self._dept)
        print(self._dept_nums)

    
    # Rceives the number of all collaborators. module names provide random list of names
        assert self.num_collaborators > 0, "There must be at least one collaborator. Apply set_people method() to create a list of people"
        ourpeople = list(range(self.num_collaborators))
        people = self.num_collaborators



    # Assign people to different areas. We will generate in order, so the results will be organized by area    
    # Rules of assigment: Production (40% of employees) General management (Max(1%,1)) Administration (20%)  
    # Talent (Max(2%, 1)) Sales (Max(4%,1)), Accounts(Max(0.5%,1)), Purchasing(Max(0,5%),1), 
    # IT(Max(2%,1)), R&D (Max(3%,1), Engineering(3%,1), Legal(Max(1%,1)), Customer service(Max(1%,1), 
    # After sales(Max(1%,1)))
    # We assign people according to previous percentajes, while there are people
        self._dept_nums[self.departments[0]] = round(0.4 * people)
        #   administration = round(0.2 * people)
        #   talent = round(max(0.2 * people, 1))
        #   grl_management = round(max(0.1 * people, 1))
        #   sales = round(max(0.4 * people, 1))
        #   finance = round(max(0.05 * people, 1))
        #   purchasing = 
        #   print(production)
        #   print(administration)
        #   print(people)
        #print(Grl_management)
        print(self._dept_nums)

    #    
    #    rand_person = random.choice(ourpeople)
    #    print("Una persona al azar : " + str(rand_person))
    #    self._dept['Production'].add(rand_person)
    #    ourpeople.remove(rand_person)
    #    #ourpeople = ourpeople.pop()
    #    print(ourpeople)
    #    
    ## seleccionar un número aleatorio de valores en la lista de ourpeople
#
#
    #    for k, v in sorted(self._dept.items()):
    #        pass
#
#
    #    self._dept['Talent']= {3, 2, 5}
    #    print(self._dept)
    #    #initiate a set with the index of        

    
        

        



    

