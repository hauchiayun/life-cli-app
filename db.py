# -----------------------------------------------------------IMPLEMENTATIONS-------------------------------------------------

from array import array
import json
import os
import sqlite3

class CustomType:
    USERNAME = "username"
    PASSWORD = "password"
    TWOFA = "two_factor_auth"
    TODO = "todo"
    AGENDA = "agenda"

# ---------------------------------------------------------SQL-FUNCTIONS-----------------------------------------------------

def executeSQLFunction(sqlCommand: str):
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    cursor.execute(sqlCommand)
    conn.commit()
    conn.close()

def init():
    executeSQLFunction('''
        CREATE TABLE IF NOT EXISTS user (
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            two_factor_auth BOOLEAN NOT NULL,
            todo JSON NOT NULL,
            agenda JSON NOT NULL
        )
    ''')

# -----------------------------------------------------------FETCH-DATA-----------------------------------------------------

def fetchData(username: str, dataType):
    # Checks
    if dataType not in (CustomType.USERNAME, CustomType.PASSWORD, CustomType.TWOFA, CustomType.TODO, CustomType.AGENDA):
        raise ValueError(f"Invalid data type: {dataType} !")
    
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()

    init()

    cursor.execute(f'SELECT * FROM user WHERE username = "{username}"')
    data = cursor.fetchall()
    
    if dataType == "username":
        value = data[0][0]
        return value
    elif dataType == "password":
        value = data[0][1]
        return value
    elif dataType == "two_factor_auth":
        value = data[0][2]
        return value
    elif dataType == "todo":
        value = data[0][3]
        return value
    elif dataType == "agenda":
        value = data[0][4]
        return value

#------------------------------------------------ADD-UPDATE-REMOVE------------------------------------------------------------

def firstTimeInsert(username: str, password: str, two_factor: bool, todo: str, agenda: str):
    # Connect to the database
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()

    try:
        init()

        # Insert data into the user table
        cursor.execute('''
            INSERT INTO user (username, password, two_factor_auth, todo, agenda)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, password, two_factor, todo, agenda))

        # Commit the changes
        conn.commit()

        print(f"User {username} inserted successfully!")

    except sqlite3.Error as e:
        print(f"Error inserting user: {e}")

    finally:
        # Close the connection
        conn.close()

def updateUserData(username: str, dataType, updatedInfo: str):
    #Checks
    if dataType not in (CustomType.USERNAME, CustomType.PASSWORD, CustomType.TWOFA, CustomType.TODO, CustomType.AGENDA):
        raise ValueError(f"Invalid data type: {dataType} !")
    
    sqlCommand = f'''UPDATE USER SET '{dataType}' = "{updatedInfo}" WHERE username = '{username}';'''
    executeSQLFunction(sqlCommand)

def addTodoTable(username, task):
    data = {
        "task": task,
        "status": "red"
    }

    rows = addTodoRowItemGen(username, data)
    executeSQLFunction(f"""
        UPDATE user
        SET todo = '{rows}'
        WHERE username = '{username}'
    """)

def updateTodoStatus(task, status):
    data = {
        "task": task,
        "status": status
    }

# -------------------------------------------------------GENERATORS-----------------------------------------------------    

def addTodoRowItemGen(username, newObj: object):
    data = str(fetchData(username, "todo"))

    # Sample data: [{"id": "1", "task": "e", "status": "WIP"}]
    updated_string = str(data).replace("'", "\"")
    data_dict = json.loads(updated_string) # Sample [{"task": "e", "status": "WIP"}]
    updated_obj = str(newObj).replace("'", "\"") # {"task": "f", "status": "WIP"}
    new_obj_dict = json.loads(updated_obj) # {"task": "f", "status": "WIP"}

    # Append the new task to the list
    data_dict.append(new_obj_dict)

    # Convert the list back to JSON
    updated_tasks = json.dumps(data_dict, indent=2)

    return updated_tasks

def removeTodoRowItemGen(username, removalID: int):
    data = str(fetchData(username, "todo"))
    dataStr = str(data).replace("'", "\"")
    dataDict = json.loads(dataStr)

    try:
        dataDict.pop(removalID - 1)
        popped = json.dumps(dataDict)
        return popped
    except IndexError:
        return False

def updateTodoRowItemGen(username, updateID: int, status):
    data = str(fetchData(username, "todo"))
    dataStr = str(data).replace("'", "\"")
    dataDict = json.loads(dataStr)

    incomplete = []
    complete = []
    for row in dataDict:
        if row[1] == "red":
            incomplete.append(row)
        elif row[1] == "green":
            complete.append(row)

    e = incomplete.pop(updateID - 1)
    e["status"] = status
    
    index_to_remove = next((index for (index, d) in enumerate(dataDict) if d == e), None)
    if index_to_remove is not None:
        dataDict.pop(index_to_remove)

    dataDict.insert(updateID -1, e)
    
    return dataDict

updateTodoRowItemGen("Chia", 2, "green")

# ---------------------------DEBUGGING SECTION (NOT IN PROD) ----------------------------------------------------------------
"""

init()

os.system('clear')

username = fetchData("Chia", "username")
password = fetchData("Chia", "password")
twoFactor = fetchData("Chia", "two_factor_auth")
todo = fetchData("Chia", "todo")
agenda = fetchData("Chia", "agenda")

print(f"Username: {username} \n Password: {password} \n twoFactor: {twoFactor} \n todo: {todo} \n agenda: {agenda}")

print(f"\n")

updateUserData("Chia", "todo", '{}')


input("Any Key To Exit: ")

"""