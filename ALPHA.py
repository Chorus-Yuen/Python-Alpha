from tkinter import *
import tkinter as tk
from tkinter import messagebox as mb
import time

def setup():
    def change_colour(coord):
        btn = root.alphabet_list[coord[1]][coord[0]]
        if btn[1] == "":
            btn[0].config(bg = red)
            btn[1] = "R"
        elif btn[1] == "R":
            btn[0].config(bg = lblbg)
            btn[1] = ""
    
    root.title("ALPHA")
    root.iconbitmap("A.ico")
    root.attributes("-fullscreen", True)
    root.fullscreen = True
    root.bind("<F11>", toggle_fullscreen)
    root.bind("<Escape>", quit)
    root.width = root.winfo_screenwidth()
    root.height = root.winfo_screenheight()
    root.configure(bg = rootbg)
    root.bind("<BackSpace>", backspace)
    root.bind("<Delete>", backspace)
    root.bind("<Return>", submit)
    
    root.title_label = Label(root, text = "ALPHA", font = "Calibri 60 bold underline", bg = rootbg)
    root.title_label.place(x = root.width//2, y = 0, anchor = N)
    
    test_frame = Frame(root, bg = rootbg)
    test_frame.place(x = root.width//2, y = root.height*5//6, anchor = S)
    
    root.row_count = 0
    root.column_count = 0
    root.test_list = []
    for y in range(6): #len of word
        temp_l = []
        for x in range(5): #num of trials
            label = Label(test_frame, text = "", font = "Calirbi 32 bold", width = 1,
                          bg = lblbg, height = 1, relief = "ridge", bd = 1)
            label.grid(row = y, column = x, padx = 2, pady = 4, ipadx = 20, ipady = 12)
            temp_l.append([label, ""])
        root.test_list.append(temp_l)
    submit_btn = Button(test_frame, text = "Submit!", font = "Calirbi 20 bold", command = confirm_pressed)
    submit_btn.grid(row = 6, column = 0, columnspan = 5, pady = 20, ipadx = 10, ipady = 10)
    
    alphabet_frame = Frame(root, bg = rootbg)
    alphabet_frame.place(x = root.width//2, y = root.height, anchor = S)
    
    root.alphabet_list = []
    for y in range(2):
        temp_l = []
        for x in range(13):
            letter = chr(y * 13 + x + 65)
            root.bind(chr(y * 13 + x + 97), key_pressed)
            root.bind(chr(y * 13 + x + 65), key_pressed)
            lbl = Button(alphabet_frame, text = letter, width = 2, height = 1, font = "Calibri 20 bold",
                         bg = lblbg, bd = 1, command = lambda coord = [x, y]: change_colour(coord))
            lbl.grid(row = y, column = x, padx = 4, pady = 8, ipadx = 3, ipady = 3)
            temp_l.append([lbl, ""])
        root.alphabet_list.append(temp_l)

def reset(option):
    root.row_count = 0
    root.column_count = 0
    for y in root.test_list:
        for x in y:
            x[0].config(text = "", bg = lblbg)
            x[1] = ""
            animation()
    for y in root.alphabet_list:
        for x in y:
            x[0].config(bg = lblbg)
            x[1] = ""
            animation()
    if option == "GG":
        for i in range(len(root.test_list[5])):
            lbl = root.test_list[5][i]
            lbl[0].config(text = root.chosen_word[i].upper(), bg = green)
            animation()

def choose_word():
    def check_word(cw_window, ent):
        root.chosen_word = ent.get().lower()
        valid = False
        with open("5LetterWords.txt", 'r') as file:
            five_letter_words = file.readlines()
        if len(root.chosen_word) == 5 and root.chosen_word + "\n" in five_letter_words:
            valid = True
            cw_window.destroy()
            root.deiconify()
        else:
            for fg in ("Red", "Black"):
                ent.config(fg = fg)
                time.sleep(0.2)
                cw_window.update()
    
    def caps(event):
        text = cw_window.ent.get().upper()
        cw_window.ent.delete(0, END)
        cw_window.ent.insert(0, text)
    
    cw_window = Toplevel()
    cw_window.iconbitmap("A.ico")
    x = 360
    y = 80
    cw_window.geometry("{}x{}+{}+{}".format(x, y,
                                           root.width // 2 - x // 2,
                                           root.height // 2 - y // 2 - 50))
    cw_window.focus()
    cw_window.resizable(False, False)
    cw_window.grab_set()
    cw_window.attributes("-topmost", True)
    #root.iconify()
    cw_window.ent = tk.Entry(cw_window, font = "Calibri 26", width = 10, justify = "center")
    cw_window.ent.grid(row = 0, column = 0, padx = 10, pady = 10)
    cw_window.ent.bind("<KeyRelease>", caps)
    cw_window.ent.icursor(0)
    btn = Button(cw_window, text = "OK!", bg = rootbg, width = 6, font = "Calibri 16",
                 command = lambda: check_word(cw_window, cw_window.ent))
    btn.grid(row = 0, column = 1, padx = 10, pady = 10)

def highlight(option, i):
    letter = root.test_list[root.row_count][i][0].cget("text")
    n = ord(letter) - 65
    x = n % 13
    y = n // 13
    if option == "G": colour = green
    elif option == "A": colour = amber
    else: colour = grey
    root.test_list[root.row_count][i][0].config(bg = colour)
    root.alphabet_list[y][x][0].config(bg = colour)
    root.alphabet_list[y][x][1] = option

def animation():
    time.sleep(0.02)
    root.update()

def comparison(guess):
    if guess == root.chosen_word:
        for i in range(5):
            highlight("G", i)
            animation()
        return True
    else:
        for i in range(5):
            chosen_occ = 0
            for j in range(5):
                if root.chosen_word[i] == root.chosen_word[j]:
                    chosen_occ += 1
            if chosen_occ != 0:
                guess_occ = 0
                for j in range(5):
                    if guess[j] == root.chosen_word[j] and guess[j] == root.chosen_word[i]:
                        guess_occ += 1
                        root.test_list[root.row_count][j][1] = "G"
                for j in range(5):
                    if guess_occ == chosen_occ:
                        break
                    elif root.test_list[root.row_count][j][1] != "G":
                        if root.chosen_word[i] == guess[j]:
                            root.test_list[root.row_count][j][1] = "A"
                            guess_occ += 1
        for i in range(5):
            letter = root.test_list[root.row_count][i]
            if letter[1] == "":
                root.test_list[root.row_count][i][1] = "B"
        for i in range(5):
            option = root.test_list[root.row_count][i][1]
            highlight(option, i)
            animation()
        return False

def submit(event):
    confirm_pressed()

def confirm_pressed():
    if root.column_count == 5:
        guess = ""
        for i in range(5):
            guess += root.test_list[root.row_count][i][0].cget("text").lower()
        with open("5letterWords.txt", 'r') as file:
            five_letter_dict = file.readlines()
        if guess + "\n" in five_letter_dict:
            correct = comparison(guess)
            if correct:
                #update_score()
                ans = mb.askyesno("Restart", "Do you want to restart?")
                if ans:
                    reset("")
                    choose_word()
                else: root.destroy()
            else:
                root.row_count += 1
                if root.row_count < 6:
                    root.column_count = 0
                else:
                    reset("GG")
                    ans = mb.askyesno("Game over", "Do you want to restart?")
                    if ans:
                        for x in root.test_list[5]:
                            x[0].config(text = "", bg = lblbg)
                            animation()
                        choose_word()
                    else: root.destroy()
        else:
            error()
    else:
        error()

def key_pressed(event):
    if root.column_count < 5:
        letter = event.char.upper()
        root.test_list[root.row_count][root.column_count][0].config(text = letter)
        root.column_count += 1

def backspace(event):
    if root.column_count != 0 :
        root.column_count -= 1
        root.test_list[root.row_count][root.column_count][0].config(text = "")

def error():
    for fg in ("Red", "Black"):
        for lbl in root.test_list[root.row_count]:
            lbl[0].config(fg = fg)
        time.sleep(0.2)
        root.update()

def toggle_fullscreen(event):
    if root.fullscreen:
        root.attributes("-fullscreen", False)
        root.geometry("{}x{}".format(root.width, root.height))
        root.fullscreen = False
    else:
        root.attributes("-fullscreen", True)
        root.fullscreen = True

root = tk.Tk()
rootbg = "#FFFFFF"
lblbg = "#DDDDDD"
green = "#3EC525"
amber = "#F7CE0A"
grey = "#666666"
red = "#CC3232"

setup()
choose_word()

root.mainloop()




