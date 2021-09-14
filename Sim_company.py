# This module helps create a made-up company, including different departments, a defined number of employeers, hierarchies and business areas
import names
import random

class Sim_comp():
    
    num_collaborators: int = 10
    _people = []
    _dept = {
        'Talent': set(),
        'Production': set(),
        'Quality': set(),
        'Administration': set(),
        'Finance': set(),
        'General management': set(), 
        'Sales': set(), 
        'Purchase': set(), 
        'R&D': set(), 
        'Engineering': set(),
        'Marketing': set()}


    def __init__(self, num_collaborators) -> None:
        self.num_collaborators = num_collaborators
        

    def set_areas(self):
    # Tis method builds a random matriz of interactions.
    # Rceives the number of all collaborators. module names provide random list of names
        self._people = [names.get_full_name() for i in range(self.num_collaborators)]
        ourpeople = list(range(self.num_collaborators))
        rand_person = random.choice(ourpeople)
        print("Una persona al azar : " + str(rand_person))
        self._dept['Production'].add(rand_person)
        ourpeople.remove(rand_person)
        #ourpeople = ourpeople.pop()
        print(ourpeople)
        print(self._people)
    
    # seleccionar un número aleatorio de valores en la lista de ourpeople


        for k, v in sorted(self._dept.items()):
            pass


        self._dept['Talent']= {3, 2, 5}
        print(self._dept)
        #initiate a set with the index of
        

        



    

