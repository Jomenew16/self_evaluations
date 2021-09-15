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
    'Purchasing', 'IT', 'R&D', 'Engineering', 'Legal', 'Customer service', 'After sales', 'Others']
    #_dept includes de sets of people. _dept_nums just includes and integer with the amount of people
    _dept = {}
    _dept_nums = {}


    def __init__(self) -> None:
        pass
 
    
    def set_people(self):
        
        self.num_collaborators = int(input("How many collaborators are there: "))
        assert self.num_collaborators > 0, "The number of collaborators has to be a positive number"
        self._people = [names.get_full_name() for i in range(self.num_collaborators)]    
        #print(self._people)
    

    def set_areas(self):
    # Tis method builds a random matriz of interactions.
    #iniciates the dictionary with the different departments and the sets of people blank
    #initiates a sencond dictionario with the number of collaborators in each area
        for i in range(len(self.departments)):
            self._dept[self.departments[i]] = []
            self._dept_nums[self.departments[i]] = 0
    
    # Assign people to different areas. We will generate in order, so the results will be organized by area    
    # Rules of assigment: Production (45% of employees) General management (Max(2%,1)) Administration (25%)  
    # Talent (Max(3%, 1)) Sales (Max(5%,1)), Accounts(Max(0.5%,1)), Purchasing(Max(0,5%),1), 
    # IT(Max(3%,1)), R&D (Max(3%,1), Engineering(4%,1), Legal(Max(2%,1)), Customer service(Max(2%,1), 
    # After sales(Max(2%,1))) Others(0)
    # We assign people according to previous percentajes, while there are people
        ourpeople = list(range(self.num_collaborators))
        people = self.num_collaborators

        
        self._dept_nums[self.departments[0]] = round(0.45 * people) # production
        self._dept_nums[self.departments[1]] = round(max(0.02 * people,1)) #gral management
        self._dept_nums[self.departments[2]] = round(0.25 * people) #administration
        self._dept_nums[self.departments[3]] = round(max(0.03 * people,1)) # talent
        self._dept_nums[self.departments[4]] = round(max(0.05 * people, 1)) #sales
        self._dept_nums[self.departments[5]] = round(max(0.005 * people,1)) #accounts
        self._dept_nums[self.departments[6]] = round(max(0.005 * people,1)) #purchasing
        self._dept_nums[self.departments[7]] = round(max(0.03 * people,1)) # IT
        self._dept_nums[self.departments[8]] = round(max(0.03 * people,1)) #R&D
        self._dept_nums[self.departments[9]] = round(max(0.04 * people,1)) #Engineering
        self._dept_nums[self.departments[10]] = round(max(0.02 * people,1)) # Legal
        self._dept_nums[self.departments[11]] = round(max(0.02 * people,1)) #customer service
        self._dept_nums[self.departments[12]] = round(max(0.02 * people,1)) #after sales
        self._dept_nums[self.departments[13]] = 0 # others
        
        people_floor = 0
        i=0
        while people > 0:
            if i < 13:
                self._dept[self.departments[i]] = ourpeople[people_floor:people_floor + self._dept_nums[self.departments[i]]]
                people_floor += self._dept_nums[self.departments[i]]
                people -= self._dept_nums[self.departments[i]]
                i += 1
            else:
                self._dept[self.departments[i]] = ourpeople[people_floor:people_floor + people]
                people = 0
        
        print(self._dept)

    # REceives the number of all collaborators
    





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
        #print(self._dept_nums)

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

    
        

        



    

