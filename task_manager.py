# =====importing libraries===========
from datetime import date       # this will help setting the current date
from datetime import datetime   
import os                       # importing os to check if a file exists
import math                     # importing math to round the percentages

# =====functions===========
# creates spaces and separates terminal printed text
def spacer():
    return print("\n====================================================================================================\n")

def register_user(username, password, confirm_password):
    # initializing dictionary that stores registered usernames 
    usernames = {}
    users_generated = 0

    # opening and reading the registered users
    with open("user.txt", "r") as user_file:
        for line in user_file:
            # assigning Key (k) and Value (v) of each line
            k, v = line.strip().split(", ")
            usernames[k] = v

        # checking all conditions to avoid errors
        if username in usernames:
            spacer()
            print("ERROR: Username already in use. Please choose a different username.")
            spacer()

        # registering user if username is unique and bot passwords are matching.
        elif password == confirm_password:
            with open("user.txt", "a") as user_file:
                user_file.write(f"\n{username}, {password}")
                usernames[username] = password
                users_generated += 1
                print("\nRegistration successful!\n")

        # checking if passwords are matching before registering user
        elif password != confirm_password:
            spacer()
            print("ERROR: Passwords are not matching.")
            spacer()


def add_task(assign_task_to_user, task_title, task_description, task_deadline, is_task_complete):
    # getting current date - from datetime import date and formatting it
    # learned how to get today's date on StackOverflow
    # at the following link:
    # (https://stackoverflow.com/questions/32490629/getting-todays-date-in-yyyy-mm-dd-in-python)
    task_submission_date = date.today().strftime("%d %b %Y")

    # formatting the deadline to conform to standards
    task_deadline = date(int(task_deadline[-1]), int(task_deadline[-2]), int(task_deadline[-3]))
    formatted_deadline = task_deadline.strftime("%d %b %Y")
        
    # opening task file and using string interpolation to write in tasks.txt
    # using a ternary operator append "Yes" or "No" absed on the completion of the task
    with open("tasks.txt", "a") as task_file:
        if assign_task_to_user in logged_usernames:
            task_file.write(f"\n{assign_task_to_user}, {task_title}, {task_description}, {task_submission_date}, {formatted_deadline}, {is_task_complete}")
            
            print("\nTask assigned successfully. Well done!")
            spacer()

        else:
            spacer()
            print("ERROR: Username not found. You cannot assign a task to unknown user.")
            spacer()
    

def view_all_tasks():
    with open("tasks.txt", "r") as tasks_data:
    # looping through line and positions ('pos') usin enumerate tokeep track of the index of the lines
        for pos, line in enumerate(tasks_data, 1):
            # separating the data by lines and each line by commas
            split_data = line.split(", ")

            # adding all info into a single variable
            output = f"Task ID: \t\t {pos}\n"
            output += f"Task assigned to: \t {split_data[0]}\n"
            output += f"Task title: \t\t {split_data[1]}\n"
            output += f"Task description: \t {split_data[2]}\n"
            output += f"Creation date: \t\t {split_data[3]}\n"
            output += f"Due date: \t\t {split_data[4]}\n"
            output += f"Task Complete? \t\t {split_data[5]}"

            # printing out the result of the variable
            print(output)
            spacer()


def view_user_tasks():
    print("\nHere are your tasks:")
    spacer()

    # looping through line and positions ('pos') usin enumerate to keep track of the index of the lines
    for pos, line in enumerate(tasks_data, 1):
        # separating the data by lines and each line by commas
        split_data = line.split(", ")
        
        # checking if tasks user and user logged in are matching. This will display only the users tasks
        if split_data[0] == username:
            # adding all info into a single variable
            output = f"Task ID: \t\t {pos}\n"
            output += f"Task assigned to: \t {split_data[0]}\n"
            output += f"Task title: \t\t {split_data[1]}\n"
            output += f"Task description: \t {split_data[2]}\n"
            output += f"Creation date: \t\t {split_data[3]}\n"
            output += f"Due date: \t\t {split_data[4]}\n"
            output += f"Task Complete? \t\t {split_data[5]}"

            # printing out the result of the variable
            print(output)
            spacer()
    

def display_statistics():
    # if these files exists print out what they have inside
    if os.path.exists("user_overview.txt") and os.path.exists("tasks_overview.txt"):
        spacer()

        with open("user_overview.txt", "r") as f:
            for line in f:
                print(line.strip("\n"))

        spacer()

        with open("tasks_overview.txt", "r") as f:
            for line in f:
                print(line.strip("\n"))

        spacer()
    # otherwise create call function that generates them
    else:
        generate_user_overview()
        generate_task_overview()


def change_assigned_user():
    # asking user who they want to assign the task to
    chosen_user = input("\nWho do you want to assign this task to?\n\n: ").lower()

    # checking if the user exists in the list of logged in users
    if chosen_user in logged_usernames:
        # updating user
        split_data[0] = chosen_user
        # joining the list into a string and storing everything in a new variable
        new_data = ", ".join(split_data)
        tasks_data[selected_task] = new_data

        # writing back everything on the tasks file
        tasks_write = open("tasks.txt", "w")
        for line in tasks_data:
            tasks_write.write(line)

        print("\nTask assigned successfully!")
        spacer()

        # at the end of this `while True:` close all the open files and break the loop
        tasks_write.close()
        tasks_read.close()
                        
        # error handling in case entered user doesn't exist
    else:
        spacer()
        print("ERROR: The user enter does not exist. Enter a registred user.")
        spacer()


def edit_due_date():
    # asking user input the desired due date
    chosen_date = input("\nWhen do you want the due date to be? (DD Mon YYYY)\n\n: ")

    if chosen_date == "":
        print("ERROR: You can't enter a blank date.")
    
    # changing the data in in right line, joining the new list to make it a string
    split_data[-2] = chosen_date
    new_data = ", ".join(split_data)
    tasks_data[selected_task] = new_data

    # opening tasks file to be able to write on it
    tasks_write = open("tasks.txt", "w")
    # replace all the old lines with the fixed ones
    for line in tasks_data:
        tasks_write.write(line)
    
    # printing an output for the user
    print("\nNew date assigned successfully!")
    spacer()

    # closing the tasks
    tasks_write.close()
    tasks_read.close()


def generate_task_overview():
    # tracking tasks creation, completion and if they're overdue
    total_tasks_amount = 0
    tasks_generated = 0
    tasks_completed = 0
    tasks_uncompleted = 0
    tasks_overdue = 0

    # opening the necessary files
    task_overview_write = open("tasks_overview.txt", "w+")
    tasks_read = open("tasks.txt", "r")
    tasks_data = tasks_read.readlines()

    # loop through each line and split it by ', ' - counting the amount of lines as amount of tasks
    for line in tasks_data:
        split_line = line.split(", ")
        total_tasks_amount += 1
                
        # initializing current date and deadline into individual variables to make it easier to read
        current_date = datetime.now()
        task_deadline = datetime.strptime(split_line[-2], "%d %b %Y")

        # checking if the task is completed or not
        if split_line[-1] == "Yes\n":
            tasks_completed += 1

        elif split_line[-1] == "No\n":
            tasks_uncompleted += 1
                
        # checking if the task is overdue
        if current_date > task_deadline:
            tasks_overdue += 1

    # formatting the output    
    output = "Here is an overview of the tasks\n\n"
    output += f"Task generated: \t {tasks_generated}\n"
    output += f"Task completed: \t {tasks_completed}\n"
    output += f"Task uncompleted: \t {tasks_uncompleted}\n"
    output += f"Task overdue: \t\t {tasks_overdue}\n"
    output += f"Task uncompleted: \t {math.floor((tasks_uncompleted / total_tasks_amount) * 100)} %\n"
    output += f"Task overdue: \t\t {math.floor((tasks_overdue / total_tasks_amount) * 100)} %"

    print(output)
    spacer()

    # closing the files
    task_overview_write.writelines(output)
    task_overview_write.close()
    tasks_read.close()


def generate_user_overview():
    # initilizing and opening user overview file
    user_overview_write = open("user_overview.txt", "w+")

    # initializing a serie of variables and a dictionary to store useful data
    tasks_per_user = {}
    total_users = 0
    tasks_completed = 0
    tasks_uncompleted = 0
    tasks_overdue = 0

    # counting the amount of users by reading each line inside 'user.txt'
    with open("user.txt", "r") as user_file:
        for line in user_file:
            total_users += 1
              
    # opening the tasks file to extract data
    with open("tasks.txt", "r") as tasks_file:
        tasks = tasks_file.read().splitlines()
                
        # looping through each task
        for task in tasks:
            split_task = task.split(", ")
            user = split_task[0]

            # assigning to each user (key inside the dict) the amount of tasks assigned (value insiide the dict)
            if user in tasks_per_user:
                tasks_per_user[user] += 1

            else:
                tasks_per_user[user] = 1

            # checking if the tasks are completed or not
            if split_task[-1] == "Yes\n":
                tasks_completed += 1

            else:
                tasks_uncompleted += 1
                    
            # initializing current date and deadline into individual variables to make it easier to read
            current_date = datetime.now()
            task_deadline = datetime.strptime(split_task[-2], "%d %b %Y")

            # checking if the task is overdue
            if current_date > task_deadline:
                tasks_overdue += 1

        # storing the total amount of tasks by adding all the tasks given to the users
        total_tasks = sum(tasks_per_user.values())

        # formatting and then printing the common output
        common_output = f"Here is an overview of users\n\n"
        common_output += f"Users: \t\t\t {total_users}\n"
        common_output += f"Tasks amount: \t\t {total_tasks}"
        common_output += "\n\n"

        spacer()
        print(common_output)
        spacer()

        user_overview_write.writelines(common_output)

        # going through each user statistic and then formatting the output and printing it
        for user, tasks in tasks_per_user.items():
            percentage = math.floor((tasks / total_tasks) * 100)
            completed = math.floor((tasks_completed / total_tasks) * 100)
            uncompleted = math.floor((tasks_uncompleted / total_tasks) * 100)
            overdue = math.floor((tasks_overdue / total_tasks) * 100)

            # checking if the task is completed or not
            if split_task[-1] == "Yes\n":
                tasks_completed += 1

            elif split_task[-1] == "No\n":
                tasks_uncompleted += 1

            output_per_user =  f"User: \t\t\t {user}\n\n"
            output_per_user += f"Assigned tasks: \t {percentage} %\n"
            output_per_user += f"Completed tasks: \t {completed} %\n"
            output_per_user += f"Uncompleted tasks: \t {uncompleted} %\n"
            output_per_user += f"Overdue tasks: \t\t {overdue} %\n\n"

            print(output_per_user)
            spacer()

            # writing the whole output into the user overview file
            user_overview_write.writelines(output_per_user)
                        
        # closing the overview file opened at the beginning of this func
        user_overview_write.close()


# ====Login Section====

# variables that stores user.txt users and passwords
logged_usernames = []
logged_passwords = []

# tracking tasks generation
tasks_generated = 0
users_generated = 0

# opening and reading files and assigning value to a variable
tasks_read = open("tasks.txt", "r")
tasks_data = tasks_read.readlines()

users_read = open("user.txt", "r")
users_data = users_read.readlines()

# checking usernames and passwords
for line in users_data:
    username, password = line.strip().split(", ")
    logged_usernames.append(username)
    logged_passwords.append(password)


# iteration through until username and passwords are correct
while True:
    # ask user to input username and password
    username = input("Enter your username: ").lower()
    password = input("Enter your password: ").lower()

    if username in logged_usernames and password in logged_passwords:
        print("\nSuccessful Login!\n")
        break

    elif not username in logged_usernames:
        spacer()
        print("ERROR: Wrong username!")
        spacer()

    elif not password in logged_passwords:
        spacer()
        print("ERROR: Wrong password!")
        spacer()

    else:
        spacer()
        print("ERROR: Something went wrong. Please, try again.")
        spacer()

    # closing the files
    users_read.close()


while True:
    # presenting the menu to the user and 
    # making sure that the user input is coneverted to lower case.
    menu = "\nSelect one of the following options below:\n\n"
    menu += "r - Registering a user\n"
    menu += "a - Adding a task\n"
    menu += "va - View all tasks\n"
    menu += "vm - View my task\n"
    # adding special options for admins
    if username == "admin":
        menu += "gr - Generate Report\n"
        menu += "ds - Display Statistics\n"
    menu += "e - Exit\n\n"
    menu += ": "

    # formatting user input to avoid errors
    user_menu_choice = input(menu).lower()

    if user_menu_choice == 'r':
        # asking for user's input
        new_user = input("\nEnter a new username: ").lower()
        new_user_password = input("Enter a new password: ").lower()
        confirm_password = input("Enter the password again: ").lower()

        # func that registers the user
        register_user(new_user, new_user_password, confirm_password)
        users_generated += 1


    elif user_menu_choice == 'a':
        # asking user some input related to the assignment
        assign_task_to_user = input("\nEnter the user that you want to assign the task to: ")            
        task_title = input("Enter the task title: ")
        task_description = input("Enter the task description: ")
        task_deadline = input("Enter the task's deadline following this format: (DD/MM/YYYY) ")
        is_task_complete = input("Has the task been completed? (Yes/No) ").capitalize()

        task_deadline = task_deadline.split("/")
        
        add_task(assign_task_to_user, task_title, task_description, task_deadline, is_task_complete)
        tasks_generated += 1


    elif user_menu_choice == 'va':
        # func that shows all the tasks
        view_all_tasks()
        

    elif user_menu_choice == 'vm':
        # func that shows all the tasks of the logged in user
        view_user_tasks()

        while True:
            output = "\nDo you want to edit a task or go back to the main menu?\n\n"
            output += "st - Select Task\n"
            output += "e - Exit\n\n"
            output += ": "

            user_input = input(output).lower()
            print()

            break

        if user_input == "e":
            continue
        
        elif user_input == "st":
            while True:
                # asking user to select the task via the ID provided
                selected_task = input("Please select a task by entering the Task ID: ")

                # error handling in case user enters an empty string
                if selected_task == "":
                    spacer()
                    print("ERROR: You must select a task to continue.")
                    spacer()
                    continue

                # else turn the input into a integer
                else:
                    selected_task = int(selected_task) - 1

                # matching user choice with the task ID. if task is outside this range print ERROR
                if selected_task < -1 or selected_task >= len(tasks_data):
                    spacer()
                    print("ERROR: Invalid option. Please, pick another one.")
                    spacer()
                    continue
                
                
                # initializing the variable that will hold the selected task 
                edit_data = tasks_data[selected_task]
                break

            
            while True:
                # printing out a menu for the user to choose from 
                output = "\nSelect an option:\n\n"
                output += "-1 - Back to Menu\n"
                output += " 1 - Edit task\n"
                output += " 2 - Mark as completed\n"
                output += "\n: "

                # variable that stores user input
                user_menu_choice = input(output)
                spacer()

                # error handling in case user input is empty
                if user_menu_choice == "":
                    print("ERROR: Select a valid option.")
                    spacer()
                    continue
                
                # turning input into integer
                user_menu_choice = int(user_menu_choice)

                # error handling in case the user selects an index out of range
                if user_menu_choice < -1  or user_menu_choice > 2:
                    spacer()
                    print("ERROR: Invalid option. Please, pick another one.")
                    spacer()
                    continue

                # go back to main menu
                if user_menu_choice == -1:
                    print("\nGoing back to main menu.\n")
                    spacer()
                    break

                # assign task to a different user or edit due date
                elif user_menu_choice == 1:
                    output = "\nSelect an option:\n\n"
                    output += "ed - Edit due Date\n"
                    output += "cu - Change assigned user\n\n"
                    output += ": "

                    user_menu_choice = input(output).lower()
                    spacer()

                    if user_menu_choice == "":
                        print("ERROR: Select a valid option.")
                        spacer()
                        continue

                    # initializing the variable that stores the user selected task data
                    split_data = edit_data.split(", ")

                    # checking if the task is not completed already
                    if split_data[-1] == "No\n":
                        if user_menu_choice == "ed":
                            edit_due_date()

                        elif user_menu_choice == "cu":
                            change_assigned_user()

                    # error handling in case the task is completed
                    else:
                        spacer()
                        print("ERROR: You cannot edit a completed task.")
                        spacer()
                        continue

                # if the user wants to mark a task completed
                elif user_menu_choice == 2:
                    # split the data of the task selected by the user
                    split_data = edit_data.split(", ") 
                    # change the last item in the list by reverse indexing   
                    split_data[-1] = "Yes\n"

                    # store the changes in a new var all joined by ", " and replace the selected task in the original file
                    new_data = ", ".join(split_data)
                    tasks_data[selected_task] = new_data

                    # open the file to write on it and write each line in the file again.
                    tasks_write = open("tasks.txt", "w")
                    for line in tasks_data:
                        tasks_write.write(line)

                    print("\nWell done! Task marked as completed.\n")
                    spacer()

                    # close all the open files
                    tasks_write.close()
                    tasks_read.close()
                    break

        else:
            spacer()
            print("ERROR: Invalid input. Going back to main menu.")
            spacer()
            continue


    elif user_menu_choice == "gr":
        # displaying a selection of options
        output = "\nSelect an option:\n\n"
        output += "to - Task Overview\n"
        output += "uo - User Overview\n\n"
        output += ": "

        user_menu_choice = input(output).lower()

        # based on the user input call the function
        if user_menu_choice == "to":
            generate_task_overview()

        elif user_menu_choice == "uo":
            generate_user_overview()

        # error handling
        else:
            print("ERROR: Select a valid option.")
            spacer()
            

    # display total number of tasks and users
    elif user_menu_choice == 'ds':
        display_statistics()


    elif user_menu_choice == 'e':
        print("\nGoodbye!!!\n")
        exit()


    else:
        print("\nYou have made a wrong choice. Please, try again.\n")
