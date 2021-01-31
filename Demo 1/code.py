import tkinter as tk #gui library

from selenium import webdriver  #for web scrapping

from selenium.webdriver.common.keys import Keys

import time

from time import gmtime, strftime

from datetime import datetime

"""

This program creates a mini crossword puzzle similar to the one at www.nytimes.com/crosswords/game/mini.

It extracts the puzzle data from the same websites. It uses the Selenium library in order to extract

relevant infomration from the website. Furthermore, the Tkinter framework is used to build the gui

components.

@authors:   Umer Shamaan

            Taha Khurram

            Hassan Raza Warraich

            Muhammad Ali Khaqan
"""



cellSize = 75  #default size of a grid cell


cluseList = []  #store the clues and their information


# Creating grid 

def createGrid():
    wid = 0
    while wid < (5 * cellSize)+1:
        lent = 0
        while lent < (5 * cellSize)+1:
            grid.create_rectangle(wid, lent, cellSize, cellSize, outline = 'grey')
            lent = lent + cellSize
        wid = wid + cellSize
    return



#to fill the wordless blocks
def fillGrey(i, j):
    grid.create_rectangle(i * cellSize, j * cellSize, i * cellSize + cellSize, j * cellSize + cellSize, fill='grey')
    return



# filling grid cells with the solution letters 
lSize = 50 #the size of the letter
def fillWord(lent, wid, letter):
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
        size = size + 36
    return


#filling grid numbers
nSize = 15
def markN(lent, wid, num):
    x = cellSize * wid + 10
    y = cellSize * lent + 12
    grid.create_text(x, y, font=("Times", nSize), text = num)
    return


# Printing the clues for down
def down():
    clues.create_text(450,50,font=('Times',36),text='Down')
    size = 0
    for i in downClues:
        clues.create_text(450, 100 + size,font=('Times',14), anchor='w', text= i + ": " + downClues[i], width=tWidth)
        size = size+36
    return



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
window.geometry("1366x768") #setting window size

# creating puzzle grid
grid = tk.Canvas(window,width=cellSize * 5,height=cellSize * 5, bg='white')
grid.place(x=50,y=50)
createGrid()



######################################################################################

temp = 0
while temp < 25:
    indexLetter = 'id="cell-id-' + str(temp) 
    indexLetter = indexLetter + '"'
    si = len(indexLetter)
    letter = content[content.find(indexLetter) + (si + 8):content.find(indexLetter) + (si + 18)]

    if letter == 'Cell-block':
        lent = int(temp / 5)
        wid = temp % 5
        fillGrey(wid, lent)                 
        temp=temp+1
        continue

    else:
        indexStart = content.find('text-anchor="start"', content.find(indexLetter), content.find('text-anchor="middle"', content.find(indexLetter)))
        if indexStart != (-1):
            markN(int(temp / 5), (temp % 5), content[content.find("</text>", indexStart) + 7])

    temp+=1



##############################################################################################


# create clues
clues = tk.Canvas(window,height = 400,width=800, bg='white')               
clues.place(x=600,y=40)
downClues = dict()
acrossClues = dict()


index = content.find("</span>", content.find("Across"))
initial = 0
fina = 5
while initial < fina:
    initial =initial+1
    end = content.find("<", content.find(">", index + 8))
    acrossClues[content[index-1]] = content[(content.find(">", index + 8))+1:end]
    #clue = dict(pos = content[index-1], content = content[(content.find(">", index + 8))+1:end])
    index = content.find("</span>", end + 10)

across()              


index = content.find("</span>", content.find("Down", end))
initial = 0
while initial < fina:
    initial =initial+1
    end = content.find("<", content.find(">", index + 8))
    downClues[content[index-1]] = content[(content.find(">", index + 8))+1:end]
    index = content.find("</span>", end + 10)

down()


print(acrossClues)
print(downClues)



#filling the grid with the solution letters
temp = 0
while temp < 25:
    indexLetter = 'id="cell-id-' + str(temp) 
    indexLetter = indexLetter + '"'
    si = len(indexLetter)
    letter = content[content.find(indexLetter) + (si + 8):content.find(indexLetter) + (si + 18)]


    if letter == 'Cell-block':
        lent = int(temp / 5)
        wid = temp % 5
        fillGrey(wid, lent)                 
        temp=temp+1
        continue

    else:
        indexStart = content.find('text-anchor="start"', content.find(indexLetter), content.find('text-anchor="middle"', content.find(indexLetter)))
        if indexStart != (-1):
            markN(int(temp / 5), (temp % 5), content[content.find("</text>", indexStart) + 7])
        fillWord(int(temp / 5), (temp % 5), content[content.find('</text>',content.find('text-anchor="middle"', content.find(indexLetter)))-1])

    temp=temp+1



#creating group name and current date and time
description = tk.Canvas(window,height = 105,width=250,highlightbackground='black', bg='white')
description.place(x=175,y=450)
description.create_text(128,20, font=('Arial',15),text='Group Name: YAINDU')
date = datetime.today().strftime('%d-%m-%Y')
description.create_text(105,40, font=('Arial',15),text='Date:'+str(date))
description.create_text(98,60, font=('Arial',15),text='Time: ' + strftime("%H:%M:%S", gmtime()))


#loop to run rin the window
window.mainloop()
