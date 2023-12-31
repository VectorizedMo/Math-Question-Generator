#Modules
import random
import math
import matplotlib.pyplot as plt
import numpy as np
import time
import string
import copy

#Classes

#Every question type has it's own class with a general question class as it's parent
#Every question type has a function to generate the question with a prompt, solution, analysis and optional graph analysis. 

#The generation function is called generateQuestion and the graph analysis function is called createGraph()

#General Question Class
class Question():
    #Initialization function for all question types
    def __init__(self) -> None:
        self.solution = []
        self.prompt = ""
        self.analysis = []
        self.timeToSolve = 0
        self.coefficients = []
        self.graphAvailable = False
    
    #Prints the time taken for a given question along with a cool congratulations message
    def printTime(self) -> None:
        print(f"{finishMessages[random.randint(0, len(finishMessages)-1)]}. This question was finished in approximately {round(self.timeToSolve, 3)} seconds")

    #For a question analysis, provides a prompt segment and a converted mapping
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
    
    #Plots a graph for a polynomial or a function given by the user. If polynomial then degree needs to be given.
    #Takes two range points to base the scale off off, keypoints to highlight, and an "origin line" of which the x value is distrelative.
    #Depth is simply addition by some integer to the scale of the plot. Coefficients are for the polynomial setting.
    def plotGraph(self,degree:int,depth:int,keypoints:list,rangepoints:list,distrelative:int,coefficients:list = None,subLambda = None):
        if not self.graphAvailable:return False
        if not subLambda:
            subLambda = lambda x: sum([coefficients[i]*(x**(degree-i)) for i in range(len(coefficients))])
        dist = min([abs(distrelative-rangepoint) for rangepoint in rangepoints])
        BasePlot = np.linspace(rangepoints[0]-depth-dist, rangepoints[-1]+depth+dist, 100)
        plt.plot(BasePlot, list(map(subLambda, BasePlot)))
        plt.scatter(keypoints, [subLambda(keypoint) for keypoint in keypoints], color = "blue")
        plt.draw()
        return subLambda
    
    #Collects the BasePlot and mapped BasePlot. The BasePlot is essentially the endpoints from which the graph is drawn. 
    def collectBasePlot(self,range:list,depth:int,distrelative:int ,subLambda) -> list:
        dist = min([abs(distrelative-rangepoint) for rangepoint in range])
        BasePlot = np.linspace(range[0]-depth-dist, range[-1]+depth+dist, 100)
        BasePlot2 = list(map(subLambda, BasePlot))
        return BasePlot,BasePlot2
    
    #Creates and returns a polynomial function based on a it's degree and coefficients.
    def collectSubLambda(self,coefficients:list, degree:int):
        subLambda = lambda x: sum([coefficients[i]*(x**(degree-i)) for i in range(len(coefficients))])
        return subLambda
    
    #Initializes the plot by writing titles, choosing scales and drawing axes
    def basePlot(self, variablename:str, baseplots:list, baseplots2:list, mode:bool = False):
        plt.grid()
        plt.title("Problem Analysis")
        plt.xlabel(variablename)
        plt.ylabel(f"f({variablename})")
        ultList = []
        ultList2 = []
        for baseplot in baseplots:
            ultList = [*ultList, min(baseplot), max(baseplot)]
        for baseplot in baseplots2:
            ultList2 = [*ultList2, min(baseplot), max(baseplot)]
        ultList = [min(ultList), max(ultList)]
        ultList2 = [min(ultList2), max(ultList2)]
        decidelist = [ultList, ultList2]
        abslambda = lambda x: sum([abs(val) for val in x])
        abslist = list(map(abslambda,decidelist))
        index = abslist.index(max(abslist))
        chosenlist = decidelist[index]
        if mode:
            chosenlist = ultList
            plt.plot(chosenlist, [0 for i in range(len(chosenlist))], color = "black")
            plt.plot([0 for i in range(len(ultList2))],ultList2, color = "green")
        else:
            plt.plot(chosenlist, [0 for i in range(len(chosenlist))], color = "black")
            plt.plot([0 for i in range(len(chosenlist))],chosenlist, color = "green")
        plt.scatter([0], [0], color = "red")
        plt.plot(chosenlist, chosenlist, linewidth = 0)
        return chosenlist

class Quadratic(Question):
    def __init__(self):
        super().__init__()
        self.equation = ""
        self.variable = "x"
        self.degree = 2

    def generateQuestion(self, problemCount:int) -> None:
        #Generating problem
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
        roots = (round(random.randint(-50,50)/5,3), round(random.randint(-50,50)/5,3))
        if monic:a=1
        else:a=randomval
        b = -(sum(roots))*a
        for val in roots:c*=val
        else:c*=a
        coefficients = [a,b,c]
        for i,coefficient in enumerate(coefficients):coefficients[i] = round(coefficient,3)
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
        self.prompt = prompt
        self.coefficients = coefficientscopy
        print(self.solution)
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
                subLambda = self.collectSubLambda(self.coefficients, self.degree)
                baseplottuple = self.collectBasePlot(self.solution, depth, 0, subLambda)
                self.basePlot(self.variable, [baseplottuple[0]], [baseplottuple[1]], True)
                self.plotGraph(self.degree, depth, self.solution, self.solution,0,self.coefficients)
        


    
class CoordinateGeometry(Question):
    def __init__(self):
        super().__init__()
        self.graphAvailable = True
        self.formula = ""
        self.variable = "x"
        self.degree = 1
        self.keypoint = []
        self.range = []

    def generateQuestion(self, problemCount:int) -> None:
        #Seed is used to randomly pick from a multitude of subquestion types
        seed = random.randint(0,100)
        seed = 81
        if seed >= 80:
            #Generating Question
            xsample = random.randint(-5,5)
            slope = random.randint(-8,8)
            while slope == 0:
                slope = random.randint(-8,8)
            yintercept = random.randint(-10,10)
            if yintercept > 0:
                formula = f"y = {slope}x+{yintercept}"
            else:
                formula = f"y = {slope}x{yintercept}"
            ysample = (xsample*slope) + yintercept
            perpslope = round(-1/slope,3)
            perpcept = ysample-(perpslope*xsample)
            coefficient1 = [slope,yintercept]
            coefficientperp = [perpslope, perpcept]
            xintercept = (-yintercept)/(slope)
            self.formula = formula
            self.coefficients = [*self.coefficients, coefficient1, coefficientperp]
            self.solution = [perpslope, perpcept]
            self.range = sorted([-xintercept,xintercept])
            self.keypoint = [xsample]
            #Generate Prompt
            self.prompt += chr(10)
            self.prompt += f"PROBLEM {problemCount}\n" + chr(10)
            randomletter = string.ascii_uppercase[random.randint(0,25)]
            self.prompt += f"Consider the formula l: {formula} and the point {randomletter}: ({xsample}, {ysample}), there exists a line perpendicular to l which passes through {randomletter} of which can be expressed in the form y = mx+c\nFind m and c\n"
            currentanalysis = chr(10)
            currentanalysis += f"To find the gradient (m) of the line that is perpendicular to {formula}, you need to find the negative reciprocal of {slope}, which is -1/{slope} or {perpslope}.\n"
            currentanalysis += f"Now that we have the gradient we need to find the y intercept. We have y = {perpslope}x+c. Given that this line passes through {randomletter} we have {ysample} = {perpslope}*{xsample}+c.\n"
            currentanalysis += f"Now we can just minus the term of the leading coefficient from both sides to get {ysample - perpslope*xsample} = c. This gives us our y intercept c, because when x = 0, this is the value of y.\n"
            currentanalysis += f"Thus we have m: {perpslope} and c: {perpcept}\n"
            self.analysis.append("1")
            self.analysis.append("Standard Method")
            self.analysis.append(currentanalysis)
            
    def createGraph(self, depth:int) -> None:
        baseplots = []
        mappedbaseplots = []
        for coefficient in self.coefficients:
            subLambda = self.collectSubLambda(coefficient, self.degree)
            baseplotstuple = self.collectBasePlot(self.range, depth,self.keypoint[0] ,subLambda)
            baseplots.append(baseplotstuple[0])
            mappedbaseplots.append(baseplotstuple[1])
        else:
            self.basePlot(self.variable, baseplots, mappedbaseplots)
        for coefficients in self.coefficients:
            self.plotGraph(self.degree, depth, self.keypoint, self.range,self.keypoint[0],coefficients)

class RootsOfPolynomials(Question):
    def __init__(self):
        super().__init__()
        self.graphAvailable = False
        self.degree = -1
        self.equation = ""

    def generateQuestion(self, problemCount:int) -> None:
        def convert(mtransform:int, atransform:int, rootsym:str):
            if atransform > 0:
                return f"{mtransform}{rootsym}+{addtransform}"
            else:
                return f"{mtransform}{rootsym}{addtransform}"
        self.degree = 2
        generator = Quadratic()
        generator.generateQuestion(0)
        while 0 in generator.solution:
            generator.generateQuestion(0)
        self.equation = generator.equation
        multiplytransform = random.randint(-4,4)
        while multiplytransform == 0:
            multiplytransform = random.randint(-4,4)
        addtransform = random.randint(-8,8)
        self.solution = [round(-((multiplytransform*generator.solution[0]+addtransform)+(multiplytransform*generator.solution[1]+addtransform))/((multiplytransform*generator.solution[0]+addtransform)*(multiplytransform*generator.solution[1]+addtransform)),3)]
        prompt = chr(10)
        randomletters = random.sample(string.ascii_uppercase, 3)
        prompt += f"PROBLEM {problemCount}\n" + chr(10)
        prompt += f"A quadratic function is in the form ax^2+bx+c. The quadratic equation {generator.equation} = 0, has roots {randomletters[0]}, {randomletters[1]}\n"
        prompt += f"A different quadratic equation {randomletters[2]} has the roots {convert(multiplytransform, addtransform, randomletters[0])}, {convert(multiplytransform, addtransform, randomletters[1])}\n"
        prompt += f"Find the ratio between b and c\n"
        self.prompt = prompt
        analysis = chr(10)
        analysis += f"Given Vieta's formulas -b/a = {randomletters[0]} + {randomletters[1]} and c/a = {randomletters[0]} * {randomletters[1]}\n"
        analysis += f"Thus {round(-generator.coefficients[1]/generator.coefficients[0],3)} = {randomletters[0]} + {randomletters[1]} and {round(generator.coefficients[2]/generator.coefficients[0],3)} = {randomletters[0]} * {randomletters[1]}\n"
        analysis += f"Take out the common factor {multiplytransform} so that -b/a = {multiplytransform}({randomletters[0]}+({randomletters[1]})) + ({addtransform*2})\n"
        analysis += f"Thus -b/a = {multiplytransform}({round(-generator.coefficients[1]/generator.coefficients[0],3)}) + ({addtransform*2})\n"
        analysis += f"Which simplifies to -b/a = {round((multiplytransform) * -generator.coefficients[1]/generator.coefficients[0] + addtransform*2,3)}\n"
        analysis += f"We have c/a  = ({convert(multiplytransform, addtransform, randomletters[0])})*({convert(multiplytransform, addtransform, randomletters[1])})\n"
        analysis += f"We have c/a = ({multiplytransform**2}{randomletters[0]}{randomletters[1]} + {multiplytransform*addtransform}({randomletters[0]}+{randomletters[1]}) + {addtransform**2})\n"
        analysis += f"Using our formulas we get {round((multiplytransform**2)*generator.solution[0]*generator.solution[1],3)} + {multiplytransform*addtransform}({round(generator.solution[0]+generator.solution[1],3)}) + {addtransform**2}\n"
        analysis += f"Finally we get c/a = {round((multiplytransform**2)*generator.solution[0]*generator.solution[1] + multiplytransform*addtransform*(generator.solution[0]+generator.solution[1]) + addtransform**2, 3)}\n"
        analysis += f"Now we divide b/a by c/a to get {self.solution[0]}\n"
        self.analysis.append("1")
        self.analysis.append("Vieta's formulas")
        self.analysis.append(analysis)

    def createGraph(self, depth:int) -> None:
        return False

#Variables
mainPrompt = "Welcome to the GCSE and A-level mathematical accuracy training range. In this program you'll be able to train and improve your mathematical accuracy. \nThe higher your mathematical accuracy the less silly mistakes you'll make. In this program you'll be able to pick from a variety of different types of problems ranging from easy to hard, which you can solve, analyse afterwards, in a multitude of different modes.\nEnter exit at any time to stop."
baselevelPrompt = "What level would you like to practice in? Please enter your choice as the number corresponding with the respective level:\n"
basemodePrompt = "What mode would you like to train in:\n"
basequestionprompt = "What question type would you like to train in:\n"
levelMapping = ["1", "GCSE", "2", "A-Level"]
modeMapping = ["1", "Practice (Standard Mode)", "2", "Death Run (Get one wrong and you're out!)"]
questionArchive = [("1", "Quadratics", "1", Quadratic), ("2", "Coordinate Geometry", "1", CoordinateGeometry), ("1", "Roots of Polynomials (Vieta's formulas, Quadratics)", "2", RootsOfPolynomials)]
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

#Filters questions to get their respective classes only
def FilterClasses(questions:list, choice:str) -> list:
    newClasses = []
    for question in questions:
        if question[2] == choice:
            newClasses = [*newClasses, question[3]]
    return newClasses

#Specialised input function with repetition for invalid input.
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

#Filters user input for the answer to gain a list of answers instead of a string
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

#Checks if the answer is correct
def validateInput(solutions:list, answer:list) -> bool:
    if len(solutions)!=len(answer):return False
    return all([x==y for x,y in zip(sorted(solutions), sorted(answer))])

#Asks the question and continues until the user gets it right. If in death mode, upon a wrong answer the question will end and show the user his streak.
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

#Combines the asking of the question with the viewing of question analysis with the potential option of graph analysis.
def invokeFullQuestion(question:str, level:str, problemCount:int, modeOption:bool, streak:int = 0) -> bool:
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
            plt.clf()
        elif wordInString(graphChoice, "exit"):
            return True
    return False

#Removes elements from the analysis and changes the numbers so it's in consecutive order.
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
    if levelInput=="exit":return False
    modeInput = superInput(modeChoiceMapping, intromodePrompt)
    if modeInput == "exit":return False
    questionInput = superInput(filterQuestions(questionArchive, levelInput), introquestionPrompt)
    if modeInput == "exit":return False
    enterPractice(modeInput, questionInput, levelInput)

#Intermediate stage between UI and practice
def enterPractice(mode:str, question:str, level:str) -> None:
    problemCount = 1
    if mode == "1":
        print('Enter "exit" to exit at any time\n')
        while not invokeFullQuestion(question,level,problemCount, False):
            problemCount += 1
    elif mode == "2":
        print('Enter "exit" to exit at any time\n')
        while not invokeFullQuestion(question,level,problemCount, True, problemCount-1):
            problemCount += 1

#Starts the program by invoking the user and collecting input from him.
invokeUser(mainPrompt, baselevelPrompt, levelMapping, basemodePrompt, modeMapping, basequestionprompt)
