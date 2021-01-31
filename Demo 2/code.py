import tkinter as tk #gui library
from selenium import webdriver  #for web scrapping
from selenium.webdriver.common.keys import Keys
import time
from time import gmtime, strftime
from datetime import datetime, timedelta
from findWords import possible_answers
from fillWords import fillWords, fillSolution

"""
This program creates a mini crossword puzzle similar to the one at www.nytimes.com/crosswords/game/mini.
It extracts the puzzle data from the same websites. It uses the Selenium library in order to extract
relevant infomration from the website. Furthermore, the Tkinter framework is used to build the gui
components. After that it tries to solve the puzzle. It extracts some key words like synonyms, antonyms
and other related words from the clues given from APIs. It uses those to generate matching words.


@authors:   Umer Shamaan
            Taha Khurram
            Hassan Raza Warraich
            Muhammad Ali Khaqan
"""



cellSize = 75  #default size of a grid cell


clueList = []  #store the clues and their information

num_arr = [[0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]]


letter_arr = [['!', '!', '!', '!', '!'],
            ['!', '!', '!', '!', '!'],
            ['!', '!', '!', '!', '!'],
            ['!', '!', '!', '!', '!'],
            ['!', '!', '!', '!', '!']]

to_be_solved_arr = [['!', '!', '!', '!', '!'],
            ['!', '!', '!', '!', '!'],
            ['!', '!', '!', '!', '!'],
            ['!', '!', '!', '!', '!'],
            ['!', '!', '!', '!', '!']]


final_sol_arr = [['!', '!', '!', '!', '!'],
            ['!', '!', '!', '!', '!'],
            ['!', '!', '!', '!', '!'],
            ['!', '!', '!', '!', '!'],
            ['!', '!', '!', '!', '!']]


def createGrid(grid):
    wid = 0
    while wid < (5 * cellSize)+1:
        lent = 0
        while lent < (5 * cellSize)+1:
            grid.create_rectangle(wid, lent, cellSize, cellSize, outline = 'grey')
            lent = lent + cellSize
        wid = wid + cellSize
    return


#to fill the wordless blocks
def fillGrey(grid, i, j):
    grid.create_rectangle(i * cellSize, j * cellSize, i * cellSize + cellSize, j * cellSize + cellSize, fill='grey')
    return


# filling grid cells with the solution letters 
lSize = 50 #the size of the letter
def fillWord(grid, lent, wid, letter):
    x = cellSize * wid + 38
    y = cellSize * lent + 43
    wid=grid.create_text(x, y, text=letter, font=("Arial", lSize))
    r=grid.create_rectangle(wid * cellSize, lent * cellSize, wid * cellSize + cellSize, lent * cellSize + cellSize,  fill="green")
    grid.tag_lower(r,wid)
    return


# Printing the clues for accross
tWidth = 350 #max width of text section
def across():
    clues.create_text(120,50, font=('Times',36),text='Across')
    size = 0
    for i in acrossClues:
        clues.create_text(50, 120 + size,font=('Times',14), anchor='w', text= i + ": " + acrossClues[i], width=tWidth)
        #clues.create_text(50, 120 + size,font=('Times',14), anchor='w', text= i + ": " + str(acrossClues[i]), width=tWidth)
        size = size + 36
    return


#filling grid numbers
nSize = 15
def markN(grid, lent, wid, num):
    x = cellSize * wid + 10
    y = cellSize * lent + 12
    grid.create_text(x, y, font=("Times", nSize), text = num)
    return


# Printing the clues for down
def down():
    #clues.create_text(450,50,font=('Times',36),text='Down')
    clues.create_text(500,50,font=('Times',36),text='Down')
    size = 0
    for i in downClues:
        clues.create_text(450, 120 + size,font=('Times',14), anchor='w', text= i + ": " + downClues[i], width=tWidth)
        size = size+36
    return


print("opening Firefox browser to extract the crossword")
# obtaining data from newyork times puzzle throught webscrapping
driver = webdriver.Firefox() #open firefox browser
#driver.minimize_window()
driver.set_page_load_timeout(50)                                         
driver.get("https://www.nytimes.com/crosswords/game/mini")                  # navigate to website
driver.find_element_by_xpath("//button[@aria-label='OK']").send_keys(Keys.ENTER)        # press enter
driver.find_element_by_xpath("//button[@aria-label='reveal']").click()              # click on the reveal link
driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/main/div[2]/div/div/ul/div[2]/li[2]/ul/li[3]/a').click()     #click reveal
driver.find_element_by_xpath("//button[@aria-label='Reveal']").send_keys(Keys.ENTER)         #press enter to exit popup
driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/span").send_keys(Keys.ENTER)    #press enter to exit popup
#driver.find_element_by_css_selector('minimodal-congrats-message').send_keys(Keys.ENTER)
#CongratsModal-subscriptionUpsell--2tbB2
element = driver.find_element_by_xpath("/html/body")          #extract the body tag from html
time.sleep(1)                   
content = element.get_attribute("innerHTML")     #put the extracted html data to variable
time.sleep(1)                   
driver.quit()       #exit browser     



# creating the window
window = tk.Tk()
window.configure(background = 'white')
window.title("New York Times Mini Crossword Puzzle by Joel Fagliano") 
window.geometry("1800x900") #setting window size

# creating puzzle and answer grid
grid = tk.Canvas(window,width=cellSize * 5,height=cellSize * 5, bg='white')
grid.place(x=50,y=50)
#createGrid()
createGrid(grid)


ans_grid = tk.Canvas(window,width=cellSize * 5,height=cellSize * 5, bg='white')
ans_grid.place(x=1410,y=50)
#createGrid()
createGrid(ans_grid)





######################################################################################
#printing number labels of cells to main grid
temp = 0
i = 0
j = 0
while temp < 25:
    indexLetter = 'id="cell-id-' + str(temp) 
    indexLetter = indexLetter + '"'
    si = len(indexLetter)
    letter = content[content.find(indexLetter) + (si + 8):content.find(indexLetter) + (si + 18)]

    if letter == 'Cell-block':
        lent = int(temp / 5)
        wid = temp % 5
        fillGrey(grid, wid, lent)                 
        #temp=temp+1
        num_arr[i][j] = -1
        #continue

    else:
        indexStart = content.find('text-anchor="start"', content.find(indexLetter), content.find('text-anchor="middle"', content.find(indexLetter)))
        if indexStart != (-1):
            markN(grid, int(temp / 5), (temp % 5), content[content.find("</text>", indexStart) + 7])
            #num_arr[i][j] = content[content.find("</text>", indexStart) + 7] ###############################################################
            num_arr[i][j] = int(content[content.find("</text>", indexStart) + 7])

    temp+=1
    j+=1
    if(j >4):
        j = 0
        i+=1



##############################################################################################

######################################################################################
#printing number labels of cells to solution grid
temp = 0
while temp < 25:
    indexLetter = 'id="cell-id-' + str(temp) 
    indexLetter = indexLetter + '"'
    si = len(indexLetter)
    letter = content[content.find(indexLetter) + (si + 8):content.find(indexLetter) + (si + 18)]

    if letter == 'Cell-block':
        lent = int(temp / 5)
        wid = temp % 5
        fillGrey(ans_grid, wid, lent)                 
        #temp=temp+1
        #continue

    else:
        indexStart = content.find('text-anchor="start"', content.find(indexLetter), content.find('text-anchor="middle"', content.find(indexLetter)))
        if indexStart != (-1):
            markN(ans_grid, int(temp / 5), (temp % 5), content[content.find("</text>", indexStart) + 7])

    temp+=1

##############################################################################################


print("extracting across clues")
# create clues
clues = tk.Canvas(window,height = 400,width=800, bg='white')               
#clues.place(x=600,y=40)
clues.place(x=520,y=50)
downClues = dict()
acrossClues = dict()


index = content.find("</span>", content.find("Across"))
initial = 0
fina = 5
while initial < fina:
    initial =initial+1
    end = content.find("<", content.find(">", index + 8))
    acrossClues[content[index-1]] = content[(content.find(">", index + 8))+1:end]  #########################################################
    #acrossClues[int(content[index-1])] = content[(content.find(">", index + 8))+1:end]
    
    #clue = dict(pos = content[index-1], content = content[(content.find(">", index + 8))+1:end], length = 0)
    #cluseList.append(clue)

    index = content.find("</span>", end + 10)

print(acrossClues)
across()              


print("extracting down clues")
index = content.find("</span>", content.find("Down", end))
initial = 0
while initial < fina:
    initial =initial+1
    end = content.find("<", content.find(">", index + 8))
    downClues[content[index-1]] = content[(content.find(">", index + 8))+1:end] #########################################################
    #downClues[int(content[index-1])] = content[(content.find(">", index + 8))+1:end]

    #clue = dict(pos = content[index-1], content = content[(content.find(">", index + 8))+1:end], length = 0)
    #cluseList.append(clue)

    index = content.find("</span>", end + 10)

print(downClues)
down()


print("extracting solution letters from the grid")
#filling the main grid with the solution letters
temp = 0
i = 0
j = 0
while temp < 25:
    indexLetter = 'id="cell-id-' + str(temp) 
    indexLetter = indexLetter + '"'
    si = len(indexLetter)
    letter = content[content.find(indexLetter) + (si + 8):content.find(indexLetter) + (si + 18)]


    if letter == 'Cell-block':
        lent = int(temp / 5)
        wid = temp % 5
        fillGrey(grid, wid, lent)                 
        #temp=temp+1
        #continue

    else:
        indexStart = content.find('text-anchor="start"', content.find(indexLetter), content.find('text-anchor="middle"', content.find(indexLetter)))
        if indexStart != (-1):
            markN(grid, int(temp / 5), (temp % 5), content[content.find("</text>", indexStart) + 7])
        fillWord(grid, int(temp / 5), (temp % 5), content[content.find('</text>',content.find('text-anchor="middle"', content.find(indexLetter)))-1])
        letter_arr[i][j] = content[content.find('</text>',content.find('text-anchor="middle"', content.find(indexLetter)))-1]
        to_be_solved_arr[i][j] = '*'
        final_sol_arr[i][j] = '*'

    temp=temp+1
    j+=1
    if j > 4:
        j = 0
        i+=1

#final_sol_arr = to_be_solved_arr.copy()


#generating dictionaries to associate clues with their answers
#genrating for down
for j in range(5):
    word = ""
    i = 0
    first =  True
    num = 0
    while num_arr[i][j] == -1:
        i+=1
    
    if i < 5: 
        while num_arr[i][j] != -1 and i < 5:
            if(first):
                num = num_arr[i][j]
                first = False
            word += letter_arr[i][j]
            i+=1
            if i > 4:
                break
        
        
        #thisdict = {"number": num, "dir": "down", "clue": downClues[num], "answer": word, "length": len(word)}###############################
        thisdict = {"number": num, "dir": "down", "clue": downClues[str(num)], "answer": word, "length": len(word)}
        
        
        #cluseList.append(dict("number"= num, "dir"= "down", "clue"= downClues[num], "answer"= word, "length"= len(word)))
        clueList.append(thisdict)


#genrating for across
for i in range(5):
    word = ""
    j = 0
    first =  True
    num = 0
    while num_arr[i][j] == -1:
        j+=1
    
    if j < 5: 
        while num_arr[i][j] != -1 and j < 5:
            if(first):
                num = num_arr[i][j]
                first = False
            word += letter_arr[i][j]
            j+=1
            if j > 4:
                break
        
        #thisdict = {"number": num, "dir": "across", "clue": acrossClues[num], "answer": word, "length": len(word)}###############################
        thisdict = {"number": num, "dir": "across", "clue": acrossClues[str(num)], "answer": word, "length": len(word)}
        
        
        
        #cluseList.append(dict("number"= num, "dir"= "across", "clue"= acrossClues[num], "answer"= word, "length"= len(word)))
        clueList.append(thisdict)



#HARD CODED ONLY FOR NOW!!
# line_clue_list = [
#     ['X+Y', 'X/Y', 'LOS', 'RNA', 'BIG', 'ROB', 'TWO', 'GUY', 'MOM', 'MEN', 'CBS'],
#     ['INDEX', 'HAGUE', 'REDDY', 'MARKS', 'MONZA', 'GRANT', 'PARKS', 'LAZIO', 'TESLA', 'S.S.C', 'MODEL', 'TREAT', 'RUDDY', 'TRAMP', 'TRACK', 'DRIVE', 'COVER', 'HELEN', 'OPERA', 'CLARA', 'HOUSE', 'GREED', 'DENCH', 'MILKY', 'CORPS', 'PEARL', 'CROSS', 'POLIO', 'ASTOR', 'MOSES', 'HEDDA', 'NURSE', 'GIVEN', 'F.B.I', 'FLOOD', 'CIVIL', 'JULIA', 'JACOB'],
#     ['RATIO', 'NIGHT', 'IQBAL', 'FORCE', 'H.E.R', 'CHANG', 'YALDĀ', 'LAYER', 'PLATE', 'HORST', 'STALE', 'SNAKE', 'SALEM', 'CADRE', 'RIGHT', 'INNER', 'BASIN', 'CYCLE', 'RANGE', 'DWARF', 'CRUST', 'PLUME', 'CERES', 'PLATE', 'OCEAN', 'WATER', 'EARTH', 'DEPTH', 'UPPER', 'LOWER'],
#     ['KAROL', 'SHEFF', 'I-DLE', 'WELLS', 'KENNY', 'BECKY', 'HERBO', 'ALBUM', 'KUMAR', 'G-400', 'G-MAN', 'STRIP', 'SCALP', 'CRUMB', 'SHELL', 'LADEN', 'STONE', 'CLEAR', 'SCOOP', 'CREAM', 'SHUCK', 'LADLE', 'THROW', 'DEGAS', 'FLICK', 'EMPTY', 'SPOON', 'SCALE', 'LEACH', 'CLEAN', 'DELVE', 'BRUSH', 'LODGE', 'FRANK', 'BLUNT', 'FRAME', 'STEEL', 'ZIGGY', 'WHEAT', 'ARRAY', 'KIWIX', 'TETRA', 'WATER', 'CREAM', 'STARS', 'PLAIN', 'MOVIE'],
#     ['LAW', '3RD', 'POE', 'S.L', '500', 'PET', 'ADD', 'ADD', '2ND', 'SEA', 'ARS', 'U–Z'],
#     ['COOL', 'MATE', 'LIST', 'A.C.', 'MACY', 'S.S.', 'B-52', 'CLUB', 'ROMA', 'MINI', 'A.S.', 'PASS', 'DARK', 'LOBE', 'STAY', 'HERB', 'LOSE', 'RIDE', 'BILL', 'LIST', 'KING', 'PUNK', 'KISS', 'ACID', '2017', 'CITY', 'ARIA', 'CARD', 'MARY', 'FIRE', 'CAMP', 'OHIO', 'MASK', '20TH', 'TOUR', 'LIMA', 'BAND', 'HERO', 'MAPS', '2018', 'CARS'],
#     ['GUNS', 'ROCK', 'BONE', 'CLUB', 'DALE', 'CHIP', 'BOYZ', 'WILD', 'HOOD', 'ROLL', 'ROAD', 'PIKE', 'JOIN', 'STAY', 'LIST', '94TH', 'FARM', 'MIKE', 'BETH', 'OHIO', '1–99', 'HIGH', 'IOWA', 'ROAD', 'YORK'],
#     ['TOUGH', 'FADED', 'DIXIT', 'TAMPA', 'CASEY', 'MIGOS', 'SHINE'],
#     ['COOL', 'LIST', 'A.C.', 'MACY', 'S.S.', 'B-52', 'CLUB', 'ROMA', 'MINI', 'FILM', 'A.S.', '1998', 'U.S.', 'NOSH', 'BITE', 'MEAL', 'NAME', 'KING', '2008', 'WEST', '2016', 'LIST'],
#     ['TOYS', 'GT-R', 'FORD', 'REAL', 'R-36', 'RENO', 'TYPE', 'VASU', 'POET', '', 'LAOS', 'LIST', 'WOOD', 'LEFT', '1848', 'MARX', 'PAUL', 'FILM', '1818', 'HANS', 'ZION', 'KARL', 'YIWU', '19TH']
# ]

print("generate keywords from clues and solve the puzzle")
line_clue_list = []
for i in range(len(clueList)):
    print("analyzing clue " + str(i))
    pos_answers = possible_answers(clueList[i]["clue"], clueList[i]["length"])
    #line_clue_list.append(possible_answers(clueList[i]["clue"], clueList[i]["length"]))
    line_clue_list.append(pos_answers)


not_to_include = [] #represents the index of those words not included in the sol array (impossible to compute) above so they will not be considered
to_include = []
index_clue_list = []
index_clue_list_2 = []
for i in range(len(line_clue_list)):
    if clueList[i]["answer"] not in line_clue_list[i]:
        not_to_include.append({"number": clueList[i]["number"], "dir": clueList[i]["dir"],  "ans": clueList[i]["answer"], "length": clueList[i]["length"]})
        index_clue_list_2.append(line_clue_list[i])
    else:
        to_include.append({"number": clueList[i]["number"], "dir": clueList[i]["dir"],  "ans": clueList[i]["answer"], "length": clueList[i]["length"]})
        index_clue_list.append(line_clue_list[i])

# for i in range(len(num_arr)):
#     print(num_arr[i])

# for i in range(len(to_be_solved_arr)):
#     print(to_be_solved_arr[i])

#filling the puzzle grid with the words for which the solution could not be determined
for i in range(len(not_to_include)):
    cur = not_to_include[i]
    a = 0
    b = 0
    direction = ""
    ans = ""
    length = 0
    done = False
    for x in range(5):
        for y in range(5):
            if num_arr[x][y] == cur["number"]:
                a = x
                b = y
                direction = cur["dir"]
                length = cur["length"]
                ans = cur["ans"]
                done = True
                break
        
        if done:
            break
    
    if direction == "down":
        index = 0
        for p in range(a, length):
            to_be_solved_arr[p][b] = ans[index]
            index+=1
    else:
        index = 0
        for p in range(b, length):
            to_be_solved_arr[a][p] = ans[index]
            index+=1

# print("-------------------------------------------------------------------")

# for i in range(len(to_be_solved_arr)):
#     print(to_be_solved_arr[i])

# print("final_sol_arr")
# for j in range(len(final_sol_arr)):
#     print(final_sol_arr[j])
# print("-------------------------------------------------------------------")


#generating words 
for i in range(len(to_include)):
    resultant_words = fillWords(index_clue_list[i], num_arr, [to_include[i]["number"], to_include[i]["dir"]], to_be_solved_arr, to_include[i]["length"])
    #to_be_solved_arr = fillSolution(resultant_words, num_arr, [to_include[i]["number"], to_include[i]["dir"]], to_be_solved_arr, to_include[i]["length"])
    final_sol_arr = fillSolution(resultant_words, num_arr, [to_include[i]["number"], to_include[i]["dir"]], final_sol_arr, to_include[i]["length"])
    #print(resultant_words)
#     for j in range(len(final_sol_arr)):
#         print(final_sol_arr[j])

# print("-------------------------------------------------------------------")

for i in range(len(not_to_include)):
    #resultant_words = fillWords(index_clue_list_2[i], num_arr, [not_to_include[i]["number"], not_to_include[i]["dir"]], to_be_solved_arr, to_include[i]["length"])
    #to_be_solved_arr = fillSolution(resultant_words, num_arr, [to_include[i]["number"], to_include[i]["dir"]], to_be_solved_arr, to_include[i]["length"])
    final_sol_arr = fillSolution(index_clue_list_2[i], num_arr, [not_to_include[i]["number"], not_to_include[i]["dir"]], final_sol_arr, not_to_include[i]["length"])
    # print("")
    # for j in range(len(final_sol_arr)):
    #     print(final_sol_arr[j])




#filling the solution grid with the solution letters
temp = 0
i = 0
j = 0
while temp < 25:
    #indexLetter = 'id="cell-id-' + str(temp) 
    #indexLetter = indexLetter + '"'
    #si = len(indexLetter)
    #letter = content[content.find(indexLetter) + (si + 8):content.find(indexLetter) + (si + 18)]
    letter = final_sol_arr[i][j]


    if letter == '!':
        lent = int(temp / 5)
        wid = temp % 5
        fillGrey(ans_grid, wid, lent)                 
        #temp=temp+1
        #continue

    else:
        indexStart = content.find('text-anchor="start"', content.find(indexLetter), content.find('text-anchor="middle"', content.find(indexLetter)))
        if indexStart != (-1):
            markN(ans_grid, int(temp / 5), (temp % 5), content[content.find("</text>", indexStart) + 7])
        fillWord(ans_grid, int(temp / 5), (temp % 5), letter)
        #letter_arr[i][j] = content[content.find('</text>',content.find('text-anchor="middle"', content.find(indexLetter)))-1]
        #to_be_solved_arr[i][j] = '*'
        #final_sol_arr[i][j] = '*'

    temp=temp+1
    j+=1
    if j > 4:
        j = 0
        i+=1


#creating group name and current date and time
description = tk.Canvas(window,height = 105,width=250,highlightbackground='black', bg='white')
description.place(x=175,y=450)
description.create_text(128,20, font=('Arial',15),text='Group Name: YAINDU')
date = datetime.today().strftime('%d-%m-%Y')
description.create_text(107,45, font=('Arial',15),text='Date: '+str(date))

curTime = datetime.now() + timedelta(hours=0)
description.create_text(98,70, font=('Arial',15),text='Time: ' + curTime.strftime("%H:%M:%S"))

#loop to run rin the window
window.mainloop()