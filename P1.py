#Author: Yeamin Chowdhury
#Date: 02/25/2023
#Description: This program is a database management system that can create, delete, and alter databases and tables.
#Project: CS - 457 - 01


# import the os and shutil modules
import os
import shutil

# main function that takes input from the user and calls the command function. If the user enters .exit, the program exits
def main():
    try:
        while True:
            
            input_command = input()

            # COVERT THE INPUT TO UPPERCASE
            input_command = input_command.upper()

            if input_command == ".EXIT":
                print("All done.")
                exit()

            # call command function
            command(input_command)
    
    except KeyboardInterrupt:
        print("\nCtrl+C detected. Exiting...")
        

# create a function that takes a string of commands and executes the command by parsing the string in appropriate manner.
def command(input):
    # parse the input into a list
    parsed_command = input.split(";")
    parsed_command = parsed_command[0].split(" ")

    # check if the command arguments are valid and execute it

    try:
        if (len(parsed_command) == 3) and parsed_command[0] == "CREATE" and parsed_command[1] == "DATABASE":
            create_database(parsed_command[2])
        elif (len(parsed_command) == 3) and parsed_command[0] == "DROP" and parsed_command[1] == "DATABASE":
            drop_database(parsed_command[2])
        elif len(parsed_command) == 2 and parsed_command[0] == "USE":
            use_database(parsed_command[1])
        elif parsed_command[0] == "CREATE" and parsed_command[1] == "TABLE":
            variables_list = input[input.find("(") + 1:input.find(";") - 1]
            variable_list = variables_list.split(", ")
            print(variable_list)
            create_table(parsed_command[2], variable_list)
        elif (len(parsed_command) == 3) and parsed_command[0] == "DROP" and parsed_command[1] == "TABLE":
            drop_table(parsed_command[2])
        elif (parsed_command[0] == "ALTER") and (parsed_command[1] == "TABLE"):
            v_list = input.partition("ADD ")[2]
            var_list = v_list[0: v_list.find(";")]
            final_list = var_list.split(", ")
            alter_table(parsed_command[2], final_list)
        elif parsed_command[0] == "SELECT" and parsed_command[1] == "*" and (len(parsed_command) == 4):
            select_table(parsed_command[3])

        else:
            print("Invalid command")

    #if there is not enough amount of armuents in the command, print Insufficient command arguments
    except IndexError:
        print("Insufficient command arguments")


# create database function takes a string as input and creates a database with that name
def create_database(database_name):

    # set the default path to the home directory(where the program is)

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # check if the database already exists
    if os.path.exists(database_name):
        print("!Failed to create database " +
              database_name + " because it already exists.")
        return
    # if the database does not exist, create it
    else:

        os.mkdir(database_name)
        print("Database " + database_name + " created.")


# drop database function
# takes a string as input and deletes the database with that name

def drop_database(database_name):
    # set the default path to the directory that the program is in
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # check if the database exists, delete it
    if os.path.exists(database_name):
        shutil.rmtree(database_name)
        print("Database " + database_name + " deleted")

    # if the database does not exist, print an error message
    else:
        print("!Failed to delete " + database_name +
              " because it does not exist.")


# This function takes a database name as input and changes the current database to the one with that name
def use_database(database_name):
    # change the current diferectory to the folder that the program is in
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # check if the database exists, change the current directory to the database
    if os.path.exists(database_name):
        os.chdir(database_name)
        print("Using database " + database_name + ".")
    # if the database does not exist, print an error message
    else:
        print("Database " + database_name + " does not exist.")


#This function takes a table name as input and creates the table with that name if it does not exist and not in the hoem directory
def create_table(table_name, variable_list):
    # if current directory is same as the directory of the program, then the database is not selected
    if os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
        print("!Failed to create table " + table_name +
              " because no database is selected.")
        return

    # check if the table already exists
    if os.path.exists(table_name):
        print("!Failed to create table " + table_name +
              " because it already exists.")
        return
    else:
        # create the table
        file = open(table_name, "w")
        file.write(" | ".join(variable_list))
        file.close()
        print("Table " + table_name + " created.")

# alter_table function takes a list of strings as input along with table name and alters the table with that name
# it also takes a list of variables as input and adds those variables to the table
#works even if threre is only one variable
def alter_table(table_name, variable_list):
    # if current directory is same as the directory of the program, then the database is not selected
    if os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
        print("!Failed to alter table " + table_name +
              " because no database is selected.")
        return
    # check if the table exists, alter it
    if os.path.exists(table_name):
        file = open(table_name, "a")
        file.write(" | " + " | ".join(variable_list))
        file.close()
        print("Table " + table_name + " altered.")
    # if the table does not exist, print an error message
    else:
        print("!Failed to alter " + table_name +
              " because it does not exist.")


# drop_table function takes a string as input and deletes the table with that name if it exists
def drop_table(table_name):

    # if current directory is same as the directory of the program, then the database is not selected
    # the table cannot be deleted if the database is not selected
    if os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
        print("!Failed to delete table " + table_name +
              " because no database is selected.")
        return
    # check if the table exists, delete it
    if os.path.exists(table_name):
        os.remove(table_name)
        print("Table " + table_name + " deleted.")
    # if the table does not exist, print an error message
    else:
        print("!Failed to delete " + table_name +
              " because it does not exist.")

# select_table function takes a string as input and prints the contents of the table with that name
def select_table(table_name):
    # if current directory is same as the directory of the program, then the database is not selected
    if os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
        print("!Failed to alter table " + table_name +
              " because no database is selected.")
        return
    # check if the table exists, open the file and print the contents.
    if os.path.exists(table_name):
        file = open(table_name, "r")
        print(file.read())
        file.close()
    # if the table does not exist, print an error message
    else:
        print("!Failed to query table " + table_name +
              " because it does not exist.")


#calls the main function
if __name__ == "__main__":
    main()
