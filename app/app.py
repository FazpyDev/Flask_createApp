import os
import shutil
import json
from template_Functions import SettingFunctionsClass
from utils import ColorPrint, ErrorPrint

running_state = {"running": True}

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

TemplateOptions = {}

with open("TemplateSettings.json", "r") as f:
    TemplateOptions = json.load(f)

TemplateOptionsKeys = list(TemplateOptions.keys())
TemplateOptionsValues = list(TemplateOptions.values())

SettingFunctionsNames = [name for name in dir(SettingFunctions)]

SettingFunctionsMethod_list = [getattr(SettingFunctions, name) for name in dir(SettingFunctions) if callable(getattr(SettingFunctions, name)) and not name.startswith("__")]


def main():

    name = input("Enter the name of the folder: ")
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    templates_path = os.path.join(BASE_DIR, "templates")
    templates = os.listdir(templates_path)

    templateIndex = QueryManager(templates, "Choose a template from the list above.")
    TemplateType = templates[templateIndex]
    source_folder = os.path.join(templates_path, TemplateType)
    destination_parent = os.getcwd()
    new_folder_name = name

    destination_folder = os.path.join(destination_parent, new_folder_name)
    shutil.copytree(source_folder, destination_folder)

    yesorno =  input("Would you like to edit something or continue?: Y | N ")
    if yesorno == "Y":
        while running_state["running"]:

            OptionsKeyIndex = find(TemplateOptionsKeys, TemplateType)
            if OptionsKeyIndex != -1:
                Options = TemplateOptionsValues[OptionsKeyIndex]

                OptionsKeys = Options.keys()
                OptionsValues = list(Options.values())

                index = QueryManager(OptionsKeys, "Choose what you want to edit.")
                FuncionName = OptionsValues[index]
                
                SettingFunctionsNames = [name for name in dir(SettingFunctions)]

                if FuncionName in SettingFunctionsNames:
                    

                    appPath = os.path.join(destination_folder, "app.py")
                    lines = []
                    with open(appPath, "r") as f:
                        lines = f.readlines()

                    func = SettingFunctionsMethod_list[SettingFunctionsNames.index(FuncionName)]
                    if FuncionName != "Exit":
                        func(lines, appPath)
                    else:
                        func(running_state)
                else:
                    ErrorPrint(f"function {FuncionName} not found for {TemplateType}, if this is a custom Template, make sure to add the function into template_Functions.py")
            else:
                
                ErrorPrint(f"No Options found for {TemplateType}, if this is a custom Template make sure to add a settings to TemplateSettings.json.")
                SettingFunctions.Exit(running_state)

if __name__ == "__main__":
    main()