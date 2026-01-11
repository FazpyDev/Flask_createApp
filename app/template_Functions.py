from utils import ErrorPrint, SuccessPrint, ColorPrint
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


    def Exit(self, running_state, *args):
        running_state["running"] = False