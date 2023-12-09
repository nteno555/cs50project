# Jennifer Yang Birthday Tracker
import tkinter as tk
import datetime

# Creating window
window = tk.Tk()
window.title("Grocery Tracker")
foodDict = {}
shoppingList = []

# Month and date lists
months = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct",
    "Nov", "Dec"
]
dates = [
    "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12",
    "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24",
    "25", "26", "27", "28", "29", "30", "31"
]
today = str(datetime.date.today())
today = months[int(today[5:7])-1]+" "+today[-2:]+", "+today[:4]

# Reading current birthdays in file into dictionary
foodFile = open('food.txt', 'r')
foodFile.seek(0)
for line in foodFile:
  line = line.split()
  foodDict[line[0][:-1]] = [int(line[1]), line[5][:-1]]
# Closing file
foodFile.close()

shoppingFile = open('shoppinglist.txt', 'r')
for line in shoppingFile:
  line = line.split()
  shoppingList.append(line[0])
shoppingFile.close()

def displayFood():
  global foodDict, addWindow
  displayWindow = tk.Toplevel()
  for food in foodDict:
    foodDictDate = months[int(foodDict[food][1][5:7])-1]+" "+foodDict[food][1][-2:]+", "+foodDict[food][1][:4]
    tk.Label(master=displayWindow, text=food+": "+str(foodDict[food][0])+" servings since "+foodDictDate).pack()
  closeButton = tk.Button(master=displayWindow, text="Close", command=lambda:displayWindow.destroy())
  closeButton.pack()

def addToDict(food, quantity):
  global foodDict, addWindow
  if (food in foodDict):
    errorWindow = tk.Toplevel()
    errorMessage = tk.Label(master=errorWindow, text="Grocery already exists")
    errorMessage.pack()
    errorClose = tk.Button(master=errorWindow, text="Close", command=lambda:errorWindow.destroy())
    errorClose.pack()
    return
  foodDict[food] = [int(quantity), str(datetime.date.today())]
  addWindow.destroy()


def addFood():
  global addWindow
  addWindow = tk.Toplevel()
  nameFrame = tk.Frame(master=addWindow)
  foodLabel = tk.Label(master=nameFrame, text="Enter grocery: ")
  foodEntry = tk.Entry(master=nameFrame, width=12)
  foodLabel.pack()
  foodEntry.pack()
  nameFrame.pack()
  quantityFrame = tk.Frame(master=addWindow)
  quantityLabel = tk.Label(master=addWindow, text="Enter quantity: ")
  quantityEntry = tk.Entry(master=addWindow, width=4)
  quantityLabel.pack()
  quantityEntry.pack()
  quantityFrame.pack()
  saveButton = tk.Button(master=addWindow, text="Save", command=lambda:addToDict(foodEntry.get(), quantityEntry.get()))
  saveButton.pack()

def displayGroceryList():
  global shoppingList
  groceryDisplay = tk.Toplevel()
  for item in shoppingList:
    tk.Label(master=groceryDisplay, text=item).pack()
  closeGrocery = tk.Button(master=groceryDisplay, text="Close", command=lambda:groceryDisplay.destroy())
  closeGrocery.pack()

def updateGroceryList(food):
  global foodDict, shoppingList
  food = food.lower()
  food = food[0].upper() + food[1:]
  if food in shoppingList: shoppingList.remove(food)
  else: shoppingList.append(food)

def groceryList():
  global shoppingList, foodDict
  groceryEdit = tk.Toplevel()
  tk.Label(master=groceryEdit, text="Type grocery to add or remove from shopping list").pack()
  displayGrocery = tk.Button(master=groceryEdit, text="View shopping list", command=lambda:displayGroceryList())
  displayGrocery.pack()
  groceryEntry = tk.Entry(master=groceryEdit, width=9)
  groceryEntry.pack()
  saveButton = tk.Button(master=groceryEdit, text="Save", command=lambda:updateGroceryList(groceryEntry.get()))
  saveButton.pack()
  closeButton = tk.Button(master=groceryEdit, text="Close", command=lambda:groceryEdit.destroy())
  closeButton.pack()

def updateEditedFood(food, quan):
  global foodDict
  foodDict[food][0] = int(quan)
  foodDict[food][1] = str(datetime.date.today())

def editFood():
  global foodDict
  editWindow = tk.Toplevel()
  dropFrame = tk.Frame(editWindow)
  groceryLabel = tk.StringVar()
  groceryLabel.set("Select grocery")
  groceryDrop = tk.OptionMenu(dropFrame, groceryLabel, *foodDict.keys())
  groceryDrop.pack()
  dropFrame.pack()
  quantityEntry = tk.Entry(master=editWindow, width=5)
  quantityEntry.pack()
  editButton = tk.Button(master=editWindow, text="Save", command=lambda:updateEditedFood(groceryLabel.get(), quantityEntry.get()))
  editButton.pack()
  closeButton = tk.Button(master=editWindow, text="Close", command=lambda:editWindow.destroy())
  closeButton.pack()

def saveAndExit():
  global window
  window.destroy()
  writeFood = open("food.txt", 'w')
  writeShopping = open("shoppinglist.txt", 'w')
  for food in foodDict:
    writeFood.write(food+": "+str(foodDict[food][0])+" servings (Last Updated: "+foodDict[food][1]+")\n")
  for item in shoppingList:
    writeShopping.write(item+"\n")

descriptionLabel = tk.Label(master=window, text="Welcome to your Grocery Tracker!\n Today is "+today+".")
descriptionLabel.pack()
displayButton = tk.Button(master=window, text="View Grocery", command=lambda:displayFood())
displayButton.pack()
addButton = tk.Button(master=window, text="Add Grocery", command=lambda: addFood())
addButton.pack()
listButton = tk.Button(master=window, text="Grocery List", command=lambda: groceryList())
listButton.pack()
removeButton = tk.Button(master=window, text="Update Grocery", command=lambda: editFood())
removeButton.pack()
exitButton = tk.Button(master=window, text="Save and Exit", command=lambda: saveAndExit())
exitButton.pack()

window.mainloop()