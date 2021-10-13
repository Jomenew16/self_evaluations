

from Sim_company import *
from Evaluations import *
from tkinter import *

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
   root = Tk()
   
   root.title("La voz del equipo")
   root.resizable(False, False)
   root.config(bg='blue')
   
   frame_left = Frame(root, width=300, height= 500)
   frame_left.pack(side='left', expand='True')
   frame_left.config(bd=10)
   frame_left.config(relief="ridge")  
   
   frame_right = Frame(root, width=300, height= 500)
   frame_right.pack(side='right', expand='True')
   frame_right.config(bd=10)
   frame_right.config(relief="ridge")  

# -------------------- Evaluations side---------------------------------------
   title_1 = Label(frame_left, text = "EVALUACIONES", font=("Open Sans", 12))
   title_1.pack(side='top', pady= 15, padx=10)   
   
   EvLabel = Label(frame_left, text = "Nueva evaluación", font = ("Open Sans", 9))
   EvLabel.pack(side = 'top')

   EvButton = Button(frame_left, text = "Diseño de evaluación")
   EvButton.pack(side = 'top')
   
   EmptyLabel = Label(frame_left)
   EmptyLabel.pack(pady=10)

   EstLabel = Label(frame_left, text = "Análisis de resultados", font = ("Open Sans", 9))
   EstLabel.pack(side = 'top')

   EstButton = Button(frame_left, text = "Ver estadísticas")
   EstButton.pack(side = 'top')
   
   EmptyLabel2 = Label(frame_left)
   EmptyLabel2.pack(pady=10)

# -------------------- Simulations side---------------------------------------

   def newcompany():
      root.destroy()
      Company = Sim_comp()
      Company.set_company()
      
   
   title_2 = Label(frame_right, text = "SIMULACIONES", font=("Open Sans", 12))
   title_2.pack(side='top', pady= 15, padx=10)   
   
   CompLabel = Label(frame_right, text = "Nueva compañía", font = ("Open Sans", 9))
   CompLabel.pack(side = 'top')

   CompButton = Button(frame_right, text = "Simula una compañía", command= newcompany)
   CompButton.pack(side = 'top')
   
   EmptyLabel3 = Label(frame_right)
   EmptyLabel3.pack(pady=10)

   AutoevLabel = Label(frame_right, text = "Autocumplimenta evaluaciones", font = ("Open Sans", 9))
   AutoevLabel.pack(side = 'top')

   AutoevButton = Button(frame_right, text = "Inicia")
   AutoevButton.pack(side = 'top')
   
   EmptyLabel4 = Label(frame_right)
   EmptyLabel4.pack(pady=10)

   
   root.mainloop()

   # option = 0
   # while option != 4:
   #     option = menu()
#
   # # if menu == 1 set matrix
   #     if option == 1:
#
   #         Company = Sim_comp()
   #         Company.set_company()
#
#
   #     elif option == 2:
   #         ev1 = Evaluation()
   #         ev1.check_matrix()  
   #     
   #     elif option == 3:
   #         test1 = Evaluation()
   #         test1.autoevaluations()


