class Sudoku:
    def __init__(self):
        self.sudoku = [[[0 for i in range(10)] for k in range(9)] for z in range(9)]
        self.solve = False
        self.changes = 0
        self.freq_table = [[0 for i in range(9)] for k in range(9)]
        self.freq = [0 for i in range(81)]
        self.row = [0 for i in range(81)]
        self.column = [0 for i in range(81)]
        self.number_list = []
        self.unsolved = 0

    def Accept(self):
        for i in range(9):
            print("Enter Sudoku line", i+1)
            inp = str(input())
            acc = 0
            for k in inp:
                if k != ' ':
                    self.sudoku[i][acc][0] = int(k)
                acc = acc + 1
        for i in range(9):
            for k in range(9):
                if(self.sudoku[i][k][0] == 0):
                    for z in range(1, 10):
                        self.sudoku[i][k][z] = z

    def Display(self):
        for i in range(9):
            for k in range(9):
                if k <= 7:
                    if self.sudoku[i][k][0] != 0:
                        print("", self.sudoku[i][k][0], "|", end = "")
                    else:
                        print("   |", end = "")
                elif k == 8:
                    if self.sudoku[i][k][0] != 0:
                        print("", self.sudoku[i][k][0], " ", end = "")
                    else:
                        print("   ", end = "")
            print()
            if i <= 7:
                for k in range(9):
                    if(k <= 7):
                        print("___|", end = "")
                    else:
                        print("___", end = "")
            else:
                for k in range(9):
                    if k <= 7:
                        print("   |", end = "")
                    else:
                        print("   ", end = "")
            print()

    def Check(self):
        flag = True
        f = False
        for i in range(9):
            for k in range(9):
                if(self.sudoku[i][k][0] == 0):
                    flag = False
                    f = True
                    break
            if f == True:
                break
        self.solve = flag

    def Primitive_Elimination(self):
        #S = self
        for i in range(9):
            for k in range(9):
                if self.sudoku[i][k][0] != 0:
                    self.PEliminate(self.sudoku[i][k][0], i, k)
                    #for i in range(9):
                     #   for k in range(9):
                      #      print("(", i, ",", k, ")", end = " ")
                       #     for z in range(1, 10):
                        #        print(self.sudoku[i][k][z], ",", end = " ")
                         #   print()

    def PEliminate(self, n, r, c):
        #Row elimination:-
        for i in range(9):
            if self.sudoku[r][i][0] == 0:
                self.sudoku[r][i][n] = 0
        #Column elimination:-
        for i in range(9):
            if self.sudoku[i][c][0] == 0:
                self.sudoku[i][c][n] = 0
        #Box elimination
        if r >= 0 and r <= 2 and c >= 0 and c <= 2:
            for i in range(3):
                for k in range(3):
                    if self.sudoku[i][k][0] == 0:
                        self.sudoku[i][k][n] = 0
        elif r >= 0 and r <= 2 and c >= 3 and c <= 5:
            for i in range(3):
                for k in range(3, 6):
                    if self.sudoku[i][k][0] == 0:
                        self.sudoku[i][k][n] = 0
        elif r >= 0 and r <= 2 and c >= 6 and c <= 8:
            for i in range(3):
                for k in range(6, 9):
                    if self.sudoku[i][k][0] == 0:
                        self.sudoku[i][k][n] = 0
        elif r >= 3 and r <= 5 and c >= 0 and c <= 2:
            for i in range(3, 6):
                for k in range(3):
                    if self.sudoku[i][k][0] == 0:
                        self.sudoku[i][k][n] = 0
        elif r >= 3 and r <= 5 and c >= 3 and c <= 5:
            for i in range(3, 6):
                for k in range(3, 6):
                    if self.sudoku[i][k][0] == 0:
                        self.sudoku[i][k][n] = 0
        elif r >= 3 and r <= 5 and c >= 6 and c <= 8:
            for i in range(3, 6):
                for k in range(6, 9):
                    if self.sudoku[i][k][0] == 0:
                        self.sudoku[i][k][n] = 0
        elif r >= 6 and r <= 8 and c >= 0 and c <= 2:
            for i in range(6, 9):
                for k in range(3):
                    if self.sudoku[i][k][0] == 0:
                        self.sudoku[i][k][n] = 0
        elif r >= 6 and r <= 8 and c >= 2 and c <= 5:
            for i in range(6, 9):
                for k in range(3, 6):
                    if self.sudoku[i][k][0] == 0:
                        self.sudoku[i][k][n] = 0
        elif r >=6 and r <= 8 and c>= 6 and c <= 8:
            for i in range(6, 9):
                for k in range(6, 9):
                    if self.sudoku[i][k][0] == 0:
                        self.sudoku[i][k][n] = 0

    def Primitive_Fill(self):
        #S = self
        self.P1Fill()
        self.PRFill()
        self.PCFill()
        self.PBFill()

    def Fill_Protocol(self, n, r, c):
        #S = self
        self.changes+=1
        #print("Filling", n, "at", "(", r, ",", c, ")")
        for i in range(1, 10):
            self.sudoku[r][c][i] = 0

    def P1Fill(self):
        #S = self
        for i in range(9):
            for k in range(9):
                if self.sudoku[i][k][0] != 0:
                    continue
                else:
                    freq = 0
                    for z in range(1, 10):
                        if self.sudoku[i][k][z] == z:
                            freq+=1
                    if freq == 1:
                        for z in range(1, 10):
                            if self.sudoku[i][k][z] == z:
                                self.sudoku[i][k][0] = z
                                #print("Single frequency fill")
                                self.Fill_Protocol(z, i, k)
                                self.Primitive_Elimination()
                                break
                    
    def PRFill(self):
        #S = self
        freq = 0
        for i in range(9):
            for k in range(1, 10):
                freq = 0
                for z in range(9):
                    if self.sudoku[i][z][0] == 0 and self.sudoku[i][z][k] == k:
                        freq = freq + 1
                if freq == 1:
                    for z in range(9):
                        if self.sudoku[i][z][0] == 0 and self.sudoku[i][z][k] == k:
                            self.sudoku[i][z][0] = k
                            #print("Row fill")
                            self.Fill_Protocol(k, i, z)
                            self.Primitive_Elimination()
                            break

    def PCFill(self):
        #S = self
        freq = 0
        for i in range(9):
            for k in range(1, 10):
                freq = 0
                for z in range(9):
                    if self.sudoku[z][i][0] == 0 and self.sudoku[z][i][k] == k:
                        freq = freq + 1
                if freq == 1:
                    for z in range(9):
                        if self.sudoku[z][i][0] == 0 and self.sudoku[z][i][k] == k:
                            self.sudoku[z][i][0] = k
                            #print("Column fill")
                            self.Fill_Protocol(k, z, i)
                            self.Primitive_Elimination()
                            break

    def PBFill(self):
        #S = self
        freq = 0
        #box 1
        for z in range(1, 10):
            freq = 0
            for i in range(3):
                for k in range(3):
                    if self.sudoku[i][k][0] == 0 and self.sudoku[i][k][z] == z:
                        freq = freq + 1
            if freq == 1:
                flag = False
                for i in range(3):
                    for k in range(3):
                        if self.sudoku[i][k][0] == 0 and self.sudoku[i][k][z] == z:
                            self.sudoku[i][k][0] = z
                            #print("Box fill")
                            self.Fill_Protocol(z, i, k)
                            self.Primitive_Elimination()
                            flag = True
                            break
                    if flag == True:
                        break
        #box 2
        for z in range(1, 10):
            freq = 0
            for i in range(3):
                for k in range(3, 6):
                    if self.sudoku[i][k][0] == 0 and self.sudoku[i][k][z] == z:
                        freq = freq + 1
            if freq == 1:
                flag = False
                for i in range(3):
                    for k in range(3, 6):
                        if self.sudoku[i][k][0] == 0 and self.sudoku[i][k][z] == z:
                            self.sudoku[i][k][0] = z
                            #print("Box fill")
                            self.Fill_Protocol(z, i, k)
                            self.Primitive_Elimination()
                            flag = True
                            break
                    if flag == True:
                        break
        #box 3
        for z in range(1, 10):
            freq = 0
            for i in range(3):
                for k in range(6, 9):
                    if self.sudoku[i][k][0] == 0 and self.sudoku[i][k][z] == z:
                        freq = freq + 1
            if freq == 1:      
                flag = False
                for i in range(3):
                    for k in range(6, 9):
                        if self.sudoku[i][k][0] == 0 and self.sudoku[i][k][z] == z:
                            self.sudoku[i][k][0] = z
                            #print("Box fill")
                            self.Fill_Protocol(z, i, k)
                            self.Primitive_Elimination()
                            flag = True
                            break
                    if flag == True:
                        break
        #box 4
        for z in range(1, 10):
            freq = 0
            for i in range(3, 6):
                for k in range(3):
                    if self.sudoku[i][k][0] == 0 and self.sudoku[i][k][z] == z:
                        freq = freq + 1
            if freq == 1:
                flag = False
                for i in range(3, 6):
                    for k in range(3):
                        if self.sudoku[i][k][0] == 0 and self.sudoku[i][k][z] == z:
                            self.sudoku[i][k][0] = z
                            #print("Box fill")
                            self.Fill_Protocol(z, i, k)
                            self.Primitive_Elimination()
                            flag = True
                            break
                    if flag == True:
                        break
        #box 5
        for z in range(1, 10):
            freq = 0
            for i in range(3, 6):
                for k in range(3, 6):
                    if self.sudoku[i][k][0] == 0 and self.sudoku[i][k][z] == z:
                        freq = freq + 1
            if freq == 1:      
                flag = False
                for i in range(3, 6):
                    for k in range(3, 6):
                        if self.sudoku[i][k][0] == 0 and self.sudoku[i][k][z] == z:
                            self.sudoku[i][k][0] = z
                            #print("Box fill")
                            self.Fill_Protocol(z, i, k)
                            self.Primitive_Elimination()
                            flag = True
                            break
                    if flag == True:
                        break
        #box 6
        for z in range(1, 10):
            freq = 0
            for i in range(3, 6):
                for k in range(6, 9):
                    if self.sudoku[i][k][0] == 0 and self.sudoku[i][k][z] == z:
                        freq = freq + 1
            if freq == 1:
                flag = False
                for i in range(3, 6):
                    for k in range(6, 9):
                        if self.sudoku[i][k][0] == 0 and self.sudoku[i][k][z] == z:
                            self.sudoku[i][k][0] = z
                            #print("Box fill")
                            self.Fill_Protocol(z, i, k)
                            self.Primitive_Elimination()
                            flag = True
                            break
                    if flag == True:
                        break
        #box 7
        for z in range(1, 10):
            freq = 0
            for i in range(6, 9):
                for k in range(3):
                    if self.sudoku[i][k][0] == 0 and self.sudoku[i][k][z] == z:
                        freq = freq + 1
            if freq == 1:
                flag = False
                for i in range(6, 9):
                    for k in range(3):
                        if self.sudoku[i][k][0] == 0 and self.sudoku[i][k][z] == z:
                            self.sudoku[i][k][0] = z
                            #print("Box fill")
                            self.Fill_Protocol(z, i, k)
                            self.Primitive_Elimination()
                            flag = True
                            break
                    if flag == True:
                        break
        #box 8
        for z in range(1, 10):
            freq = 0
            for i in range(6, 9):
                for k in range(3, 6):
                    if self.sudoku[i][k][0] == 0 and self.sudoku[i][k][z] == z:
                        freq = freq + 1
            if freq == 1:
                flag = False
                for i in range(6, 9):
                    for k in range(3, 6):
                        if self.sudoku[i][k][0] == 0 and self.sudoku[i][k][z] == z:
                            self.sudoku[i][k][0] = z
                            #print("Box fill")
                            self.Fill_Protocol(z, i, k)
                            self.Primitive_Elimination()
                            flag = True
                            break
                    if flag == True:
                        break
        #box 9
        for z in range(1, 10):
            freq = 0
            for i in range(6, 9):
                for k in range(6, 9):
                    if self.sudoku[i][k][0] == 0 and self.sudoku[i][k][z] == z:
                        freq = freq + 1
            if freq == 1:
                flag = False
                for i in range(6, 9):
                    for k in range(6, 9):
                        if self.sudoku[i][k][0] == 0 and self.sudoku[i][k][z] == z:
                            self.sudoku[i][k][0] = z
                            #print("Box fill")
                            self.Fill_Protocol(z, i, k)
                            self.Primitive_Elimination()
                            flag = True
                            break
                    if flag == True:
                        break

    def Valid_Sudoku(self):
        flag = True
        for i in range(1, 10):
            #row check
            for k in range(9):
                freq = 0
                for z in range(9):
                    if self.sudoku[k][z][0] == i:
                        freq+=1
                if freq > 1:
                    flag = False
                    return flag
            #column check
            for k in range(9):
                freq = 0
                for z in range(9):
                    if self.sudoku[z][k][0] == i:
                        freq+=1
                if freq > 1:
                    flag = False
                    return flag
            #box check
            #box 1
            freq = 0
            for k in range(3):
                for z in range(3):
                    if self.sudoku[k][z][0] == i:
                        freq+=1
                if freq > 1:
                    flag = False
                    return flag
            #box 2
            freq = 0
            for k in range(3):
                for z in range(3, 6):
                    if self.sudoku[k][z][0] == i:
                        freq+=1
                if freq > 1:
                    flag = False
                    return flag
            #box 3
            freq = 0
            for k in range(3):
                for z in range(6, 9):
                    if self.sudoku[k][z][0] == i:
                        freq+=1
                if freq > 1:
                    flag = False
                    return flag
            #box 4
            freq = 0
            for k in range(3, 6):
                for z in range(3):
                    if self.sudoku[k][z][0] == i:
                        freq+=1
                if freq > 1:
                    flag = False
                    return flag
            #box 5
            freq = 0
            for k in range(3, 6):
                for z in range(3, 6):
                    if self.sudoku[k][z][0] == i:
                        freq+=1
                if freq > 1:
                    flag = False
                    return flag
            #box 6
            freq = 0
            for k in range(3, 6):
                for z in range(6, 9):
                    if self.sudoku[k][z][0] == i:
                        freq+=1
                if freq > 1:
                    flag = False
                    return flag
            #box 7
            freq = 0
            for k in range(6, 9):
                for z in range(3):
                    if self.sudoku[k][z][0] == i:
                        freq+=1
                if freq > 1:
                    flag = False
                    return flag
            #box 8
            freq = 0
            for k in range(6, 9):
                for z in range(3, 6):
                    if self.sudoku[k][z][0] == i:
                        freq+=1
                if freq > 1:
                    flag = False
                    return flag
            #box 9
            freq = 0
            for k in range(6, 9):
                for z in range(6, 9):
                    if self.sudoku[k][z][0] == i:
                        freq+=1
                if freq > 1:
                    flag = False
                    return flag
        return flag

    def Advanced_Step1(self):
        count = 0
        for i in range(9):
            for k in range(9):
                count = 0
                if self.sudoku[i][k][0] == 0:
                    for z in range(1, 10):
                        if self.sudoku[i][k][z] != 0:
                            count+=1
                if count != 0:
                    self.freq_table[i][k] = count
                else:
                    self.freq_table[i][k] = 10
        acc = 0
        for i in range(9):
            for k in range(9):
                self.freq[acc] = self.freq_table[i][k]
                self.row[acc] = i
                self.column[acc] = k
                acc+=1
        for i in range(80):
            for k in range(80-i):
                if self.freq[k] > self.freq[k+1]:
                    swap = self.freq[k]
                    self.freq[k] = self.freq[k+1]
                    self.freq[k+1] = swap
                    swap = self.row[k]
                    self.row[k] = self.row[k+1]
                    self.row[k+1] = swap
                    swap = self.column[k]
                    self.column[k] = self.column[k+1]
                    self.column[k+1] = swap
        for i in range(9):
            for k in range(9):
                if self.sudoku[i][k][0] == 0:
                    self.unsolved+=1
        for i in range(30):
            buff = []
            r = self.row[i]
            c = self.column[i]
            for z in range(1, 10):
                if self.sudoku[r][c][z] != 0:
                    buff.append(z)
            self.number_list.append(buff)

    def Antifill(self, n):
        for i in range(n, 15):
            if self.sudoku[self.row[i]][self.column[i]][0] != 0:
                for z in range(10):
                    self.sudoku[self.row[i]][self.column[i]][z] = self.sudoku3[self.row[i]][self.column[i]][z]

    def Advanced(self):
        #S = self
        self.Advanced_Step1()
        print("unsolved boxes =", self.unsolved)
        if self.unsolved <= 10:
            #lets make 5 guesses
            print("Advanced solving done, 5 assumptions taken")
            sudoku2 = [[[0 for i in range(10)] for k in range(9)] for z in range(9)]
            for i in range(9):
                for k in range(9):
                    for z in range(10):
                        sudoku2[i][k][z] = self.sudoku[i][k][z]
            for a in self.number_list[0]:
                for b in self.number_list[1]:
                    for c in self.number_list[2]:
                        for d in self.number_list[3]:
                            for e in self.number_list[4]:
                                self.sudoku[self.row[0]][self.column[0]][0] = a
                                self.sudoku[self.row[1]][self.column[1]][0] = b
                                self.sudoku[self.row[2]][self.column[2]][0] = c
                                self.sudoku[self.row[3]][self.column[3]][0] = d
                                self.sudoku[self.row[4]][self.column[4]][0] = e
                                self.Fill_Protocol(a, self.row[0], self.column[0])
                                self.Fill_Protocol(b, self.row[1], self.column[1])
                                self.Fill_Protocol(c, self.row[2], self.column[2])
                                self.Fill_Protocol(d, self.row[3], self.column[3])
                                self.Fill_Protocol(e, self.row[4], self.column[4])
                                flag = self.Valid_Sudoku()
                                if flag == False:
                                    for i in range(9):
                                        for k in range(9):
                                            for z in range(10):
                                                self.sudoku[i][k][z] = sudoku2[i][k][z]
                                    continue
                                else:
                                    self.Primitive_Elimination()
                                    while(True):
                                        self.changes = 0
                                        self.Primitive_Fill()
                                        if self.changes == 0:
                                            self.Primitive_Fill()
                                            if self.changes == 0:
                                                self.Check()
                                                break
                                    if self.solve == True:
                                        self.Display()
                                        print("Sudoku Solved!!")
                                        return ""
                                    else:
                                        for i in range(9):
                                            for k in range(9):
                                                for z in range(10):
                                                    self.sudoku[i][k][z] = sudoku2[i][k][z]
        elif self.unsolved <= 20 and self.solve == False:
        #lets make 10 guesses
            print("Advanced solving done, 10 assumptions taken")
            sudoku2 = [[[0 for i in range(10)] for k in range(9)] for z in range(9)]
            for i in range(9):
                for k in range(9):
                    for z in range(10):
                        sudoku2[i][k][z] = self.sudoku[i][k][z]
            for a in self.number_list[0]:
                for b in self.number_list[1]:
                    for c in self.number_list[2]:
                        for d in self.number_list[3]:
                            for e in self.number_list[4]:
                                for f in self.number_list[5]:
                                    for g in self.number_list[6]:
                                        for h in self.number_list[7]:
                                            for i in self.number_list[8]:
                                                for j in self.number_list[9]:
                                                    self.sudoku[self.row[0]][self.column[0]][0] = a
                                                    self.sudoku[self.row[1]][self.column[1]][0] = b
                                                    self.sudoku[self.row[2]][self.column[2]][0] = c
                                                    self.sudoku[self.row[3]][self.column[3]][0] = d
                                                    self.sudoku[self.row[4]][self.column[4]][0] = e
                                                    self.sudoku[self.row[5]][self.column[5]][0] = f
                                                    self.sudoku[self.row[6]][self.column[6]][0] = g
                                                    self.sudoku[self.row[7]][self.column[7]][0] = h
                                                    self.sudoku[self.row[8]][self.column[8]][0] = i
                                                    self.sudoku[self.row[9]][self.column[9]][0] = j
                                                    self.Fill_Protocol(a, self.row[0], self.column[0])
                                                    self.Fill_Protocol(b, self.row[1], self.column[1])
                                                    self.Fill_Protocol(c, self.row[2], self.column[2])
                                                    self.Fill_Protocol(d, self.row[3], self.column[3])
                                                    self.Fill_Protocol(e, self.row[4], self.column[4])
                                                    self.Fill_Protocol(f, self.row[5], self.column[5])
                                                    self.Fill_Protocol(g, self.row[6], self.column[6])
                                                    self.Fill_Protocol(h, self.row[7], self.column[7])
                                                    self.Fill_Protocol(i, self.row[8], self.column[8])
                                                    self.Fill_Protocol(j, self.row[9], self.column[9])
                                                    flag = self.Valid_Sudoku()
                                                    if flag == False:
                                                        for i in range(9):
                                                            for k in range(9):
                                                                for z in range(10):
                                                                    self.sudoku[i][k][z] = sudoku2[i][k][z]
                                                        continue
                                                    else:
                                                        self.Primitive_Elimination()
                                                        while(True):
                                                            self.changes = 0
                                                            self.Primitive_Fill()
                                                            if self.changes == 0:
                                                                self.Primitive_Fill()
                                                                if self.changes == 0:
                                                                    self.Check()
                                                                    break
                                                        if self.solve == True:
                                                            self.Display()
                                                            print("Sudoku Solved!!")
                                                            return ""
                                                        else:
                                                            for i in range(9):
                                                                for k in range(9):
                                                                    for z in range(10):
                                                                        self.sudoku[i][k][z] = sudoku2[i][k][z]
        elif self.unsolved <= 65 and self.solve == False:
        #lets make 15 guesses
            acc = 1
            print("Advanced solving done, 15 assumptions taken")
            sudoku2 = [[[0 for i in range(10)] for k in range(9)] for z in range(9)]
            self.sudoku3 = [[[0 for i in range(10)] for k in range(9)] for z in range(9)]
            for i in range(9):
                for k in range(9):
                    for z in range(10):
                        self.sudoku3[i][k][z] = self.sudoku[i][k][z]
                        sudoku2[i][k][z] = self.sudoku[i][k][z]
            for a in self.number_list[0]:
                for i in range(9):
                    for k in range(9):
                        for z in range(10):
                            self.sudoku[i][k][z] = sudoku2[i][k][z]
                self.sudoku[self.row[0]][self.column[0]][0] = a
                self.Fill_Protocol(a, self.row[0], self.column[0])
                for b in self.number_list[1]:
                    self.Antifill(2)
                    self.sudoku[self.row[1]][self.column[1]][0] = b
                    self.Fill_Protocol(b, self.row[1], self.column[1])
                    if self.Valid_Sudoku() == False:
                        continue
                    for c in self.number_list[2]:
                        self.Antifill(3)
                        self.sudoku[self.row[2]][self.column[2]][0] = c
                        self.Fill_Protocol(c, self.row[2], self.column[2])
                        if self.Valid_Sudoku() == False:
                            continue
                        for d in self.number_list[3]:
                            self.Antifill(4)
                            self.sudoku[self.row[3]][self.column[3]][0] = d
                            self.Fill_Protocol(d, self.row[3], self.column[3])
                            if self.Valid_Sudoku() == False:
                                continue
                            for e in self.number_list[4]:
                                self.Antifill(5)
                                self.sudoku[self.row[4]][self.column[4]][0] = e
                                self.Fill_Protocol(e, self.row[4], self.column[4])
                                if self.Valid_Sudoku() == False:
                                    continue
                                for f in self.number_list[5]:
                                    self.Antifill(6)
                                    self.sudoku[self.row[5]][self.column[5]][0] = f
                                    self.Fill_Protocol(f, self.row[5], self.column[5])
                                    if self.Valid_Sudoku() == False:
                                        continue
                                    for g in self.number_list[6]:
                                        self.Antifill(7)
                                        self.sudoku[self.row[6]][self.column[6]][0] = g
                                        self.Fill_Protocol(g, self.row[6], self.column[6])
                                        if self.Valid_Sudoku() == False:
                                            continue
                                        for h in self.number_list[7]:
                                            self.Antifill(8)
                                            self.sudoku[self.row[7]][self.column[7]][0] = h
                                            self.Fill_Protocol(h, self.row[7], self.column[7])
                                            if self.Valid_Sudoku() == False:                  
                                                continue
                                            for i in self.number_list[8]:
                                                self.Antifill(9)
                                                self.sudoku[self.row[8]][self.column[8]][0] = i
                                                self.Fill_Protocol(i, self.row[8], self.column[8])  
                                                if self.Valid_Sudoku() == False:                                                    
                                                    continue
                                                for j in self.number_list[9]:
                                                    self.Antifill(10)
                                                    self.sudoku[self.row[9]][self.column[9]][0] = j
                                                    self.Fill_Protocol(j, self.row[9], self.column[9])
                                                    if self.Valid_Sudoku() == False:
                                                        continue
                                                    for k in self.number_list[10]:
                                                        self.Antifill(11)
                                                        self.sudoku[self.row[10]][self.column[10]][0] = k
                                                        self.Fill_Protocol(k, self.row[10], self.column[10])
                                                        if self.Valid_Sudoku() == False:
                                                            continue
                                                        for l in self.number_list[11]:
                                                            self.Antifill(12)
                                                            self.sudoku[self.row[11]][self.column[11]][0] = l
                                                            self.Fill_Protocol(l, self.row[11], self.column[11])
                                                            if self.Valid_Sudoku() == False:
                                                                continue
                                                            for m in self.number_list[12]:
                                                                self.Antifill(13)
                                                                self.sudoku[self.row[12]][self.column[12]][0] = m
                                                                self.Fill_Protocol(m, self.row[12], self.column[12])
                                                                if self.Valid_Sudoku() == False:
                                                                    continue
                                                                for n in self.number_list[13]:
                                                                    self.Antifill(14)
                                                                    self.sudoku[self.row[13]][self.column[13]][0] = n
                                                                    self.Fill_Protocol(n, self.row[13], self.column[13])
                                                                    if self.Valid_Sudoku() == False:
                                                                        continue
                                                                    for o in self.number_list[14]:
                                                                        self.sudoku[self.row[14]][self.column[14]][0] = o
                                                                        self.Fill_Protocol(o, self.row[14], self.column[14])
                                                                        flag = self.Valid_Sudoku()
                                                                        if flag == False:
                                                                            continue
                                                                        else:
                                                                            acc+=1
                                                                            inter = [[[0 for i in range(10)] for k in range(9)] for z in range(9)]
                                                                            for i in range(9):
                                                                                for k in range(9):
                                                                                    for z in range(10):
                                                                                        inter[i][k][z] = self.sudoku[i][k][z]
                                                                            self.Primitive_Elimination()
                                                                            while(True):
                                                                                self.changes = 0
                                                                                self.Primitive_Fill()
                                                                                if self.changes == 0:
                                                                                    self.Primitive_Fill()
                                                                                    if self.changes == 0:
                                                                                        self.Check()
                                                                                        break
                                                                            if self.solve == True:
                                                                                self.Display()
                                                                                print("Sudoku Solved!!")
                                                                                return ""
                                                                            else:
                                                                                #print(acc, "Assumption incorrect")
                                                                                acc+=1
                                                                                for i in range(9):
                                                                                    for k in range(9):
                                                                                        for z in range(10):
                                                                                            self.sudoku[i][k][z] = inter[i][k][z]
        else:
            print("Too many blank entries, cannot solve.")
              
    def Solve(self):
        #S = self
        #self.Accept()
        #self.Display()
        #print("Does your Sudoku matrix look like this? Enter 1 if yes, 0 otherwise")
        #a = int(input())
        is_Valid = self.Valid_Sudoku()
        if is_Valid == True:
            self.Primitive_Elimination()
            while(True):
                self.changes = 0
                self.Primitive_Fill()
                if self.changes == 0:
                    self.Primitive_Fill()
                    if self.changes == 0:
                        self.Check()
                        break
            print("Primitive solving done")
            #self.Display()
            if self.solve == True:
                self.Display()
                print("Sudoku Solved!!")
            else:
                self.Advanced()
        else:
            print("Incorrect Sudoku")
        if self.solve == False:
            print("Couldnt solve sudoku")
            print("Maybe input was incorrect, try again.")
