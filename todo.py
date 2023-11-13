# ----------------------------------------------IMPLEMENTATIONS---------------------------------

from ctypes import Array
from uu import Error
from warnings import catch_warnings
from db import executeSQLFunction, addTodoRowItemGen, fetchData, updateTodoRowItemGen, updateUserData, addTodoTable
from main import username
import json
import rich
from rich.table import Table
from rich.console import Console

console = Console()

# ----------------------------------------------FRONT-END---------------------------------------

def render_list(rowsArray):

    console.print("[magenda_bold]TODO LIST")
    console.line()
    console.print("Colours:")
    console.print("[red]Red: No progress")
    console.print("[yellow]Yellow: Work In Progress")
    console.print("[green]Green: Done")
    console.line()
    try:
        incomplete = []
        complete = []
        for row in rowsArray:
            if row[1] == "red":
                incomplete.append(row)
            elif row[1] == "green":
                complete.append(row)
        i = 0

        console.print("[red]INCOMPLETED:")
        for row in incomplete:
            i = i + 1
            console.print(f"[red] {i}: {row[0]}")
    except KeyError:
        console.print(f"Its empty here....")
        console.log(rowsArray)

def handleUserInput():
    io = console.input(f"\n 1: Add Todo \n 2: Update Todo Status \n 3: Remove Todo \n 4: Back Home \n Choose an option: ")
    if io == "1":
        console.clear()
        render_list(fetchData(username, "todo"))
        console.print(f"\n [cyan]ADD-TODO")
        taskName = console.input(f"\n Task Name: ")
        addTodoTable(username, taskName)
    elif io == "2":
        console.clear()
        render_list(fetchData(username, "todo"))
        console.print(f"\n [lime]UPDATE-TODO")
        taskID = int(console.input(f"Task ID: "))
        status = console.input(f"Completed Or Incomplete? (y/n): ")
        try:
            if status == "y" or status == "Y":
                updateTodoRowItemGen(username, taskID, "green")
            elif status == "n" or status == "N":
                updateTodoRowItemGen(username, taskID, "red")
            else:
                console.clear()
                render_list(fetchData(username, "todo"))
                console.print(f'[red] Previous Action Failed (Invalid Option on the prompt "Complete Or incomplete" provided {status}. Should be "y" OR "n"), No Action Was Taken.')
        except Error:
            print(Error)
        


# ----------------------------------------------DEBUGGING----------------------------------------

todo_config = fetchData(username, "todo")
todo_config_dict = json.loads(str(todo_config))
console.clear()
render_list(todo_config_dict)
handleUserInput()