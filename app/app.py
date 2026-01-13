import os
import shutil
import json
from TemplateFunctions import SettingFunctionsClass
from utils import ColorPrint, ErrorPrint

#// Variables

# Objects

running_state = {"running": True} # This makes it so it will stop running if the user chooses to exit or there is a major error.

template_options = {} # These are what options each template has, e.g. Change Port, and assigns the function ChangePort to it.

settings_functions = SettingFunctionsClass() # This gets the Functions that the TemplateOptions use, e.g. ChangePort which is used by all the Default Templates.

# Constants

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # The directory of app.py, this is to get the Templates folder and TemplateOptions.json, without this you could only run this inside of the app directory
TEMPLATEOPTIONSPATH = os.path.join(BASE_DIR, "TemplateOptions.json") # The path of TemplateOptions.json which is used to map the Options into functions from TemplateFunctions.py

TEMPLATES_PATH = os.path.join(BASE_DIR, "templates") # The path of the Templates directory
TEMPLATEGROUPS = os.listdir(TEMPLATES_PATH) # The Groups inside of Templates, e.g. Flask

DESTINATION_PARENT = os.getcwd() # The path is where app.py is run from and where the Copy of the template will go to 

def is_valid_index(num, QueryOptions): # e.g if the user inputs 1 out of 5 options it will return True, if not it will return False
    return 0 <= num-1 < len(QueryOptions)
    
def ColorInput(inputText, color): # A input with a color
    ColorPrint(inputText, color)
    inpt = input()
    return inpt

def QueryManager(Querylist, inputText): # Prints a numbered list of all the Options and allows the user to pick a option using a number
    for i, element in enumerate(Querylist):
        print(f"{i+1}. {element}")

    InitialText = f"{inputText} Enter a number between 1 and {len(Querylist)} "
    ErrorText = f"Invalid input, please enter a number between 1 and {len(Querylist)} "

    while True:
        try:
            num = int(ColorInput(InitialText, "purple"))
            if is_valid_index(num, Querylist):
                return num-1
        except ValueError:
            ErrorPrint("Please enter a number.")


with open(TEMPLATEOPTIONSPATH, "r") as f: # Turns the TemplateSettings.json into a usable object to access what options the user can use
    template_options = json.load(f)

def main(): # The main function, this is just for the package version

    name = input("Enter the name of the Project: ").strip()
    
    TEMPLATEGROUPINDEX = QueryManager(TEMPLATEGROUPS, "Choose what type of Template you want to make") # Index of the chosen Template Group
    TEMPLATEGROUP = TEMPLATEGROUPS[TEMPLATEGROUPINDEX] # Gets the chosen Group as a string
    TEMPLATEGROUPPATH = os.path.join(TEMPLATES_PATH, TEMPLATEGROUP) # Gets the path of the Template Group, so if you chose option 1, Flask, it will be ("templates/Flask")

    TEMPLATES = os.listdir(TEMPLATEGROUPPATH) # The name of the folders inside of the Chosen TemplateGroup/Type (Default example: Flask)

    TEMPLATEINDEX = QueryManager(TEMPLATES, "Choose a template from the list above.") # The index of what template you chose, so if it is the first one, it would be 0
    TEMPLATETYPE = TEMPLATES[TEMPLATEINDEX] # Gets the name of the Template
    SOURCE_FOLDER = os.path.join(TEMPLATEGROUPPATH, TEMPLATETYPE) # Gets the folder of the chosen template

    destination_folder = os.path.join(DESTINATION_PARENT, name) # The path of the new Folder
    while os.path.exists(destination_folder):
        name = input("Please choose a new name of the project since a directory with that Name already exists: ").strip()
        destination_folder = os.path.join(DESTINATION_PARENT, name)
    shutil.copytree(SOURCE_FOLDER, destination_folder) # Copies the chosen folder with the new name and the directory

    if input(f"Would you like to Change some settings of {name}? (Y/N) ").upper() != "Y": # If you would like to continue with some settings
        return 

    while running_state["running"]: # While the user has not exited or there was not a major error

        options = template_options.get(TEMPLATETYPE) # Gets all of the Options for the chosen Template, this is editable in TemplateOptions.json
        if options: # If they exist
        
            options_keys = list(options.keys()) # The name of each Option, e.g. "Change Port", "Exit"

            index = QueryManager(options_keys, "Choose what you want to edit.") # Gets the index of what option you want to do, e.g. Option 1 Chane Port the index would be 0
            function_name = options[options_keys[index]] # Gets the name of the function connected to the Option, e.g "Change Port" would get "ChangePort" function

            func = getattr(settings_functions, function_name, None) # Gets the actual function from the name and from TemplateFunctions.py
            
            if not callable(func): # If the function does not exist 
                ErrorPrint(
                    f"Function '{function_name}' not found in TemplateFunctions.py"
                )
                continue

            if function_name != "Exit": # If the function is not exit then it adds the templateType and the path of the new Folder
                func(TEMPLATETYPE, destination_folder)
            else:
                func(running_state) # Exits the program by changing the Running state
        else:
            
            ErrorPrint(f"No Options found for {TEMPLATETYPE}, if this is a custom Template make sure to add a settings to TemplateSettings.json.")
            settings_functions.Exit(running_state)

    ColorPrint("Bye bye!", "red")

if __name__ == "__main__":
    main()
