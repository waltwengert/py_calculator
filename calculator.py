###Known bug when % or / by 0

import tkinter as tk

HEIGHT = 280
WIDTH = int((HEIGHT/4)*3) #width is always 3/4 height
DISPLHEIGHT = int(HEIGHT/4) #display takes 1/4 height

BTNHEIGHT = 2 ########################
BTNWIDTH = 6 #########################

window = tk.Tk()
window.title("Calculator")
window.geometry("%dx%d" % (WIDTH, HEIGHT))
window.resizable(0, 0) #prevent resizing

displStr = tk.StringVar()
displStr.set("0") #start the calculator empty

current = 0 #the number displayed
previous = 0 #the number before operation started
operator = "0" #"0" is unset
decNo = 0 #the number decimal place

#the calculator's display or output 
frDispl = tk.Frame(window, width=WIDTH, height=DISPLHEIGHT, background="grey")
frDispl.pack()
frDispl.pack_propagate(0) #stops widgets messing with their parents config

lblDispl = tk.Label(frDispl, textvariable=displStr)
lblDispl.pack(side="right")

#a separate frame just for the buttons
frButtons = tk.Frame(window, width=WIDTH, height=HEIGHT-DISPLHEIGHT)
frButtons.pack()
frButtons.pack_propagate(0) #stops widgets messing with their parents config

#funbuttons slightly different properties so have to assign separately
bDiv = tk.Button(frButtons, text="/", command = lambda : numPress("/"))
bMod = tk.Button(frButtons, text="%", command = lambda : numPress("%"))
bNeg = tk.Button(frButtons, text="-X", command = lambda : numPress("-X"))
bC = tk.Button(frButtons, text="C", command = lambda : numPress("C"))
bMult = tk.Button(frButtons, text="*", command = lambda : numPress("*"))
bSub = tk.Button(frButtons, text="-", command = lambda : numPress("-"))
bAdd = tk.Button(frButtons, text="+", command = lambda : numPress("+"))
bEq = tk.Button(frButtons, text="=", command = lambda : numPress("="))
bDec = tk.Button(frButtons, text=".", command = lambda : numPress("."))

#list of buttons to allow batch configs
funcButtons = [bDiv, bMod, bNeg, bC, bMult, bSub, bAdd, bEq, bDec]

for btn in funcButtons: #batch config function buttons
    btn.config(height=BTNHEIGHT, width=BTNWIDTH)

#place function buttons in their appropriate position
bDiv.grid(row=0, column=3)
bMod.grid(row=0, column=2)
bNeg.grid(row=0, column=1)
bC.grid(row=0, column=0)
bMult.grid(row=1, column=3)
bSub.grid(row=2, column=3)
bAdd.grid(row=3, column=3)
bEq.grid(row=4, column=3)
bDec.grid(row=4, column=2)

#create and place number buttons
for i in range(9, -1, -1): #last number (-1) is loop increment
    btn = tk.Button(frButtons)
    btn.config(text="%d" % (i), command = lambda i=i: numPress(i), \
              height=BTNHEIGHT, width=BTNWIDTH)
    if i == 0:
        #0 on row 4
        btn.grid(row=4)
    elif i <= 3:
        #1-3 on row 3
        btn.grid(row=3, column=(i+2)%3)
    elif i <= 6:
        #4-6 on row 2
        btn.grid(row=2, column=(i+2)%3)
    elif i <= 9:
        #7-9 on row 1
        btn.grid(row=1, column=(i+2)%3)

#function for any calculator button clicked, each passes its ID 
def numPress(clicked):
    global displStr 

    global current #the number displayed
    global previous #the number before operation started
    global operator #"0" is unset
    global decNo #the number decimal place
    calculation = [previous, current, operator] 
    print(calculation)
    
    numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    if clicked in numbers: #user clicked a number
        if current == 0 or current == previous:
            current = clicked
        elif decNo > 0:
            current += (clicked / (10**decNo)) #add digits in the decimals
            current = round(current, decNo) #round to the current decimal place
            decNo += 1
        else:
            current *= 10 #move up a tenth place
            current += clicked
    elif clicked == "C": #clear
        current = 0
        operator = "0"
        decNo = 0
    elif clicked == "-X": #negative
        if current != previous: #ensure a negative can't happen mid operation
            current *= -1
    elif clicked == ".": #decimal
        decNo += 1
    elif clicked == "=": #equals
        current = evaluate(calculation)
        operator = "0"
        decNo = 0
    else: #one of the 5 operations
        if operator != "0": #evaluate then set up next operation
            current = evaluate(calculation)
            operator = clicked
        else: #first operation
            previous = current
            operator = clicked
            return #so that the display isn't updated

    if current % 1 == 0: #if current is a whole number
        current = int(current) #ensure it's an int so e.g. 5.0 isn't displayed
    displStr.set(current)

#function to evaluate a statement given two numbers and an operator
def evaluate(calculation):
    if calculation[2] == "+":
        return calculation[0] + calculation[1]
    elif calculation[2] == "-":
        return calculation[0] - calculation[1]
    elif calculation[2] == "*":
        return calculation[0] * calculation[1]
    elif calculation[2] == "/":
        return calculation[0] / calculation[1]
    elif calculation[2] == "%":
        return calculation[0] % calculation[1]

window.mainloop()
