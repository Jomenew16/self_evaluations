# This module helps create a made-up company, including different departments, a defined number of employeers, hierarchies and business areas
#import sys
from os import replace
from typing import Type
import names
import pandas as pd
from pandas import ExcelWriter
from pathlib import Path
from tkinter import *
from tkinter import messagebox
from menu import Menu

#sys.setrecursionlimit(1000000)

class Sim_comp:

    # Rules of assigment: Production (40% of employees) General management (Max(1%,1)) Administration (20%) 
    #  Talent (Max(2%, 1)) Sales (Max(4%,1)), Accounts(Max(0.5%,1)), Purchasing(Max(0,5%),1), 
    # IT(Max(2%,1)), R&D (Max(3%,1), Engineering(3%,1), Legal(Max(1%,1)), Customer service(Max(1%,1), 
    # After sales(Max(1%,1)))    

    #Receives from Menú, de number of collaborators....

    def __init__(self, num_collaborators) -> None:
        self.num_collaborators: int = num_collaborators
        self._people = []
        self.departments = ['Production', 'General management','Administration', 'Talent', 'Sales', 'Accounts', 
        'Purchasing', 'IT', 'R&D', 'Engineering', 'Legal', 'Customer service', 'After sales', 'Others']
        #__dept includes de sets of people. ___dept_nums just includes and integer with the amount of people
        self.__dept = {}
        self.___dept_nums = {}
        self.__list_subareas = []
        self.__list_managers = []
        self.__list_submanagers = []
        self.__column_dept = []
        self.set_company()

 
    
    def set_company(self):
        
        #Number of collaborators come from Menu

        #while self.num_collaborators <7:
            
            #root_colabs = Tk()

            #num_colabs = IntVar()
            #num_colabs.set(20)
#
            #def readEntry(event=None):
            #    #global num_colabs
            #    try:    
            #        self.num_collaborators = num_colabs.get()
            #    except:
            #        messagebox.showwarning('Aviso', 'Introduce un número entero')
            #    finally:
            #        if isinstance(self.num_collaborators, int):
            #            if self.num_collaborators >= 7:
            #                pass
            #            else:
            #                messagebox.showwarning('Aviso', 'La empresa debe tener al menos 7 colaboradores')            
            #        else:
            #            self.num_collaborators = 0 
#
            #    root_colabs.destroy()
#
            #    print(self.num_collaborators)
#
            #def cancel():
            #    root_colabs.destroy()
            #    exit()
#
            #sizeLabel = Label(root_colabs, text= "Tamaño de la empresa (número de colaboradores)", font = ("Open Sans", 10))
            #sizeLabel.pack(side = "top")
#
            #sizeText = Entry(root_colabs, textvariable= num_colabs)
            #sizeText.pack(side="top")
#
            #sizeButton = Button(root_colabs, text="Iniciar", command = readEntry)
            #sizeButton.focus()
            #sizeButton.bind('<Return>', readEntry)
            #sizeButton.pack(pady=10)
#
            #cancelButton = Button(root_colabs, text="Cancelar", command = cancel)
            #cancelButton.pack( pady=10)
            #
            ##self.num_collaborators = input("How many collaborators are there?: ")
            #root_colabs.mainloop()
            

        self._people = [names.get_full_name() for i in range(self.num_collaborators)]    
        
        self.set_areas()

    def set_subareas(self, area:list):
        submanagers=[]
        if len(area) > 20:
            #number of subareas
            num_subareas = (len(area) // 20) + 1
            #people on each subarea
            quotient = len(area) // num_subareas
            remainder = len(area) % num_subareas
        
            sets_floor = 0
            j=0 
            while j < (num_subareas-1) or sets_floor < len(area):
                while remainder > 0:
                    self.__list_subareas.append(area[sets_floor:sets_floor + quotient + 1])
                    submanagers.append(area[sets_floor])
                    sets_floor += quotient +1
                    remainder -= 1 
                    j +=1    
                self.__list_subareas.append(area[sets_floor:sets_floor + quotient])
                submanagers.append(area[sets_floor])
                sets_floor += quotient
                j +=1
            self.__list_submanagers.append(list(submanagers))
        else:
            self.__list_subareas.append(area[:])
            self.__list_submanagers.append(area[0])
            #submanagers.clear()    

    def set_areas(self):
    # Tis method builds a random matriz of interactions.
    #iniciates the dictionary with the different departments and the sets of people blank
    #initiates a sencond dictionario with the number of collaborators in each area     
    #Receives the list of people of each department, selects a general manager, and divides in subareas with a maximum of 20 people.
    #The first collaborator of each subarea will be its leader
                   
        for i in range(len(self.departments)):
            self.__dept[self.departments[i]] = []
            self.___dept_nums[self.departments[i]] = 0
    
    # Assign people to different areas. We will generate in order, so the results will be organized by area    
    # Rules of assigment: Production (45% of employees) General management (Max(2%,1)) Administration (25%)  
    # Talent (Max(3%, 1)) Sales (Max(5%,1)), Accounts(Max(0.5%,1)), Purchasing(Max(0,5%),1), 
    # IT(Max(3%,1)), R&D (Max(3%,1), Engineering(4%,1), Legal(Max(2%,1)), Customer service(Max(2%,1), 
    # After sales(Max(2%,1))) Others(0)
    # We assign people according to previous percentajes, while there are people
        ourpeople = list(range(self.num_collaborators))
        people = self.num_collaborators

    # number of people on each department    
        self.___dept_nums[self.departments[0]] = round(0.45 * people) # production
        self.___dept_nums[self.departments[1]] = round(max(0.02 * people,1)) #gral management
        self.___dept_nums[self.departments[2]] = round(0.25 * people) #administration
        self.___dept_nums[self.departments[3]] = round(max(0.03 * people,1)) # talent
        self.___dept_nums[self.departments[4]] = round(max(0.05 * people, 1)) #sales
        self.___dept_nums[self.departments[5]] = round(max(0.005 * people,1)) #accounts
        self.___dept_nums[self.departments[6]] = round(max(0.005 * people,1)) #purchasing
        self.___dept_nums[self.departments[7]] = round(max(0.03 * people,1)) # IT
        self.___dept_nums[self.departments[8]] = round(max(0.03 * people,1)) #R&D
        self.___dept_nums[self.departments[9]] = round(max(0.04 * people,1)) #Engineering
        self.___dept_nums[self.departments[10]] = round(max(0.02 * people,1)) # Legal
        self.___dept_nums[self.departments[11]] = round(max(0.02 * people,1)) #customer service
        self.___dept_nums[self.departments[12]] = round(max(0.02 * people,1)) #after sales
        self.___dept_nums[self.departments[13]] = 0 # others
        
        people_floor = 0
        i=0
        
        while people > 0:
            if i < 13:
                self.__dept[self.departments[i]] = ourpeople[people_floor:people_floor + self.___dept_nums[self.departments[i]]]
                self.__list_managers.append(ourpeople[people_floor])
                #we will use this list to build de final DF
                [self.__column_dept.append(self.departments[i]) for j in range(self.___dept_nums[self.departments[i]])]
                
                #divide each repartment in different subareas, with no more than 20 people
                self.set_subareas(self.__dept[self.departments[i]])
                people_floor += self.___dept_nums[self.departments[i]]
                people -= self.___dept_nums[self.departments[i]]
                i += 1
            else:
                self.__dept[self.departments[i]] = ourpeople[people_floor:self.num_collaborators]
                self.set_subareas(self.__dept[self.departments[i]])
                [self.__column_dept.append(self.departments[i]) for j in range(people)]
                people = 0
        
        
        self.build_interactions()

    # REceives the number of all collaborators
    
    
    def set_interactions(self,list_int: list, df):
#The function receives a list of data and the DataFrame of the company and includes de interactions
        for i in range(0 , len(list_int)):
            for j in range(i+1,len(list_int)):
                df.iloc[list_int[i],list_int[j]] = True
                df.iloc[list_int[j],list_int[i]] = True
        return df
    
    def build_interactions(self):
    #This method creates the empty DataFrame with two dimensiones of the number of collaborators
    #Then it calls to the method set_interactions and develop the DataFrame according to the following rules:  
               
        #build & compile different sets of interactions, according to the following rules
        # 1- all the people in the same subarea interact with each other. self.__list_subareas
        # 2- All the business area managers interact with each other. self__list_managers
        # 3- All the subareas managers interact with the managers of other subaareas in their department .defined self__list_submanagers
        # 4 - Talent submanagers interacts with everyone 
        # 5- General management interacts with all area and subarea managers
        # Model is not perfect, for in a real company there are many other channels, but it is a good first approach

        
        # blank dataframe
        self.comp_df = pd.DataFrame(columns=range(self.num_collaborators), index=range(self.num_collaborators))
        
        #1 . self.__sets_subareas
        for i in range(len(self.__list_subareas)):
            self.comp_df = self.set_interactions(self.__list_subareas[i],self.comp_df)
        
        #2. self.__list_managers (Managers)
        self.comp_df = self.set_interactions(self.__list_managers,self.comp_df)

        #3. subarea managers interact with othe subarea manegers within their gral department
        for i in range(0,len(self.__list_submanagers)):
            if isinstance(self.__list_submanagers[i],list):
                self.comp_df = self.set_interactions(self.__list_submanagers[i],self.comp_df)
            
        #4. Talent submanagers interact with everyone
        #Generate small lists of pairs (a talent submanager with everyone else)
        
        
        collaborators = range(self.num_collaborators)

        if isinstance(self.__list_submanagers[3], list):
            for i in range(len(self.__list_submanagers[3])):   
                for j in collaborators:
                    if self.__list_submanagers[3][i] != collaborators[j]:
                        pair =[self.__list_submanagers[3][i],collaborators[j]]
                        self.comp_df = self.set_interactions(pair,self.comp_df)
        else:
            for j in collaborators:
                    if self.__list_submanagers[3] != collaborators[j]:
                        pair =[self.__list_submanagers[3],collaborators[j]]
                        self.comp_df = self.set_interactions(pair,self.comp_df)
                    
        #5. Gral management interacts with submanagers
        #Generate small lists of pairs (a talent submanager with everyone else)
        
        #create a list of integers with all the submanagers
        full_submanagers = []

        for i in range(len(self.__list_submanagers)):
            if isinstance (self.__list_submanagers[i], list):
                for j in range(len(self.__list_submanagers[i])):
                    full_submanagers.append(self.__list_submanagers[i][j])
            else:
                full_submanagers.append(self.__list_submanagers[i])
        
  
        if isinstance(self.__list_submanagers[1], list):
            for i in range(len(self.__list_submanagers[1])):   
                for j in range(len(full_submanagers)):
                    if self.__list_submanagers[1][i] != full_submanagers[j]:
                        pair =[self.__list_submanagers[1][i],full_submanagers[j]]
                        self.comp_df = self.set_interactions(pair,self.comp_df)
        else:
            for j in range(len(full_submanagers)):
                if self.__list_submanagers[1] != full_submanagers[j]:
                    pair =[self.__list_submanagers[1],full_submanagers[j]]
                    self.comp_df = self.set_interactions(pair,self.comp_df)                  
       
        
        self.comp_df.set_axis(self._people, axis=1, inplace=True)
        #introducir una columna con los departamentos
        
        #insertamos columna en posición 0
        self.comp_df.insert(0,'Collaborators',self._people)
        self.comp_df.set_index(['Collaborators'], inplace=True)
        self.comp_df.insert(0, 'Areas', self.__column_dept)
        
        #person = self.comp_df.loc[self._people[4],:]
        
        self.comp_df.replace(True, 1, inplace=True)
        
        Path("./archivos").mkdir(parents=True, exist_ok=True)

        self.comp_df.to_csv('./archivos/interacciones.csv')
        
        #with ExcelWriter('./archivos/interacciones.xlsx') as writer:
        #    self.comp_df.to_excel(writer)


#if __name__ == '__main__':
#    Company = Sim_comp()
#    Company.set_company()