#Modules
import random
import math
import matplotlib.pyplot as plt
import numpy as np
import time
import string
import copy
#Classes

#General Question Class
class Question():
    def __init__(self):
        self.solution = []
        self.prompt = ""
        self.analysis = []
        self.timeToSolve = 0
        self.coefficients = []
        self.graphAvailable = False

    def printTime(self) -> None:
        print(f"{finishMessages[random.randint(0, len(finishMessages)-1)]}. This question was finished in approximately {round(self.timeToSolve, 3)} seconds")

    def invokeAnalysisType(self) -> None:
        newAnalysisPrompt = analysisprompt
        convertedMapping = []
        for i in range(2,len(self.analysis), 3):
            newAnalysisPrompt += self.analysis[i-2] + " - " + self.analysis[i-1] + "\n"
            convertedMapping.append(self.analysis[i-2])
            convertedMapping.append(self.analysis[i-1])
        else:
            newAnalysisPrompt += "\n"
        return newAnalysisPrompt,convertedMapping


    def plotGraph(self,degree:int,depth:int,solutions:list,variablename:str,coefficients:list = None,subLambda = None):
        if not self.graphAvailable:return False
        #Initialization
        plt.grid()
        plt.title("Problem Analysis")
        plt.xlabel(variablename)
        plt.ylabel(f"f({variablename})")
        if not subLambda:
            subLambda = lambda x: sum([coefficients[i]*(x**(degree-i)) for i in range(len(coefficients))])
        dist = min([abs(0-solution) for solution in solutions])
        BasePlot = np.linspace(solutions[0]-depth-dist, solutions[-1]+depth+dist, 100)
        plt.plot(BasePlot, BasePlot, linewidth = 0)
        plt.plot(BasePlot, list(map(subLambda, BasePlot)))
        plt.plot(BasePlot, [0 for i in range(len(BasePlot))], color = "black")
        plt.plot([0 for i in range(len(BasePlot))], list(map(subLambda, BasePlot)), color = "green")
        plt.scatter(solutions, [0 for i in range(len(solutions))], color = "blue")
        plt.scatter([0], [0], color = "red")
        plt.draw()
        return subLambda
        

class Quadratic(Question):
    def __init__(self):
        super().__init__()
        self.equation = ""
        self.variable = "x"
        self.degree = 2
    #Generates a question with a prompt and analysis    
    def generateQuestion(self, problemCount:int) -> None:
        #Generating Problem
        variable = string.ascii_lowercase[random.randint(0,25)]
        self.variable = variable
        self.graphAvailable = True
        problem = ""
        prompt = ""
        analysis = chr(10)
        a = -1
        b = -1
        c = 1
        randomval = random.randint(-6,6)
        monic = randomval%2==0
        roots = (random.randint(-10,10), random.randint(-10,10))
        if monic:a=1
        else:a=randomval
        b = -(sum(roots))*a
        for val in roots:c*=val
        else:c*=a
        coefficients = [a,b,c]
        coefficientscopy = copy.deepcopy(coefficients)
        variablemap = [f"{variable}^2", variable, ""]
        problem = self.formEquation([*coefficients], variablemap)


        #Generating Prompt and Analysis
        prompt += chr(10)
        prompt += f"PROBLEM {problemCount}\n" + chr(10)
        prompt += f"Consider the quadratic function f({variable}) = {problem}, given that f({variable}) is zero, solve for {variable}\n"
        analysis += "ANALYSIS\n\n"
        analysis += f"Firstly setup the quadratic formula with your values: (-({b})±sqrt(({b})^2 - 4({a})*({c})))/2({a})\n"
        analysis += f"Simplify the equation down to: ({-b}±{((b)**2 -4*a*c)**0.5})/{2*a}\n"
        analysis += f"This gives us the two values of {variable}, {roots[0]} and {roots[1]}\n"
        self.analysis.append("1")
        self.analysis.append("Quadratic Formula")
        self.analysis.append(analysis)
        analysis = chr(10) + "ANALYSIS\n\n"
        if not monic:analysis += f"First divide through by the leading coefficient to get {self.formEquation([coefficient/a for coefficient in coefficients], variablemap)} = 0\n"
        analysis += f"We produce a complete square by dividing the coefficient of the degree 1 term by 2 and and squaring it to form a complete square of the form (x+b/2)^2.\nThe constants from this process and the original quadratic need to be transferred to the other side."
        analysis += f"The equation now becomes: (x+({b/(2*a)}))^2 = {-c/a+(b**2)/(4*(a**2))}\n"
        analysis += f"As such we can square root both sides and get x+({b/(2*a)}) = ±{(-c/a+(b**2)/(4*(a**2)))**0.5}"
        analysis += f"Thus we get our solutions which are {((-c/a+(b**2)/(4*(a**2)))**0.5) - b/(2*a)} and {-((-c/a+(b**2)/(4*(a**2)))**0.5) - b/(2*a)}\n"
        self.analysis.append("2")
        self.analysis.append("Completing the Square")
        self.analysis.append(analysis)
        analysis = chr(10) + "ANALYSIS\n\n"
        if monic:
            analysis += f"Find the two values which multiple to equal the constant and add to equal the coefficient of the x term (b), these values are {-roots[0]} and {-roots[1]}\n"
            analysis += f"The quadratic can now be written as (x+({-roots[0]}))(x+({-roots[1]}))\n"
            analysis += f"As such we can deduce that if this expression were to equal 0 then one of these brackets must be zero following from the zero product property.\nThus x has to be either {roots[0]} or {roots[1]}\n"
            self.analysis.append("3")
            self.analysis.append("Factoring Method")
            self.analysis.append(analysis)
        self.equation = problem
        self.solution = sorted(roots)
        print(self.solution)
        self.prompt = prompt
        self.coefficients = coefficientscopy

    #Produces a quadratic equation string based off a list of coefficients
    def formEquation(self,coefficientlist:list, variablemap:list) -> str:
        clist = coefficientlist
        for index in range(len(coefficientlist)):
            val = ""
            coefficient = str(coefficientlist[index])
            if float(coefficient) == 0:
                coefficientlist[index] = ""
                continue
            if float(coefficient) == 1 and index<2:coefficient = ""
            elif float(coefficient) == -1 and index<2:coefficient = "-"
            if index < 2:
                if clist[index+1] > 0:
                    val = coefficient + variablemap[index] + "+"
                else:
                    val = coefficient + variablemap[index]
            else:
                if clist[index] >= 0 and "+" not in clist[index-1]:val = "+" + coefficient + variablemap[index]
                else:val = coefficient + variablemap[index]
            clist[index] = val
        return ''.join(clist)
    
    def createGraph(self, depth:int) -> None:
        if self.graphAvailable:
            if self.coefficients:
                self.plotGraph(self.degree,depth,self.solution,self.variable,self.coefficients)
        


    
class CoordinateGeometry(Question):
    def __init__(self):
        super().__init__()

class RootsOfPolynomials(Question):
    def __init__(self):
        super().__init__()
    

#Variables
mainPrompt = "Welcome to the GCSE and A-level mathematical accuracy training range. In this program you'll be able to train and improve your mathematical accuracy. \nThe higher your mathematical accuracy the less silly mistakes you'll make. In this program you'll be able to pick from a variety of different types of problems ranging from easy to hard, which you can solve, analyse afterwards, in a multitude of different modes. "
baselevelPrompt = "What level would you like to practice in? Please enter your choice as the number corresponding with the respective level:\n"
basemodePrompt = "What mode would you like to train in:\n"
basequestionprompt = "What question type would you like to train in:\n"
levelMapping = ["1", "GCSE", "2", "A-Level"]
modeMapping = ["1", "Practice (Standard Mode)", "2", "Death Run (Get one wrong and you're out!)"]
questionArchive = [("1", "Quadratics", "1", Quadratic), ("2", "Coordinate Geometry", "1", CoordinateGeometry), ("1", "Roots of Polynomials (Vieta's formulas)", "2", RootsOfPolynomials)]
finishMessages = ["Legendary", "Magnificent work", "Well done", "You are on fire", "Don't stop cooking because you're Gordon Ramsay", "Colder than Ice"]
analysisprompt = "Of which of these methods would you like to view the analysis? Enter -1 to exit the analysis\n"
filterInputLambda = lambda string: "".join([char for char in string if char.isnumeric() or char == "-"])
wordInString = lambda word, string: ''.join(list(dict.fromkeys([char for char in word if char.lower() in string.lower()]))) == word



#Converts base prompt to include all the choices
def convertPrompt(prompt:str, mapping:str) -> str:
    newPrompt = prompt
    for i in range(1,len(mapping), 2):
        newPrompt += mapping[i-1] + " - " + mapping[i] + "\n"
    else:
        newPrompt += "\n"
    return newPrompt

#Filters questions by level
def filterQuestions(questions:list, choice:str) -> list:
    newQuestions = []
    for question in questions:
        if question[2] == choice:
            newQuestions = [*newQuestions, question[0], question[1]]
    return newQuestions


def FilterClasses(questions:list, choice:str) -> list:
    newClasses = []
    for question in questions:
        if question[2] == choice:
            newClasses = [*newClasses, question[3]]
    return newClasses

#Specialised input function
def superInput(mapping:list, prompt:str) -> str:
    choice = ""
    generalPrompt = convertPrompt(prompt, mapping)
    while choice not in mapping:
        choice = input(generalPrompt)
        if wordInString("exit", choice):return "exit"
        choice = filterInputLambda(choice)
        if choice not in mapping:
            print("Please re-enter your choice.")
    return choice

def filterInput(string:str) -> list:
    Done = False
    values = []
    tempstr = ''
    for char in string:
        if char.isnumeric() or char in ".-":
            Done = True
        else:
            Done = False
            values.append(tempstr)
            tempstr = ''
        if Done: tempstr += char
    else:
        values.append(tempstr)
    return [float(char) for char in values]

def validateInput(solutions:list, answer:list) -> bool:
    if len(solutions)!=len(answer):return False
    return all([x==y for x,y in zip(sorted(solutions), sorted(answer))])

def initiateQuestion(instance, mode:bool, streak:int = 0) -> float:
    print(instance.prompt)
    solutionVerified = False
    solved = False
    begintime = time.time()
    while not solved:
        while not solutionVerified:
            solutionInput = input("Enter your solution here: ")
            try:
                solutionInput = filterInput(solutionInput)
                solutionVerified = True
            except ValueError:
                if wordInString("exit",solutionInput):
                    return -1
                print("This isn't good enough, make sure your solution is valid.")
        solved = validateInput(solutionInput, instance.solution)
        if not solved:
            print("Your solution is wrong.")
            if mode:
                print(f"Unfortunately your run has ended with a streak of {streak}")
                return False
            solutionVerified = False
    endtime = time.time()
    timeTaken = endtime-begintime
    timeTaken = round(timeTaken,2)
    instance.timeToSolve = timeTaken
    instance.printTime()
    print(chr(10))
    return timeTaken

def invokeFullQuestion(mode:str, question:str, level:str, problemCount:int, modeOption:bool, streak:int = 0) -> bool:
    analysischoice = 0
    questionClasses = FilterClasses(questionArchive, level)
    instance = questionClasses[int(question)-1]()
    instance.generateQuestion(problemCount)
    analysis = instance.invokeAnalysisType()
    analysiscopy = copy.deepcopy(analysis[1])
    originalanalysis = copy.deepcopy(instance.analysis)
    analysiscopy.append("-1")
    if modeOption:timeTaken = initiateQuestion(instance, True, streak)
    else:timeTaken = initiateQuestion(instance, False)
    if not timeTaken:return True
    while len(originalanalysis)>0:
        analysischoice = superInput(analysiscopy, analysisprompt)
        if analysischoice == "exit":return True
        if analysischoice == "-1":
            break
        analysischoice = filterInputLambda(analysischoice)
        print(originalanalysis[(int(analysischoice)*3)-1])
        if analysischoice in analysiscopy:
            analysiscopy = convertAnalysis(analysiscopy, analysischoice, True)
            originalanalysis = convertAnalysis(originalanalysis, analysischoice, False)
    print("ANALYSIS DONE")
    if instance.graphAvailable:
        graphChoice = input("Would you like to view the graphical analysis, enter YES to see the graph and NO to proceed. Once the graph is closed then you can continue.\n")
        if wordInString(graphChoice, "yes"):
            instance.createGraph(5)
            plt.show()
        elif wordInString(graphChoice, "exit"):
            return True
    return False

def convertAnalysis(analysis:list,pos:str, mode:bool) -> list:
    if mode:num=2
    else:num=3
    newanalysis = copy.deepcopy(analysis)
    numcount = 1
    index = analysis.index(pos)
    for i in range(num):newanalysis.pop(index)
    for position,char in enumerate(newanalysis):
        if char.isnumeric():
            newanalysis[position] = str(numcount)
            numcount+=1
    return newanalysis




#Initial part of the UI to ask the user where they want to proceed
def invokeUser(introPrompt:str, levelChoicePrompt:str, levelChoiceMapping:list, intromodePrompt:str, modeChoiceMapping:list, introquestionPrompt:str) -> None:
    for i in range(1):print(chr(10))
    print(introPrompt)
    for i in range(1):print(chr(10))
    levelInput = superInput(levelChoiceMapping, levelChoicePrompt)
    modeInput = superInput(modeChoiceMapping, intromodePrompt)
    questionInput = superInput(filterQuestions(questionArchive, levelInput), introquestionPrompt)
    enterPractice(modeInput, questionInput, levelInput)

#Intermediate stage between UI and practice
def enterPractice(mode:str, question:str, level:str) -> None:
    problemCount = 1
    if mode == "1":
        print('Enter "exit" to exit at any time\n')
        while not invokeFullQuestion(mode,question,level,problemCount, False):
            problemCount += 1
    elif mode == "2":
        print('Enter "exit" to exit at any time\n')
        while not invokeFullQuestion(mode,question,level,problemCount, True, problemCount-1):
            problemCount += 1

        

invokeUser(mainPrompt, baselevelPrompt, levelMapping, basemodePrompt, modeMapping, basequestionprompt)
