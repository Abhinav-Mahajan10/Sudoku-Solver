from Process_Image import Start_Solving, GUI_And_Processing
import os

if __name__ == "__main__":
    print("Sudoku Solver: -")
    print("These are your options")
    print("1.) The unsolved Sudoku pictures are in your phone")
    print("2.) The unsolved Sudoku picture is in your laptop you are running this program on")
    print("Enter 1 or 2")
    var = input()
    var = int(var)
    if var == 1:
        print("After IP address is disclosed, we are clear for receiving uploads.")
        os.system('python D:\VSCode\Project/Flask_Server.py')
    elif var == 2:
        print("Enter image path name")
        print("Note:")
        print("If image is in the program folder, then just enter the image file name.extension")
        print("Else enter the path correctly followed by the file name.extension")
        pathname = input()
        Start_Solving(pathname)
    else:
        print("Please enter only 1 or 2")