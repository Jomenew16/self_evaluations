

from datetime import date
from datetime import datetime
from random import sample
from tkinter import font

from matplotlib.pyplot import title
from Sim_company import *
from Evaluations import *
from tkinter import *
from tkinter import ttk
import time
from PIL import Image, ImageTk

from assessments import EvaluationsAssessment

class Menu(Frame):
   

   def __init__(self, master=None):
       super().__init__(master)
       self.master = master
       self.first_try = True
       self.thispath = os.getcwd()
       #self.areas = []
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
      num_formatsCheck, num_evaluatorsCheck, problematicEvaluations = last_ev.checkplan()
      names= list(last_ev.evaluation_data.keys())
      date_of_evaluation = last_ev.evaluation_data[names[0]]['date']

   #  Set dimensions of the screen
      total_width = self.master.winfo_screenwidth()
      total_height = self.master.winfo_screenheight()

      frame0 = Frame(self.master)
      frame0.grid(row=0, columnspan=2)
      submenu_title = Label(frame0, text='ESTATUS ÚLTIMA EVALUACIÓN', font = ("Open Sans", 12)).pack()
      
      frame1 = Frame(self.master)
      frame1.grid(row=1, column=0)
      frame1.config(highlightcolor='black', highlightthickness=1)
      #frame1.config(bd=10)
      #frame1.config(relief="ridge")
      frame2 = Frame(self.master )
      frame2.grid(row=1, column=1)
      frame2.config(highlightcolor='black', highlightthickness=1)
      #frame2.config(bd=10)
      #frame2.config(relief="ridge") 
      frame3 = Frame(self.master )
      frame3.grid(row=2, columnspan=2)
      frame3.config(highlightcolor='black', highlightthickness=1)
      #frame3.config(bd=10)
      #frame3.config(relief="ridge") 
      #frame4 = Frame(self.master )
      #frame4.grid(row=3, column=1)
      #frame4.config(highlightcolor='black', highlightthickness=1)
      #frame4.config(bd=10)
      #frame4.config(relief="ridge") 
      frame4 = Frame(self.master )
      frame4.grid(row=3, columnspan=2)
      frame4.config(highlightcolor='black', highlightthickness=1)
      #frame5.config(bd=10)
      #frame5.config(relief="ridge")

# First Frame includes checking of formats status and of evaluators
      formatsCheck = 'Número de formularios: OK' if num_formatsCheck else 'El número de formularios no coincide con el plan'
      evaluatorsCheck = 'Comprobación de evaluadores: OK' if num_evaluatorsCheck else f'Hay una inconsistencia en {len(problematicEvaluations)} archivos de evaluación'

      #we need date and checkings
      #1- FIND LAS EVALUATION
      def see_inconsistencies():
         if len(problematicEvaluations) == 0:
            messagebox.showinfo('Aviso', 'Las evaluaciones parecen ajustarse a lo prediseñado')
         else:
            messagebox.showinfo('Verificar', f'Verifica las evalaciones de las siguientes personas \n{problematicEvaluations}\n')


      dateLabel = Label(frame1, text="Fecha de la evaluación:  ", font=('Open Sans', 9))
      dateLabel.grid(sticky='W', row=0, column=0)
      f = font.Font(dateLabel, dateLabel.cget("font"))
      f.configure(underline=True)
      dateLabel.configure(font = f)

      evDate = Label(frame1, text=date_of_evaluation.strftime('%d/%m/%Y'), font=('Open Sans', 9, 'bold'))
      evDate.grid(sticky='W', row=0, column=1)

      firstCheck = Label(frame1, text = formatsCheck)
      firstCheck.grid(sticky='W', row=1,columnspan=2)
      if num_formatsCheck:
         firstCheck.config(font=('Open Sans', 9), fg='green')
      else:
         firstCheck.config(font=('Open Sans', 9, 'bold'), fg='red')

      secondCheck = Label(frame1, text = evaluatorsCheck)
      secondCheck.grid(sticky='W', row=2,column=0)
      if num_evaluatorsCheck:
         secondCheck.config(font=('Open Sans', 9), fg='green')
      else:
         secondCheck.config(font=('Open Sans', 9, 'bold'), fg='red')

      seeProblems = Button(frame1, text='Verificar', command=see_inconsistencies)
      seeProblems.grid(sticky='W', row=2, column= 1)

   # Second Frame includes number of completed formats
      last_ev.create_first_check_submenu_stats()

      #thispath = os.getcwd()
      
      S1F2_pie_img = PhotoImage(file = self.thispath + '/archivos/1_archivos de trabajo/S1F2_pieCompletion.png')
      S1F2_pieGraphcompletion = Label(frame2, image= S1F2_pie_img)
      S1F2_pieGraphcompletion.config(relief='ridge', borderwidth='2')
      S1F2_pieGraphcompletion.image = S1F2_pie_img
      S1F2_pieGraphcompletion.pack(side='top')


   # Third Frame includes number of completed formats
      S1F3_hbar_img = PhotoImage(file = self.thispath + '/archivos/1_archivos de trabajo/S1F3_hbars_completion.png')
      S1F3_hbar_completion = Label(frame3, image= S1F3_hbar_img)
      S1F3_hbar_completion.config(relief='ridge', borderwidth='2')
      S1F3_hbar_completion.image = S1F3_hbar_img
      S1F3_hbar_completion.pack(side='left')
   
   
   # Forth Frame includes return to menu Button, save and see statistics

      def mainmenu():
         frame0.destroy()
         frame1.destroy()
         frame2.destroy()
         frame3.destroy()
         frame4.destroy()
         self.main_menu_widgets()

      def globalstmenu():
         frame0.destroy()
         frame1.destroy()
         frame2.destroy()
         frame3.destroy()
         frame4.destroy()
         #guardar datos evaluación
         last_ev.save_data()
         self.global_stats_menu(date_of_evaluation, last_ev)

      contBut = Button(frame4, text="Continuar", command = globalstmenu)
      contBut.grid(row=0, column=0, padx=15)

      backBut = Button(frame4, text="Menú principal", command = mainmenu)
      backBut.grid(row=0, column=1)

      #ansevBut = Button(frame4, text="Ver evaluación anterior")
      #ansevBut.grid(row=0, column=2, padx = 5)
      
   
   # -------------------- Global statistics menu ---------------------------------------------------

   def global_stats_menu(self, date, eval_instance):
      
      frame1=Frame(self.master)
      frame1.grid(row=0, columnspan=3)

      dateLabel = Label(frame1, text="Fecha: ", font=('Open Sans', 9))
      dateLabel.grid(sticky='W', row=0, column=0)
      f = font.Font(dateLabel, dateLabel.cget("font"))
      f.configure(underline=True)
      dateLabel.configure(font = f)

      evDate = Label(frame1, text=date.strftime('%d/%m/%Y'), font=('Open Sans', 9))
      evDate.grid(sticky='W', row=0, column=1)
      evDate.config(bg='white')

      submenu2_title = Label(frame1, text='RESULTADOS GENERALES', font = ("Open Sans", 10))
      submenu2_title.grid(sticky='N',row=1, columnspan=2)
      
      frame2 = Frame(self.master)
      frame2.grid(row=1,column=0)
      frame2.config(highlightcolor='black', highlightthickness=1)

      frame3 = Frame(self.master)
      frame3.grid(row=1, column=1)
      frame3.config(highlightcolor='black', highlightthickness=1)

      frame4 = Frame(self.master)
      frame4.grid(row=1, column=2)
      frame4.config(highlightcolor='black', highlightthickness=1)

      frame5 = Frame(self.master)
      frame5.grid(row=2, columnspan=3)
      frame5.config(highlightcolor='black', highlightthickness=1)

#include image of comparison between collaborators
      eval_instance.create_second_allcollabs_submenu_stats()

      S2F1_bar_img = PhotoImage(file = self.thispath + '/archivos/1_archivos de trabajo/S2F1_bar_allCollabs.png')
      S2F1_bar_allCollabs = Label(frame2, image=S2F1_bar_img)
      S2F1_bar_allCollabs.config(relief='ridge', borderwidth='3')
      S2F1_bar_allCollabs.image = S2F1_bar_img
      S2F1_bar_allCollabs.pack(side='left')
      #S2F1_bar_allCollabs.grid(row=0, column=0)   

      #S2F3_bar_img = PhotoImage(file = self.thispath + '/archivos/1_archivos de trabajo/S2F3_bar_category.png')
      #S2F3_bar_category = Label(frame3, image=S2F3_bar_img)
      #S2F3_bar_category.config(relief='ridge', borderwidth='3')
      #S2F3_bar_category.image = S2F3_bar_img
      #S2F3_bar_category.pack(side='top')
      
      S2F2_bar_img = PhotoImage(file = self.thispath + '/archivos/1_archivos de trabajo/S2F2_bar_area.png')
      S2F2_bar_area = Label(frame4, image=S2F2_bar_img)
      S2F2_bar_area.config(relief='ridge', borderwidth='3')
      S2F2_bar_area.image = S2F2_bar_img
      S2F2_bar_area.pack(side='top')
      #S2F1_bar_allCollabs.grid(row=0, column=1)


      def backtomainmenu():
         frame1.destroy()
         frame2.destroy()
         frame3.destroy()
         frame4.destroy()
         frame5.destroy()
         self.main_menu_widgets()

      def backtofirststats():
         frame1.destroy()
         frame2.destroy()
         frame3.destroy()
         frame4.destroy()
         frame5.destroy()
         self.menu_last_evaluation()

      def collab_menu():
         frame1.destroy()
         frame2.destroy()
         frame3.destroy()
         frame4.destroy()
         frame5.destroy()
         self.menu_collaborator_first_submenu(date, eval_instance)

      def area_menu():
         frame1.destroy()
         frame2.destroy()
         frame3.destroy()
         frame4.destroy()
         frame5.destroy()
         self.menu_areas_submenu(date, eval_instance)
   
      findCButton = Button(frame5, text = 'Ver colaborador', command= collab_menu)
      findCButton.grid(row=0, column=0)

      findDButton = Button(frame5, text = 'Ver departamento', command=area_menu)
      findDButton.grid(row=0, column=1, padx=5)

      backButton =Button(frame5, text = 'Volver', command=backtofirststats)
      backButton.grid(row=0, column=3, padx=10)

      initButton = Button(frame5, text = 'Inicio', command = backtomainmenu)
      initButton.grid(row=0, column=4)


   # -------------------- Subm3 - Collaborator statistics ---------------------------------------------------

   def menu_collaborator_first_submenu(self, date, eval_instance):

      #Set date and a selection combo box and button to select the collaborator
      frame1=Frame(self.master)
      frame1.grid(row=0, columnspan=2)

      frame2 = Frame(self.master) # categories chart
      frame2.grid(row=1, column=0)

      frame3 = Frame(self.master) # evaluation results
      frame3.grid(row=1, column=1)

      frame4 = Frame(self.master) # bottom menu
      frame4.grid(row=2, columnspan=2)

      frame5 = Frame(self.master) # bottom menu
      frame5.grid(row=3, columnspan=2)


      evDate = Label(frame1, text=date.strftime('%d/%m/%Y'), font=('Open Sans', 9))
      evDate.grid(sticky='W', row=0, column=0, padx=10)
      evDate.config(bg='white')

      selectLable = Label(frame1, text = "Selecciona colaborador:")
      selectLable.grid(sticky='E', row=0, column=1)

      #combo box and selection of collaborator
      
      #list of collaborators
      collabs = list(eval_instance.evaluation_data.keys())  #list of collaborators, in case we need them for combo box
      collab = StringVar()
      collab.set(collabs[0])
      #collaborator: str
      
      
      
      def collab_statistics():
         #global collaborator 
         collaborator = collab.get()
         
         eval_instance.create_collaborator_submenu_stats(collaborator)
         set_charts() 


      comboCollabs = ttk.Combobox(frame1, state='readonly', textvariable=collab) #
      comboCollabs['values'] = collabs
      comboCollabs.grid(sticky='W', row=0, column=2)
        
      confirmBut = Button(frame1, text = "Ver evaluación", command=collab_statistics)
      confirmBut.grid(sticky='W', row=0, column=3, padx=10)

      #----------------------------- 2nd and 3rd frames with the collaborator charts--------------------
      chart_set = False

      def set_charts():
         for widget in frame2.winfo_children():
            widget.destroy()
         for widget in frame3.winfo_children():
            widget.destroy()
         for widget in frame4.winfo_children():
            widget.destroy()
         
         S3F2_radar_img = PhotoImage(file = self.thispath + '/archivos/1_archivos de trabajo/S2F2_radar_category.png')
         S3F2_radar_categ = Label(frame2, image=S3F2_radar_img)
         S3F2_radar_categ.config(relief='ridge', borderwidth='3')
         S3F2_radar_categ.image = S3F2_radar_img
         S3F2_radar_categ.grid(row=0, columnspan=2)

         S3F3_questionsbar_img = PhotoImage(file = self.thispath + '/archivos/1_archivos de trabajo/S2F3_questions_evaluation.png')
         S3F3_questionsbar = Label(frame3, image=S3F3_questionsbar_img)
         S3F3_questionsbar.config(relief='ridge', borderwidth='3')
         S3F3_questionsbar.image = S3F3_questionsbar_img
         S3F3_questionsbar.grid(row=0, columnspan=2)
         #S3F3_questionsbar.pack(side='top')

         # Detail of the questions ratios. First, include the general results
      #   detail_quests_Label = Label(frame3, text='Detalles')
      #   detail_quests_Label.grid(row=1, column=0)
      #   
      #   detail_quests_Button = Button(frame3, text='Ver más')
      #   detail_quests_Button.grid(row=1, column=1)
#
   #---------------- FRAME 4. SUMMARY and EVALUATION STATS-----------------------------------------------
         def qualification(x):
            if x < 2.9:
               return 'Necesita mejorar'
            elif x <= 3.4:
               return 'Normal'
            elif x <= 4.2:
               return 'Bueno'
            else:
               return 'Excelente'

         global_qual= eval_instance.evaluation_data[collab.get()]['global evaluation']
         overall_qual= eval_instance.evaluation_data[collab.get()]['overall evaluation']
         #print(global_qual)
         #print(overall_qual)

         global_ev_mean = Label(frame4, text = 'Desempeño promedio: ' + qualification(global_qual) + f' ({str(round(global_qual,1))})', font=('Open Sans', 9, 'bold'))
         global_ev_mean.grid(row=0, column=0, padx=15)

         global_ev_overall = Label(frame4, text = 'Desempeño cualitativo: ' + qualification(overall_qual) + f' ({str(round(overall_qual,1))})', font=('Open Sans', 9, 'bold'))
         global_ev_overall.grid(row=0, column=1, padx=15)

         # Details on the evaluation

         ev_details = Label(frame4, text = 'Detalles y rangos de evaluación', font=('Open Sans', 9))
         ev_details.grid(row=1, column=0, pady=10, sticky='N')

         def menu_details():
            frame1.destroy()
            frame2.destroy()
            frame3.destroy()
            frame4.destroy()
            frame5.destroy()
            self.menu_details_evaluation(date, eval_instance, collab.get())

         ev_detailsButton = Button(frame4, text = 'Ver detalles', command= menu_details)
         ev_detailsButton.grid(row=1, column=1, sticky='W')


   #---------------- FRAME 5. NAVIGATION------------------------------------------      
      def backtomainmenu():
         frame1.destroy()
         frame2.destroy()
         frame3.destroy()
         frame4.destroy()
         frame5.destroy()
         self.main_menu_widgets()

      def backtogeneralstats():
         frame1.destroy()
         frame2.destroy()
         frame3.destroy()
         frame4.destroy()
         frame5.destroy()
         self.global_stats_menu(date, eval_instance)

      def evolution_menu():
         frame1.destroy()
         frame2.destroy()
         frame3.destroy()
         frame4.destroy()
         frame5.destroy()
         self.menu_collaborator_evolution_submenu(date, eval_instance, collab.get())
      
      def area_menu():
         frame1.destroy()
         frame2.destroy()
         frame3.destroy()
         frame4.destroy()
         frame5.destroy()
         self.menu_areas_submenu(date, eval_instance)

      findCButton = Button(frame5, text = 'Ver evolución', command= evolution_menu)
      findCButton.grid(row=0, column=0)

      findDButton = Button(frame5, text = 'Ver departamento', command=area_menu)
      findDButton.grid(row=0, column=1, padx=5)

      backButton =Button(frame5, text = 'Volver', command=backtogeneralstats)
      backButton.grid(row=0, column=2, padx=10)

      initButton = Button(frame5, text = 'Inicio', command = backtomainmenu)
      initButton.grid(row=0, column=3) 


# -------------------- Subm4 - Collaborator statistics ---------------------------------------------------
   
   def menu_details_evaluation (self, date, eval_instance, collaborator):

      #Set date and a selection combo box and button to select the collaborator
      frame1=Frame(self.master)
      frame1.grid(row=0, columnspan=2)

      frame2 = Frame(self.master) # categories chart
      frame2.grid(row=1, column=0)

      frame3 = Frame(self.master) # categories chart
      frame3.grid(row=2, column=0)

      evDate = Label(frame1, text=date.strftime('%d/%m/%Y'), font=('Open Sans', 9))
      evDate.grid(sticky='W', row=0, column=0, padx=10)
      evDate.config(bg='white')

      collabLabel = Label(frame1, text = collaborator.upper(), font=('Open Sans', 10, 'bold'))
      collabLabel.grid(sticky='E', row=0, column=1)

      #create pie charts with valid evaluations
      eval_instance.collaborator_subsubmenu_details(collaborator)

      S4F2_pieEvaluations_img = PhotoImage(file = self.thispath + '/archivos/1_archivos de trabajo/S4F2_valid_evaluations_pie.png')
      S4F2_pieEvaluations = Label(frame2, image=S4F2_pieEvaluations_img)
      S4F2_pieEvaluations.config(relief='ridge', borderwidth='3')
      S4F2_pieEvaluations.image = S4F2_pieEvaluations_img
      S4F2_pieEvaluations.grid(rowspan=2, column=0)

      S4F2_out_of_range_explant_Label = Label(frame2, text = 'Las evaluaciones fuera de rango son las que se han desviado \nun determinado porcentaje de la media')
      S4F2_out_of_range_explant_Label.grid(row=0, column=1, columnspan=3, sticky='N')
      
      S4F2_out_of_range_modif_Label = Label(frame2, text = 'Modifica el rango de sensibilidad (%)')
      S4F2_out_of_range_modif_Label.grid(row=1, column=1)

      tol_range = IntVar()
      tol_range.set(round(eval_instance.evaluation_data[collaborator]['tolerance']*100))

      def newrange():
         #eval_instance.evaluation_data[collaborator]['tolerance'] = (tol_range.get())/100
         eval_instance.read_directories(tol_range.get()/100)
         eval_instance.save_data()
         eval_instance.collaborator_subsubmenu_details(collaborator)
         frame1.destroy()
         frame2.destroy()
         frame3.destroy()
         self.menu_details_evaluation(date, eval_instance, collaborator)         


      S4F2_out_of_range_modif_Entry = Entry(frame2, textvariable= tol_range)
      S4F2_out_of_range_modif_Entry.grid(row=1, column=2, sticky='W')

      S4F2_out_of_range_modif_Button = Button(frame2, text = 'cambiar', command=newrange)
      S4F2_out_of_range_modif_Button.grid(row=1, column=3, sticky='W')

      def backtomainmenu():
         frame1.destroy()
         frame2.destroy()
         frame3.destroy()
         self.main_menu_widgets()

      def backtocollabstats():
         frame1.destroy()
         frame2.destroy()
         frame3.destroy()
         self.menu_collaborator_first_submenu(date, eval_instance)
      
      backButton =Button(frame3, text = 'Volver', command=backtocollabstats)
      backButton.grid(row=0, column=2, padx=10)

      initButton = Button(frame3, text = 'Inicio', command = backtomainmenu)
      initButton.grid(row=0, column=3) 


# -------------------- Subm5 - Collaborator statistics ---------------------------------------------------

   def menu_collaborator_evolution_submenu(self, date, eval_instance, collaborator):
      frame1=Frame(self.master)
      frame1.grid(row=0, columnspan=2)

      frame2 = Frame(self.master) # categories chart
      frame2.grid(row=1, column=0)

      frame3 = Frame(self.master) # categories chart
      frame3.grid(row=2, column=0)

      collabLabel = Label(frame1, text = collaborator.upper(), font=('Open Sans', 10, 'bold'))
      collabLabel.grid(sticky='E', row=0, column=0)

      eval_instance.collaborator_evolution(collaborator)

      S5F2_gb_evolutions_line_img = PhotoImage(file = self.thispath + '/archivos/1_archivos de trabajo/S5F2_global evolution.png')
      S5F2_gb_evolutions_line = Label(frame2, image=S5F2_gb_evolutions_line_img)
      S5F2_gb_evolutions_line.config(relief='ridge', borderwidth='3')
      S5F2_gb_evolutions_line.image = S5F2_gb_evolutions_line_img
      S5F2_gb_evolutions_line.grid(row=0, column=0)

      S5F2_cat_evolutions_line_img = PhotoImage(file = self.thispath + '/archivos/1_archivos de trabajo/S5F2_evolution_by_categories.png')
      S5F2_cat_evolutions_line = Label(frame2, image=S5F2_cat_evolutions_line_img)
      S5F2_cat_evolutions_line.config(relief='ridge', borderwidth='3')
      S5F2_cat_evolutions_line.image = S5F2_cat_evolutions_line_img
      S5F2_cat_evolutions_line.grid(row=0, column=1)

      # End menú
      def backtomainmenu():
         frame1.destroy()
         frame2.destroy()
         frame3.destroy()
         self.main_menu_widgets()

      def backtocollabstats():
         frame1.destroy()
         frame2.destroy()
         frame3.destroy()
         self.menu_collaborator_first_submenu(date, eval_instance)
      
      backButton =Button(frame3, text = 'Volver', command=backtocollabstats)
      backButton.grid(row=0, column=2, padx=10)

      initButton = Button(frame3, text = 'Inicio', command = backtomainmenu)
      initButton.grid(row=0, column=3) 

# -------------------- Subm6 - Area statistics ---------------------------------------------------

   def menu_areas_submenu(self, date, eval_instance):      
      #Set date and a selection combo box and button to select the collaborator
      frame1=Frame(self.master)
      frame1.grid(row=0, columnspan=2)

      frame2 = Frame(self.master) # categories chart
      frame2.grid(row=1, column=0)

      frame3 = Frame(self.master) # evaluation results
      frame3.grid(row=2, column=0)

      frame4 = Frame(self.master) # bottom menu
      frame4.grid(row=2, columnspan=2)

      frame5 = Frame(self.master) # bottom menu
      frame5.grid(row=3, columnspan=2)


      evDate = Label(frame1, text=date.strftime('%d/%m/%Y'), font=('Open Sans', 9))
      evDate.grid(sticky='W', row=0, column=0, padx=10)
      evDate.config(bg='white')

      selectLable = Label(frame1, text = "Selecciona area:")
      selectLable.grid(sticky='E', row=0, column=1)

      #combo box and selection of collaborator
      
      #list of collaborators
      areas = eval_instance.areas  #list of collaborators, in case we need them for combo box
      #areas = list(eval_instance.evaluation_data[collaborators[0]][])
      area = StringVar()
      area.set(areas[0])
      #collaborator: str
          
      def areas_statistics():
         #global collaborator 
         department = area.get()
         
         eval_instance.create_area_submenu_stats(department)
         set_charts() 



      comboCollabs = ttk.Combobox(frame1, state='readonly', textvariable=area) #
      comboCollabs['values'] = areas
      comboCollabs.grid(sticky='W', row=0, column=2)
        
      confirmBut = Button(frame1, text = "Ver evaluación", command=areas_statistics)
      confirmBut.grid(sticky='W', row=0, column=3, padx=10)


      def set_charts():
         for widget in frame2.winfo_children():
            widget.destroy()
         #for widget in frame3.winfo_children():
         #   widget.destroy()
         #for widget in frame4.winfo_children():
         #   widget.destroy()
   #-------------------- department statistics----------------------
         S6F2_dept_collabs_bar_img = PhotoImage(file = self.thispath + '/archivos/1_archivos de trabajo/S6F2_area_collaborators.png')
         S6F2_dept_collabs_bar = Label(frame2, image=S6F2_dept_collabs_bar_img)
         S6F2_dept_collabs_bar.config(relief='ridge', borderwidth='3')
         S6F2_dept_collabs_bar.image = S6F2_dept_collabs_bar_img
         S6F2_dept_collabs_bar.grid(row=0, column=0)

         S6F2_dept_catg_heat_img = PhotoImage(file = self.thispath + '/archivos/1_archivos de trabajo/S6F2_area_heatmap.png')
         S6F2_dept_catg_heat = Label(frame2, image=S6F2_dept_catg_heat_img)
         S6F2_dept_catg_heat.config(relief='ridge', borderwidth='3')
         S6F2_dept_catg_heat.image = S6F2_dept_catg_heat_img
         S6F2_dept_catg_heat.grid(row=0, column=1)



      def backtomainmenu():
         frame1.destroy()
         frame2.destroy()
         frame3.destroy()
         frame4.destroy()
         frame5.destroy()
         self.main_menu_widgets()

      def backtoglobalstats():
         frame1.destroy()
         frame2.destroy()
         frame3.destroy()
         frame4.destroy()
         frame5.destroy()
         self.global_stats_menu(date, eval_instance)
      
      backButton =Button(frame3, text = 'Volver', command=backtoglobalstats)
      backButton.grid(row=0, column=0, padx=10)

      initButton = Button(frame3, text = 'Inicio', command = backtomainmenu)
      initButton.grid(row=0, column=1) 



if __name__ == '__main__':

# Read menu
   root = Tk()
   
   #root.config(bg='white')
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


