

from datetime import date
from random import sample
from tkinter import font
from Sim_company import *
from Evaluations import *
from tkinter import *

from assessments import EvaluationsAssessment

class Menu(Frame):
   

   def __init__(self, master=None):
       super().__init__(master)
       self.master = master
       self.first_try = True
       #self.first_try_comp = True
       #self.first_try_formats = True

       self.main_menu_widgets()
      
       #self.pack(padx=20, pady=10)
      
   
   def main_menu_widgets(self):
   
   #Create two frames

      self.frame_left = Frame(self.master, width=300, height= 500)
      self.frame_left.grid(row=0, column=0)
      self.frame_left.config(bd=10)
      self.frame_left.config(relief="ridge")  

      self.frame_right = Frame(self.master, width=300, height= 500)
      self.frame_right.grid(row=0, column=1)
      self.frame_right.config(bd=10)
      self.frame_right.config(relief="ridge")        

      self.frame_bottom = Frame(self.master, width=300, height= 150)
      self.frame_bottom.grid(row=1, columnspan=2)
      self.frame_bottom.config(bd=10)
              

#-------------------- Evaluations side -----------------------------------------

      self.title_1 = Label(self.frame_left, text = "EVALUACIONES", font=("Open Sans", 12))
      self.title_1.pack(side='top', pady= 15, padx=10)   

      self.EvLabel = Label(self.frame_left, text = "Nueva evaluación", font = ("Open Sans", 9))
      self.EvLabel.pack(side = 'top')

      self.EvButton = Button(self.frame_left, text = "Crear formularios", command= self.set_formats)
      self.EvButton.pack(side = 'top')

      self.EmptyLabel = Label(self.frame_left)
      self.EmptyLabel.pack(pady=10)

      self.EstLabel = Label(self.frame_left, text = "Análisis de resultados", font = ("Open Sans", 9))
      self.EstLabel.pack(side = 'top')

      self.EstButton = Button(self.frame_left, text = "Ver estadísticas", command= self.menu_last_evaluation)
      self.EstButton.pack(side = 'top')

      self.EmptyLabel2 = Label(self.frame_left)
      self.EmptyLabel2.pack(pady=10)

# -------------------- Simulations side---------------------------------------

      self.title_2 = Label(self.frame_right, text = "SIMULACIONES", font=("Open Sans", 12))
      self.title_2.pack(side='top', pady= 15, padx=10)   

      self.CompLabel = Label(self.frame_right, text = "Nueva compañía", font = ("Open Sans", 9))
      self.CompLabel.pack(side = 'top')

      self.CompButton = Button(self.frame_right, text = "Simula una compañía", command= self.newcompany_menu)
      self.CompButton.pack(side = 'top')

      self.EmptyLabel3 = Label(self.frame_right)
      self.EmptyLabel3.pack(pady=10)

      self.AutoevLabel = Label(self.frame_right, text = "Autocumplimenta evaluaciones", font = ("Open Sans", 9))
      self.AutoevLabel.pack(side = 'top')

      self.AutoevButton = Button(self.frame_right, text = "Inicia autollenado", command= self.autofill)
      self.AutoevButton.pack(side = 'top')

      self.EmptyLabel4 = Label(self.frame_right)
      self.EmptyLabel4.pack(pady=10)
   


      self.CompButton = Button(self.frame_bottom, text = "Salir", command= self.salir_programa)
      self.CompButton.pack(side = BOTTOM)

   def salir_programa(self):
      self.master.destroy()
      exit()
   
   def destroy_main_frames(self):
      self.frame_left.destroy()
      self.frame_right.destroy()
      self.frame_bottom.destroy()


# -------------------- Create formats from the interactions file menu---------------------------------------
   def set_formats(self):

      #if entering for the first time, drops the main menú frames
      if self.first_try:
         self.destroy_main_frames()
         
      
      #get the number of evaluators required
      sample_evaluators = 0
      
      num_evaluations = IntVar()
      num_evaluations.set(7) 

      def destroy_formats_menu():
         self.txLabel.destroy()
         self.numEntry.destroy()
         self.evButton.destroy()
         self.evcancelButton.destroy()      
      
      def evaluators(event=None):

          try:    
              sample_evaluators = num_evaluations.get()
          except:
              messagebox.showwarning('Aviso', 'Debes escoger un número entero')
              
          finally:
              if isinstance(sample_evaluators, int):
                  if sample_evaluators >= 3:
                      messagebox.showwarning('¡Excelente!', 'Selecciona a continuación el archivo con las interacciones')
                      ev = Evaluation()
                      ev.check_matrix(sample_evaluators)                      
                      back_to_main()                
                  else:
                      messagebox.showwarning('Aviso', 'Escoge al menos 3 evaluadores por colaborador')            
                      self.first_try =False
                      destroy_formats_menu()
                      self.set_formats()
                      #print("\nEscoge al menos 3 evaluadores por colaborador\n")
              else:
                  sample_evaluators = 0
                  self.first_try =False
                  destroy_formats_menu()
                  self.set_formats() 
          
      def back_to_main ():
          destroy_formats_menu()
          self.first_try =True
          self.main_menu_widgets()
      
      self.txLabel = Label(self.master, text="¿Cuántas evaluaciones se requieren por cada colaborador?")
      self.txLabel.pack(side="top")
      self.numEntry = Entry(self.master, textvariable = num_evaluations)
      self.numEntry.pack(side='top')
      self.evButton = Button(self.master, text="iniciar", command = evaluators)
      self.evButton.focus()
      self.evButton.bind('<Return>', evaluators)
      self.evButton.pack(side='top')
      self.evcancelButton = Button(self.master, text="Cancelar", command = back_to_main)
      self.evcancelButton.pack(pady=10)

# -------------------- Simulate a new company menu---------------------------------------

   def newcompany_menu(self):
      
      #if entering for the first time, drops the main menú frames
      if self.first_try:
         self.destroy_main_frames()
      
      company_size = 0

      #while company_size <= 7:
      num_colabs = IntVar()
      num_colabs.set(20)
      
      def destroy_newcompany_menu():
         self.sizeLabel.destroy()
         self.sizeText.destroy()
         self.sizeButton.destroy()
         self.cancelButton.destroy()

      
      def readEntry(event=None):
         #global num_colabs
         try:    
            company_size = num_colabs.get()
         except:
            messagebox.showwarning('Aviso', 'Introduce un número entero')
         finally:
             if isinstance(company_size, int):
                 if company_size >= 7:
                     messagebox.showwarning('¡Excelente!', 'La empresa se está creando')
                     new_company = Sim_comp(company_size)
                     destroy_newcompany_menu()
                     self.first_try = True
                     self.main_menu_widgets()
                     #new_company.set_company()
                 else:
                     messagebox.showwarning('Aviso', 'La empresa debe tener al menos 7 colaboradores')
                     self.first_try = False
                     destroy_newcompany_menu()
                     #self.main_menu_widgets()
                     self.newcompany_menu()            
             else:
                 company_size = 0
                 self.first_try = False
                 destroy_newcompany_menu() 
                 self.newcompany_menu()      
         
      
      def cancel():
         destroy_newcompany_menu()
        # messagebox.showwarning('Aviso', 'Volver al menu original')
         self.main_menu_widgets()
         self.first_try = True

         
   
      self.sizeLabel = Label(self.master, text= "Tamaño de la empresa (número de colaboradores)", font = ("Open Sans", 10))
      self.sizeLabel.pack(side = "top")
      self.sizeText = Entry(self.master, textvariable= num_colabs)
      self.sizeText.pack(side="top")
      self.sizeButton = Button(self.master, text="Iniciar", command = readEntry)
      self.sizeButton.focus()
      self.sizeButton.bind('<Return>', readEntry)
      self.sizeButton.pack(pady=10)
      self.cancelButton = Button(self.master, text="Cancelar", command = cancel)
      self.cancelButton.pack( pady=10)

   def autofill(self):
      messagebox.showwarning('¡Aviso!', 'Selecciona la carpeta que contiene los archivos a cumplimentar')
      test = Evaluation()
      test.autoevaluations()


# -------------------- First statistics menu ---------------------------------------

   def menu_last_evaluation(self):
      
      if self.first_try:
         self.destroy_main_frames()

      last_ev = EvaluationsAssessment()
      last_ev.read_directories()  #reads the last evaluation data from the archivos directory
      names= last_ev.evaluation_data.keys()
      date_of_evaluation = last_ev.evaluation_data[names[0]['date']]

   #  Set dimensions of the screen
      total_width = self.master.winfo_screenwidth()
      total_height = self.master.winfo_screenheight()

      submenu_title = Label(self.master, text='ESTATUS ÚLTIMA EVALUACIÓN', font = ("Open Sans", 15)).grid(row=0, columnspan=2)
      frame1 = Frame(self.master, width= 600, height=500)
      frame1.grid(row=1, column=0)
      frame1.config(highlightcolor='black', highlightthickness=1)
      frame2 = Frame(self.master, width= total_width-700, height=500)
      frame2.grid(row=1, column=1)
      frame2.config(highlightcolor='black', highlightthickness=1)
      frame3 = Frame(self.master, width= 800, height=total_height-500)
      frame3.grid(row=2, column=0)
      frame3.config(highlightcolor='black', highlightthickness=1)
      frame4 = Frame(self.master, width= total_width-800, height=total_height-500)
      frame4.grid(row=2, column=1)
      frame4.config(highlightcolor='black', highlightthickness=1)
      frame5 = Frame(self.master, width= total_width, height=200)
      frame5.grid(row=3, columnspan=2)
      frame5.config(highlightcolor='black', highlightthickness=1)

# First Frame includes checking of formats status and of evaluators

      #we need date and checkings
      #1- FIND LAS EVALUATION

      dateLabel = Label(frame1, text="Fecha:", font=('Open Sans', 12))
      dateLabel.grid(row=0, column=0)
      f = font.Font(dateLabel, dateLabel.cget("font"))
      f.configure(underline=True)
      dateLabel.configure(font = f)

      evDate = Label(frame1, text=date_of_evaluation, font=('Open Sans', 12, 'bold'))
      evDate.grid(row=0, column=1)
      

   #   
   #   #get the number of evaluators required
   #   sample_evaluators = 0
   #   
   #   num_evaluations = IntVar()
   #   num_evaluations.set(7) 
#
   #   def destroy_formats_menu():
   #      self.txLabel.destroy()
   #      self.numEntry.destroy()
   #      self.evButton.destroy()
   #      self.evcancelButton.destroy()      
   #   
   #   def evaluators(event=None):
#
   #       try:    
   #           sample_evaluators = num_evaluations.get()
   #       except:
   #           messagebox.showwarning('Aviso', 'Debes escoger un número entero')
   #           
   #       finally:
   #           if isinstance(sample_evaluators, int):
   #               if sample_evaluators >= 3:
   #                   messagebox.showwarning('¡Excelente!', 'Selecciona a continuación el archivo con las interacciones')
   #                   ev = Evaluation()
   #                   ev.check_matrix(sample_evaluators)                      
   #                   back_to_main()                
   #               else:
   #                   messagebox.showwarning('Aviso', 'Escoge al menos 3 evaluadores por colaborador')            
   #                   self.first_try =False
   #                   destroy_formats_menu()
   #                   self.set_formats()
   #                   #print("\nEscoge al menos 3 evaluadores por colaborador\n")
   #           else:
   #               sample_evaluators = 0
   #               self.first_try =False
   #               destroy_formats_menu()
   #               self.set_formats() 
   #       
   #   def back_to_main ():
   #       destroy_formats_menu()
   #       self.first_try =True
   #       self.main_menu_widgets()
   
         
   #   self.txLabel = Label(self.master, text="¿Cuántas evaluaciones se requieren por cada colaborador?")
   #   self.txLabel.pack(side="top")
   #   self.numEntry = Entry(self.master, textvariable = num_evaluations)
   #   self.numEntry.pack(side='top')
   #   self.evButton = Button(self.master, text="iniciar", command = evaluators)
   #   self.evButton.focus()
   #   self.evButton.bind('<Return>', evaluators)
   #   self.evButton.pack(side='top')
   #   self.evcancelButton = Button(self.master, text="Cancelar", command = back_to_main)
   #   self.evcancelButton.pack(pady=10)



   # menu =int(input("""¿What do you want to do?:
   # 1. Simulate a new company \n
   # 2. Setup the team evaluations\n
   # 3. Fill autoevaluations\n
   # 4. Exit program\n"""))
#
   # return menu
    
    
    #We will requests the data to set the matrix, read matrix, etc
    #1 create matrix
        #Data: number of employees
    #2 read matrix
    #3 New evaluation
       #2.1 Evaluations by employee
       #2.2 Evaluators of an employeer
       #2.3 set forms
     


if __name__ == '__main__':

# Read menu
   root = Tk()
   
   root.title("La voz del equipo")
   root.resizable(False, False)
   menu_app = Menu(master = root)
   
   root.mainloop()


# -------------------- Evaluations side---------------------------------------
   
#   def set_formats():

       
   
   

# -------------------- Simulations side---------------------------------------#
#

      


  
#   root.mainloop()

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


