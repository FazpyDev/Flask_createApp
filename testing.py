import os
import shutil
from rich import print

running = True

class SettingFunctionsClass():

    def BasicChangePort(self, lines, appPath):

        found = False
        for i, line in enumerate(lines):
            if "debug" in line:
                found = True
                runLine = lines[i]
                port = input("What port would you like to change it to? ")
                runLine = f'    app.run(host="0.0.0.0", debug=True, port={port})'
                lines[i] = runLine
                with open(appPath, "w") as f:
                    f.writelines(lines)
        if not found:
            ErrorPrint("app.run has not been found!")
        else:
            SuccessPrint("Successfully changed the Port!")


    def Exit(self, *args):
        global running
        running = False

def NuminRange(num, list):
    index = num-1
    if index in range(0, len(list)):
        return True
    else:
        return False
    
def find(lst, value):
    try:
        return lst.index(value)
    except ValueError:
        return -1

def SuccessPrint(inputText):
    ColorPrint(inputText, "green")

def ErrorPrint(inputText):
    ColorPrint("Error: " + inputText, "red")

def ColorPrint(inputText, color):
    print(f"[{color}]{inputText}[/{color}]", end="\n")

def ColorInput(inputText, color):
    ColorPrint(inputText, color)
    inpt = input()
    return inpt

def QueryManager(list, inputText):
    for i, element in enumerate(list):
        print(f"{i+1}. {element}")

    InitialText = f"{inputText} Enter a number between 1 and {len(list)} "
    ErrorText = f"Invalid input, please enter a number between 1 and {len(list)} "
    num = int(ColorInput(InitialText, "purple"))
    while not NuminRange(num, list):
        num = int(ColorInput(ErrorText, "red"))
    index = num-1
    return index

SettingFunctions = SettingFunctionsClass()