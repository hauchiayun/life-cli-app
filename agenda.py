from rich.table import Table
from rich.console import Console
from db import fetchData, updateUserData
from main import username
import json

# Create Table
'''
table = Table(title="Weekly Agenda", show_header=True, show_lines=True , header_style="bold magenta")
table.add_column("Time", style="green")
table.add_column("Monday", style="magenta")
table.add_column("Tuesday", style="magenta")
table.add_column("Wednesday", style="magenta")
table.add_column("Thursday", style="magenta")
table.add_column("Friday", style="magenta")
table.add_column("Saturday", style="magenta")
table.add_column("Sunday", style="magenta")
'''

# Create a console to render the table
console = Console()

console.clear()

def convert_to_table(json_data):
    updated_string = json_data.replace("'", "\"")
    table_data = json.loads(updated_string)
    table = Table(title="Weekly Agenda", show_header=True, show_lines=True, header_style="bold magenta")
    
    for i in table_data["columns"]:
        table.add_column(i)
    
    for row_data in table_data["rows"]:
        table.add_row(*[str(row_data[column_name]) for column_name in table_data["columns"]])
    
    return table

def agendaConfig():

    #TLDR: MAKE THEM HAVE MULTIPLE STYLING AND ADD REAL TIME UPDATE AS PROMPT GOES ON.

    print(f"We will now start the reconfiguration of your Weekly agenda. \n")
    timeSlots = int(console.input("[red]How many time slots will they be?: ")) + 1
    time_slot_value = []
    monday_classes = []
    tuesday_classes = []
    wednesday_classes = []
    thursday_classes = []
    friday_classes = []
    saturday_classes = []
    sunday_classes = []

    for i in range(1, timeSlots):
        value = console.input(f"[red]Time Slot {i} Value (example: 9:30am-11:00am): ")
        time_slot_value.append(value)

    for i in range (1, timeSlots):
        value = console.input(f"[red]What [red]lecture[red] is held on [red]Monday[red] during the time of [red]{time_slot_value[i - 1]}[red]? (Leave empty and press enter if none): ")
        monday_classes.append(value)
    
    for i in range (1, timeSlots):
        value = console.input(f"[red]What [red]lecture[red] is held on [red]Tuesday[red] during the time of [red]{time_slot_value[i - 1]}[red]? (Leave empty and press enter if none): ")
        tuesday_classes.append(value)

    for i in range (1, timeSlots):
        value = console.input(f"[red]What [red]lecture[red] is held on [red]Wednesday[red] during the time of [red]{time_slot_value[i - 1]}[red]? (Leave empty and press enter if none): ")
        wednesday_classes.append(value)

    for i in range (1, timeSlots):
        value = console.input(f"[red]What [red]lecture[red] is held on [red]Thursday[red] during the time of [red]{time_slot_value[i - 1]}[red]? (Leave empty and press enter if none): ")
        thursday_classes.append(value)
    
    for i in range (1, timeSlots):
        value = console.input(f"[red]What [red]lecture[red] is held on [red]Friday[red] during the time of [red]{time_slot_value[i - 1]}[red]? (Leave empty and press enter if none): ")
        friday_classes.append(value)

    for i in range (1, timeSlots):
        value = console.input(f"[red]What [red]lecture[red] is held on [red]Saturday[red] during the time of [red]{time_slot_value[i - 1]}[red]? (Leave empty and press enter if none): ")
        saturday_classes.append(value)

    for i in range (1, timeSlots):
        value = console.input(f"[red]What [red]lecture[red] is held on [red]Sunday[red] during the time of [red]{time_slot_value[i - 1]}[red]? (Leave empty and press enter if none): ")
        sunday_classes.append(value)


    # Create a list of dictionaries for each class
    rows = []
    for i in range(1, timeSlots):
        rows.append({
            "Time": time_slot_value[i - 1],
            "Monday": monday_classes[i - 1],
            "Tuesday": tuesday_classes[i - 1],
            "Wednesday": wednesday_classes[i - 1],
            "Thursday": thursday_classes[i - 1],
            "Friday": friday_classes[i - 1],
            "Saturday": saturday_classes[i - 1],
            "Sunday": sunday_classes[i - 1]
        })

    agenda = {
        "columns": [
            "Time", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
        ],

        "rows": rows
    }   

    updateUserData(username, "agenda", str(agenda))

    return str(agenda)


def initAgenda():
    agendaJSON = fetchData(username, "agenda")
    if agendaJSON == '{columns: ["Time", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], rows: []}' or agendaJSON == "{}":
        agendaJSON = agendaConfig()
    console.clear()
    table = convert_to_table(agendaJSON)
    console.print(table)
    option = int(console.input(f"\n 1: Reconfigure agenda \n 2: Reset Data And Exit \n 3: Back Home \n Select an option: "))


    if option == 1:
        console.clear()
        agendaJSON = agendaConfig()
        table = convert_to_table(agendaJSON)
        console.print(table)
    elif option == 2:
        updateUserData(username, "agenda", "{}")
        exit(0)
    elif option == 3:
        exit(0)
    else:
        console.clear()
        console.print(table)
        option = int(console.input(f"\n [red]Invalid Option! 1: Reconfigure agenda \n 2: Reset Data And Exit \n 3: Back Home \n Select an option: "))