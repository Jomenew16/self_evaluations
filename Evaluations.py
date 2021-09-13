import names

class Evaluation:
    evaluators: int = 0
    mx_evaluations: int = 0
    

    def __init__(self, evaluators, mx_evaluations) -> None:
    # parameter evaluators represents the desired number of evaluators of each collaborator. 
    # max_evaluations is the maximum number of evaluations that each colaborator will make. 
        self.evaluators = evaluators
        self.mx_evaluations = mx_evaluations

    def set_interactions(self):
    # This method builds a random matriz of interactions.
    # Receives the number of all collaborators. module names provide random list of names
         
        collaborators = int(input("How many collaborators are there: "))
        assert collaborators > 0, "The number of collaborators has to be a positive number"
        our_names = [names.get_full_name() for i in range(collaborators)]
        print(our_names)
        

    def check_matrix(self):
    #This method checks that the matrix is well build. Transposition of the matrix equals the original one
        pass

    def set_evaluators(self, evaluators, mx_evaluations):
    # Every collaborator will be evaluated by a number of evaluators. 
    # The number of evaluator will be the same for each collaborator, unless, he/she interacts with less people
    # No one will conduct more than a specified number of evaluations
        pass

    def read_interactions(self):
        pass
        
        
    