#For image preprocessing
import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import imutils
#For reading image
import easyocr
#For avoiding tensorflow warnings, terminating processes etc.
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
#CNN module to read numbers
from tensorflow.keras.models import load_model
model = load_model('myModel.h5')
#GUI module to print a Sudoku
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
#Basic utility
import copy
#Importing my program file which solves a Sudoku
import My_Sudoku_Solver
Sudoku_object = My_Sudoku_Solver.Sudoku()

def Start_Solving(pathname):
    #print(pathname)
    image_raw = cv2.imread(pathname)
    #plt.imshow(cv2.cvtColor(image_raw, cv2.COLOR_BGR2RGB))
    #plt.show()
    print("Does your image require rotating?")
    print("1.) Clockwise 90 degrees")
    print("2.) Anticlockwise 90 degrees")
    print("3.) 180 degrees rotation")
    print("4.) No rotation required")
    print("Enter the corresponding option number for your choice")
    option = input()
    option = int(option)
    if option == 1:
        rotated_image = cv2.rotate(image_raw, cv2.cv2.ROTATE_90_CLOCKWISE)
        #plt.imshow(cv2.cvtColor(rotated_image, cv2.COLOR_BGR2RGB))
        #plt.show()
        GUI_And_Processing(rotated_image)
    elif option == 2:
        rotated_image = cv2.rotate(image_raw, cv2.cv2.ROTATE_90_CLOCKWISE)
        rotated_image = cv2.rotate(rotated_image, cv2.cv2.ROTATE_90_CLOCKWISE)
        rotated_image = cv2.rotate(rotated_image, cv2.cv2.ROTATE_90_CLOCKWISE)
        #plt.imshow(cv2.cvtColor(rotated_image, cv2.COLOR_BGR2RGB))
        #plt.show()
        GUI_And_Processing(rotated_image)
    elif option == 3:
        rotated_image = cv2.rotate(image_raw, cv2.cv2.ROTATE_90_CLOCKWISE)
        rotated_image = cv2.rotate(rotated_image, cv2.cv2.ROTATE_90_CLOCKWISE)
        #plt.imshow(cv2.cvtColor(rotated_image, cv2.COLOR_BGR2RGB))
        #plt.show()
        GUI_And_Processing(rotated_image)
    elif option == 4:
        GUI_And_Processing(image_raw)
    else:
        print("Invalid input, enter only either 1, 2, 3 or 4")

def GUI_And_Processing(img):
    heightImg = img.shape[0]
    widthImg = img.shape[1]
    heightImg = max(heightImg, widthImg)
    widthImg = heightImg
    heightImg2 = 450
    widthImg2 = 450
    if heightImg2 > heightImg:
        x = heightImg
        y = int(x / 9)
        y = y * 9
        heightImg2 = y
        widthImg2 = y

    img = cv2.resize(img, (widthImg, heightImg))
    imgBlank = np.zeros((500, 500, 3), np.uint8)

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, 1, 1, 11, 2)
    #plt.imshow(cv2.cvtColor(imgThreshold, cv2.COLOR_BGR2RGB))
    #plt.show()

    contours, heirarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    imgContours = img.copy()
    imgBigContour = img.copy()
    cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 3)
    #plt.imshow(cv2.cvtColor(imgContours, cv2.COLOR_BGR2RGB))
    #plt.show()

    biggest = np.array([])
    max_area = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 50:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area
    #print(biggest)

    if biggest.size != 0:
        myPoints = biggest.reshape((4, 2))
        myPointsNew = np.zeros((4, 1, 2), dtype = np.int32)
        add = myPoints.sum(1)
        myPointsNew[0] = myPoints[np.argmin(add)]
        myPointsNew[3] = myPoints[np.argmax(add)]
        diff = np.diff(myPoints, axis = 1)
        myPointsNew[1] = myPoints[np.argmin(diff)]
        myPointsNew[2] = myPoints[np.argmax(diff)]
        biggest = myPointsNew

    cv2.drawContours(imgBigContour, biggest, -1, (0, 255, 0), 10)
    #plt.imshow(cv2.cvtColor(imgBigContour, cv2.COLOR_BGR2RGB))
    #plt.show()
    pts1 = np.float32(biggest)
    #print(pts1)
    pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
    imgWarpColored = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)
    #plt.imshow(cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2RGB))
    #plt.show()

    imgWarpColored = cv2.resize(imgWarpColored, (heightImg2, widthImg2))
    #plt.imshow(cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2RGB))
    #plt.show()

    #Border detection
    #Same algorithm as before
    #Biggest contour inside sudoku is border
    border_flag = 0
    imgBlur = cv2.GaussianBlur(imgWarpColored, (5, 5), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, 1, 1, 11, 2)

    contours2, heirarchy2 = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    imgContours = imgWarpColored.copy()
    imgBigContour = imgWarpColored.copy()
    cv2.drawContours(imgContours, contours2, -1, (0, 255, 0), 3)
    #plt.imshow(cv2.cvtColor(imgContours, cv2.COLOR_BGR2RGB))
    #plt.show()

    biggest = np.array([])
    max_area = 0
    for contour in contours2:
        area = cv2.contourArea(contour)
        x = heightImg2 * widthImg2
        y = int(x * 3 / 4)
        if area > y:
            #print(area)
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
            if area > max_area and len(approx) == 4:
                border_flag = 1
                biggest = approx
                max_area = area
    
    if biggest.size != 0:
        myPoints = biggest.reshape((4, 2))
        myPointsNew = np.zeros((4, 1, 2), dtype = np.int32)
        add = myPoints.sum(1)
        myPointsNew[0] = myPoints[np.argmin(add)]
        myPointsNew[3] = myPoints[np.argmax(add)]
        diff = np.diff(myPoints, axis = 1)
        myPointsNew[1] = myPoints[np.argmin(diff)]
        myPointsNew[2] = myPoints[np.argmax(diff)]
        biggest = myPointsNew

        cv2.drawContours(imgBigContour, biggest, -1, (0, 255, 0), 10)
        #plt.imshow(cv2.cvtColor(imgBigContour, cv2.COLOR_BGR2RGB))
        #plt.show()

        heightImg = imgWarpColored.shape[0]
        widthImg = imgWarpColored.shape[1]
        heightImg = max(heightImg, widthImg)
        widthImg = heightImg

        pts1 = np.float32(biggest)
        #print(pts1)
        pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        imgWarpColored2 = cv2.warpPerspective(imgWarpColored, matrix, (widthImg, heightImg))
        #imgWarpColored2 = cv2.cvtColor(imgWarpColored2, cv2.COLOR_BGR2GRAY)
        #plt.imshow(cv2.cvtColor(imgWarpColored2, cv2.COLOR_BGR2RGB))
        #plt.show()

        imgWarpColored2 = cv2.resize(imgWarpColored2, (heightImg2, widthImg2))
        #plt.imshow(cv2.cvtColor(imgWarpColored2, cv2.COLOR_BGR2RGB))
        #plt.show()

    print()
    if border_flag == 1:
        imgWarpColored = imgWarpColored2
        print("Border detected")
    else:
        print("Border not deteceted")
    #plt.imshow(cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2RGB))
    #plt.show()

    def splitBoxes(img):
        rows = np.vsplit(img,9)
        boxes=[]
        for r in rows:
            cols= np.hsplit(r,9)
            for box in cols:
                boxes.append(box)
        return boxes

    boxes = splitBoxes(imgWarpColored)

    question_sudoku = [[0 for i in range(9)] for k in range(9)]
    print("\nNumbers are being read...")
    for i in range(0, 81):
        img = boxes[i]
        img = cv2.medianBlur(img, 3)
        img = np.asarray(img)
        img = img[4:img.shape[0] - 4, 4:img.shape[1] -4]
        img = cv2.resize(img, (28, 28))
        img = img / 255
        img = img.reshape(1, 28, 28, 1)
        predictions = model.predict(img)
        classIndex = np.argmax(predictions, axis = -1)
        probabilityValue = np.amax(predictions)
        ans = classIndex[0]
        if probabilityValue <= 0.6:
            ans = 0
        row = int(i / 9)
        col = i % 9
        question_sudoku[row][col] = ans
        #print(i, ans, probabilityValue)

    print("Done\n")
    print("Please correct the entries, if there is any mistake in reading.")
    print("Then click on Solve\n")

    root = Tk()
    root.title("Sudoku Input Check")
    root.geometry("500x400")

    my_notebook = ttk.Notebook(root)
    my_notebook.pack(pady = 5)

    #creating frames
    input_f = Frame(my_notebook, width = 480, height = 380, bg = "#65CCB8")
    input_f.pack(fill = 'both', expand = 1)

    #adding frames
    my_notebook.add(input_f, text = 'Input Check')

    num = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]               #list of numbers as options
    click = StringVar()
    def select(event):                      #event loop responds if we click on particular num and takes that as event 
        mylab = Label(input_f, text = click.get())
        mylab.grid(row = 0, column = 0)
    
    click1 = copy.deepcopy(question_sudoku)

    #loop for storing values selected in dropdown box
    for i in range(9):
        for k in range(9):
            click1[i][k] = IntVar()
            click1[i][k].set(question_sudoku[i][k])

    drop = [[OptionMenu(input_f, click1[i][k], *num, command = select) for k in range(9)] for i in range(9)]

    for i in range(9):
        for k in range(9):
            drop[i][k].grid(row = i,column = k)
            box = 0
            if i <= 2 and k <= 2:
                box = 1
            elif i <= 2 and k <= 5:
                box = 2
            elif i <= 2 and k <= 8:
                box = 3
            elif i <= 5 and k <= 2:
                box = 4
            elif i <= 5 and k <= 5:
                box = 5
            elif i <= 5 and k <= 8:
                box = 6
            elif i <= 8 and k <= 2:
                box = 7
            elif i <= 8 and k <= 5:
                box = 8
            elif i <= 8 and k <= 8:
                box = 9
            if box == 2 or box == 4 or box == 6 or box == 8:
                drop[i][k].config(bg="red", fg="white")
            else:
                drop[i][k].config(bg="#EAE7DC", fg="black") 
        
    #setting the values in question sudoku
    def set_button():
        for i in range(9):
            for k in range(9):
                drop[i][k].configure(state = 'disabled', bg = "#D8C3A5", fg = "#E85A4F")

    #contains code to solve the sudoku
    def solve_sudoku():
        #set button is called
        set_button()
        #solving code
        for i in range(9):
            for k in range(9):
                question_sudoku[i][k] = int(click1[i][k].get())
        for i in range(9):
            for k in range(9):
                if question_sudoku[i][k] != 0:
                    Sudoku_object.sudoku[i][k][0] = question_sudoku[i][k]
                else:
                    for z in range(1, 10):
                        Sudoku_object.sudoku[i][k][z] = z 
                #print(question_sudoku[i][k], end = " ")
            #print()
        lets_quit()
        print("Solving Sudoku..\n")
        Sudoku_object.Solve()
        imgBlank.fill(255)
        acc1 = 5
        for k in range(1, 10):
            acc2 = 5
            for i in range(0, 9):
                st = str(Sudoku_object.sudoku[k-1][i][0])
                x = i * 50
                x = x + acc2
                y = k * 50
                y = y + acc1
                if Sudoku_object.sudoku[k-1][i][0] == 0:
                    st = " "
                if question_sudoku[k-1][i] == 0:
                    cv2.putText(imgBlank, st, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0))
                else:
                    cv2.putText(imgBlank, st, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0))
                acc2 = acc2 + 5
            acc1 = acc1 + 5
        cv2.line(imgBlank, (5, 170), (495, 170), (0, 0, 0), 1)
        cv2.line(imgBlank, (5, 335), (495, 335), (0, 0, 0), 1)
        cv2.line(imgBlank, (165, 5), (165, 495), (0, 0, 0), 1)
        cv2.line(imgBlank, (330, 5), (330, 495), (0, 0, 0), 1)
        #plt.imshow(cv2.cvtColor(imgBlank, cv2.COLOR_BGR2RGB))
        #plt.show()
        cv2.imshow("Sudoku_grid", imgBlank)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def lets_quit():
        root.destroy()

    b1 = Button(input_f, text = "Solve", command = solve_sudoku, bg = "black", fg = "white") #to solve question sudoku
    b1.grid(row = 12, column = 0, columnspan = 2)

    root.resizable(0,0)
    root.mainloop()