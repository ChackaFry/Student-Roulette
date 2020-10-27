from tkinter import *
import random as rnd
import os
import zipfile


def find_files(files, filetype):
    """
    Finds all files of a specific file type in the current directory
    :param files: List of string containg all files in the directory
    :param filetype: string containing the filetype to be searched for. e.g. ".zip"
    :return: Lis of string containing all files of that filetype
    """
    zip_files = list()
    for file in files:
        if file[-1 * len(filetype):] == filetype:
            zip_files.append(file)
    return zip_files


def select_random(list_of_things):
    """
    Selects a random element from the list
    :param list_of_things: List of any type
    :return: random element from the List
    """
    return list_of_things[rnd.randrange(0, len(list_of_things))]


def new_student(canvas, x, y, text, color, font_size):
    """
    Resets the Canvas, to display a new student
    :param canvas: Canvas to modify
    :param x: int x coordinate of centre of the text
    :param y: int y coordinate of centre of the text
    :param text: string of text to be input into canvas
    :param color: string containing colour info in hex, e.g. "#0f1a2b"
    :param font_size: int representing the font size of the text
    :return: Canvas that has been updated.
    """
    canvas.delete("all")
    canvas.create_text(x, y,
                       fill=color,
                       font=f"Calibri {font_size} italic bold",
                       text=text)
    canvas.pack()

# Find and Extract all ZIP files in the current dir
zip_files = find_files(os.listdir(), ".zip")
for file in zip_files:
    with zipfile.ZipFile(file, "r") as zipObj:
        zipObj.extractall()

# Find, Read and Rewrite all CSV files in the current dir
csv_files = find_files(os.listdir(), ".csv")
for file in csv_files:
    with open(file, "r", encoding="utf-8") as csv:
        full_file = csv.read()
        new_file = ""
        records = full_file.split("\n")
        records.pop(0)  # Remove the header
        if records[-1] == "":
            records.pop(-1)  # Remove the header
        for record in records:
            elements = record.split(",")
            elements.pop(0)  # Remove timestamp
            new_file += f"{elements[0]:}: {elements[1]}\n"
            new_file = new_file.replace("\"", "")  # Remove '"' char from the string
    os.remove(file)  # Deleteing old file
    new = open(file, "w")
    new.write(new_file)
    new.close()

x = open(csv_files[0], "r")
studentARR = x.read().split("\n")  # Getting Student name from the new file
x.close()

maxLength = 0
for student in studentARR:
    if len(student) > maxLength:
        maxLength = len(student)

root = Tk()
root.title("Select a Student")

font_size = 50
width = maxLength * int(50)  # width of window
height = int(font_size) + 30  # height of window
xC = int(width / 2)  # x coordinate of centre of text
yC = int(height / 2)  # x coordinate of centre of text

red = 100
green = 100
blue = 200

can = Canvas(root, width=width, height=height, bg='#000000')
btn_student = Button(root, text="New Student",
                     command=lambda: new_student(can, xC, yC, select_random(studentARR),
                                                 f"#{red:0>2x}{green:0>2x}{blue:0>2x}", font_size))
can.pack()
btn_student.pack()

root.mainloop()
