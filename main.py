# Jennifer Yang Birthday Tracker
import tkinter as tk
import time
import datetime
from dateutil.relativedelta import relativedelta

# Creating window
window = tk.Tk()
window.title("Birthday Tracker")
birthdayDict = {}

# Reading current birthdays in file into dictionary
birthdayFile = open('birthdays.txt', 'r')
birthdayFile.seek(0)
for line in birthdayFile:
  birthdayDict[line[:line.find(":")]] = line[line.find("/") -
                                             2:line.find("/") + 8]
# Closing file
birthdayFile.close()

# Month list for converting from month name to month number and dropdown
months = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct",
    "Nov", "Dec"
]
# Date list for dropdown
dates = [
    "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12",
    "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24",
    "25", "26", "27", "28", "29", "30", "31"
]


# Editing the dictionary if save pressed and closes editWindow
def updateEditedBirthdays(name, newMonth, newDate, newYear):
  global editWindow, birthdayDict
  if (months.index(newMonth) < 9):
    newMonth = "0" + str(months.index(newMonth) + 1)
  else:
    newMonth = str(months.index(newMonth) + 1)
  birthdayDict[name] = newMonth + "/" + newDate + "/" + newYear
  editWindow.destroy()


# Edit birthday window
def editBirthdays():
  global birthdayDict, editWindow
  names = []
  for name in birthdayDict:
    names.append(name)
  editWindow = tk.Toplevel()
  nameLabel = tk.StringVar()
  nameLabel.set("Select the birthday to edit")
  nameDropdown = tk.OptionMenu(editWindow, nameLabel, *names)
  newYearLabel = tk.Label(master=editWindow, text="Enter the new birth year")
  newYear = tk.Entry(master=editWindow, width=6)
  nameDropdown.pack()
  monthLabel = tk.StringVar()
  monthLabel.set("Select a month")
  monthDrop = tk.OptionMenu(editWindow, monthLabel, *months)
  dateLabel = tk.StringVar()
  dateLabel.set("Select a date")
  dateDrop = tk.OptionMenu(editWindow, dateLabel, *dates)
  saveButton = tk.Button(
      master=editWindow,
      text="Save",
      command=lambda: updateEditedBirthdays(nameLabel.get(), monthLabel.get(),
                                            dateLabel.get(), newYear.get()))
  nameDropdown.pack()
  newYearLabel.pack()
  newYear.pack()
  monthDrop.pack()
  dateDrop.pack()
  saveButton.pack()


# Display birthday window
def displayBirthdays():
  global birthdayDict
  displayWindow = tk.Toplevel()
  today = datetime.date.today()
  for bday in birthdayDict:
    bdayDate = datetime.date(int(birthdayDict[bday][6:]),
                             int(birthdayDict[bday][:2]),
                             int(birthdayDict[bday][3:5]))
    rdelta = relativedelta(today, bdayDate)
    tk.Label(master=displayWindow,
             text=bday + " (" + birthdayDict[bday] + ") is " +
             str(rdelta.years) + " years " + str(rdelta.months) + " months " +
             str(rdelta.days) + " days old.").pack()
  tk.Button(master=displayWindow,
            text="Close",
            command=lambda: displayWindow.destroy()).pack()


# Saves added birthdays and closes addWindow
def addToDict(nameSelected, monthSelected, dateSelected, yearSelected):
  global addWindow
  if nameSelected in birthdayDict:
    errorWindow = tk.Toplevel()
    errorMessage = tk.Label(
        master=errorWindow,
        text="Birthday already exists. Try the edit button")
    errorButton = tk.Button(master=errorWindow,
                            text="Close",
                            command=lambda: errorWindow.destroy())
    errorMessage.pack()
    errorButton.pack()
  else:
    m = str(months.index(monthSelected) + 1)
    if (int(m) < 10): m = "0" + m
    birthdayDict[nameSelected] = m + "/" + dateSelected + "/" + yearSelected
    addWindow.destroy()


# Add birthday window
def addBirthday():
  global months, dates, addWindow

  addWindow = tk.Toplevel()

  frame2 = tk.Frame(master=addWindow)
  nameLabel = tk.Label(master=frame2, text="Enter name")
  nameEntry = tk.Entry(master=frame2, width=10)
  yearLabel = tk.Label(master=frame2, text="Enter the birth year")
  year = tk.Entry(master=frame2, width=6)
  nameLabel.pack()
  nameEntry.pack()
  yearLabel.pack()
  year.pack()
  frame2.pack(side=tk.TOP)

  frame3 = tk.Frame(master=addWindow)
  monthLabel = tk.StringVar()
  monthLabel.set("Select a month")
  monthDrop = tk.OptionMenu(frame3, monthLabel, *months)
  monthDrop.pack()
  frame3.pack(side=tk.TOP)

  frame4 = tk.Frame(master=addWindow)
  dateLabel = tk.StringVar()
  dateLabel.set("Select a date")
  dateDrop = tk.OptionMenu(frame4, dateLabel, *dates)
  submitButton = tk.Button(master=frame4,
                           text="Save",
                           command=lambda: addToDict(nameEntry.get(
                           ), monthLabel.get(), dateLabel.get(), year.get()))
  dateDrop.pack()
  submitButton.pack()
  frame4.pack(side=tk.TOP)


# Ends program and saves birthdays to file
def closeWindow():
  global window
  window.destroy()
  birthdayFile = open('birthdays.txt', 'w')
  for bday in birthdayDict:
    birthdayFile.write(bday + ": " + birthdayDict[bday] + "\n")
  birthdayFile.close()
  exit()


# Homepage
frame1 = tk.Frame(master=window)
displayButton = tk.Button(master=frame1,
                          text="Show birthdays",
                          command=lambda: displayBirthdays())
addButton = tk.Button(master=frame1,
                      text="Add birthday",
                      command=lambda: addBirthday())
editButton = tk.Button(master=frame1,
                       text="Edit birthday",
                       command=lambda: editBirthdays())
doneButton = tk.Button(master=frame1,
                       text="Done? Click to save & exit",
                       command=lambda: closeWindow())
displayButton.pack()
addButton.pack()
editButton.pack()
doneButton.pack()
frame1.pack()

# Mainloop so window doesn't disappear
window.mainloop()
