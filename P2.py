#Author: Yeamin Chowdhury
#Date: 04/03/2023
#Description: This program is a database management system that can create, delete, and modify databases and tables. It can also insert, delete, and update records in the tables. It can also select records from the tables based on the given conditions.
#Project: CS - 457 - 02


# import the os and shutil modules
import os
import shutil

# main function that takes input from the user and calls the command function. If the user enters .exit, the program exits
def main():
    try:
        while True:
            # take input from the user
            # if the user enters .exit, the program exits
            #takes 3 lines of input
            #if a line contains a semicolon, it will add the line to the input_command string and break the loop
            c = 0
            input_command = ''
            while True:
                com_line = input()
                c += 1
                input_command += com_line + ' '
                if com_line.endswith(';') or c == 3:
                    break
                if com_line == '.exit':
                    print("All done.")
                    exit()


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
        elif len(parsed_command) == 2 and parsed_command[0] == "USE":
            use_database(parsed_command[1])
        elif parsed_command[0] == "CREATE" and parsed_command[1] == "TABLE":
            variables_list = input[input.find("(") + 1:input.find(";") - 1]
            variable_list = variables_list.split(", ")
            print(variable_list)
            create_table(parsed_command[2], variable_list)
        elif parsed_command[0] == "SELECT" and parsed_command[1] == "*" and (len(parsed_command) == 4):
            select_table(parsed_command[3])
        elif parsed_command[0] == "INSERT" and parsed_command[1] == "INTO":
            v_list = input.split("(")[1]
            var_list = v_list[0: v_list.find(")")]
            
            final_list = var_list.split(", ")
            for i in range(0, len(final_list)):
                final_list[i] = final_list[i].strip()
            insert_into(parsed_command[2], final_list)
        elif parsed_command[0] == "DELETE" and parsed_command[1] == "FROM":
            delete_from(parsed_command[2], parsed_command[4], parsed_command[5], parsed_command[6])
        elif parsed_command[0] == "UPDATE" and parsed_command[2] == "SET":
            update_table(parsed_command[1], parsed_command[3], parsed_command[7], parsed_command[8], parsed_command[9], parsed_command[5])
        elif parsed_command[0] == "SELECT" and parsed_command[1] != "*":
            att_count = 0
            for each in parsed_command:
                if each.endswith(","):
                    att_count += 1
            attribute_list = []
            for i in range(0, att_count + 1):
                attribute_list.append(parsed_command[1 + i].strip(","))

            t_name = parsed_command[att_count + 3]
            o_att = parsed_command[att_count + 5]
            o = parsed_command[att_count + 6]
            o_val = parsed_command[att_count + 7]
            select_set(t_name, attribute_list, o_att, o, o_val)
            
        else:
            print("Invalid command")

    #if there is not enough amount of armuents in the command, print Insufficient command arguments
    except IndexError:
        print("Insufficient command arguments")

#this function displays a database record that matches the given conditions
def select_set(table_name, attribute_name, operator_att, operator, operator_value):
    # if current directory is same as the directory of the program, then the database is not selected
    if os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
        print("!Failed to select values from " + table_name +
              " because no database is selected.")
        return
    # check if the table exists, open the file and print the contents.
    if os.path.exists(table_name):
        file = open(table_name, "r")
        #check if the attribute exists in the first line and if it does, get its index. Otherwise, print an error message
        first_line = file.readline()
        file.close()
        first_line_list = first_line.split(" | ")
        first_line_list_printer = first_line_list.copy()
        
        for i in range(0, len(first_line_list)):
            first_line_list[i] = first_line_list[i].split(" ")[0]


        #check if the attribute exists in the first line and if it does, get its index. Otherwise, print an error message
        #also check if the attributes from given command line exists in the first line and if it does, get its index. Otherwise, print an error message
        index_list = []
        for i in range(0, len(attribute_name)):
            if attribute_name[i] not in first_line_list:
                print("!Failed to select values from table " + table_name +
                      " because the attribute " + attribute_name[i] + " does not exist.")
                return

            else:
                index_list.append(first_line_list.index(attribute_name[i]))

            if operator_att not in first_line_list:
                print("!Failed to select values from table " + table_name +
                      " because the attribute " + operator_att + " does not exist.")
                return

            else:
                operator_index = first_line_list.index(operator_att)



       #read values and store them in a 2d list
        values = []
        file = open(table_name, "r")
        for line in file:
            line = line.strip().split(" | ")
            values.append(line)
        file.close()
        selected_values = values[1:]
        included_rows = []
        #call the set operation function to get the indexes of values that matches condition and store the returned value in a list
        included_rows = set_operation(values[1:], operator_index, operator, operator_value)
        
        #print the first line
        s = ''
        for each in index_list:
            s += first_line_list_printer[each] + " | "
        print(s.strip(" | "))
    
        #if the list is empty, print an error message and return
        if included_rows is None:
            print("No values satisfy the condition")
            return
        #print the values that match the condition
        for i in included_rows:
            row = ""
            for j in index_list:
                row += selected_values[i][j] + " | "
            print(row.strip(" | "))

    # if the table does not exist, print an error message
    else:
        print("!Failed to select values from table " + table_name +
              " because it does not exist.")


#this function updates a database record that matches the given conditions
## If the conditional segment of the commands contains invalid data types of values, then the function returns None
def set_operation(two_d_list, attribute_index, operator, operator_value):
    try:
        e_value_index = []
        if operator == "=":
            for i in two_d_list:
                if i[attribute_index] == operator_value:
                    e_value_index.append(two_d_list.index(i))
        elif operator == ">":
            if operator_value.isalpha():
                for i in two_d_list:
                    if i[attribute_index] > operator_value:
                        e_value_index.append(two_d_list.index(i))
            else:
                for i in two_d_list:
                    if float(i[attribute_index]) > float(operator_value):
                        e_value_index.append(two_d_list.index(i))
        elif operator == "!=":
            for i in two_d_list:
                if i[attribute_index] != operator_value:
                    e_value_index.append(two_d_list.index(i))

        return e_value_index
    except ValueError:
        print("Invalid type value")
        return
                



#this function inserts the values into a existing table, with existing schema
#if the number of values does not match the number of attributes, print an error message
def insert_into(table_name, value_list):
    # if current directory is same as the directory of the program, then the database is not selected
    if os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
        print("!Failed to insert values into " + table_name +
              " because no database is selected.")
        return
    # check if the table exists, open the file and print the contents.
    if os.path.exists(table_name):
        file = open(table_name, "r")
        #check if the attribute exists in the first line and if it does, get its index. Otherwise, print an error message
        first_line = file.readline()
        file.close()
        first_line_list = first_line.split(" | ")
        if len(value_list) != len(first_line_list):
            print("!Failed to insert values into table " + table_name +
              " because the number of values does not match the number of attributes.")
            return
        file = open(table_name, "a")
        file.write("\n" + " | ".join(value_list))
        file.close()
        print("1 new record inserted.")
    # if the table does not exist, print an error message
    else:
        print("!Failed to insert values into table " + table_name +
              " because it does not exist.")


#this function deletes the values from the table that match the condition given =, >,
def delete_from(table_name, attribute_name, operator, operator_value):
    

    # if current directory is same as the directory of the program, then the database is not selected
    if os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
        print("!Failed to delete values from " + table_name +
              " because no database is selected.")
        return
    # check if the table exists, open the file and print the contents.
    if os.path.exists(table_name):
        file = open(table_name, "r")
        #check if the attribute exists in the first line and if it does, get its index. Otherwise, print an error message
        first_line = file.readline()
        file.close()
        attribute_list = first_line.split(" | ")
        #find the name of the attribute without the type
        for i in range(0, len(attribute_list)):
            attr_type = attribute_list[i].split(" ")
            attribute_list[i] = attr_type[0]
            
        attribute_index = 0        
        #if the attribute does not exist, print an error message
        if attribute_name not in attribute_list:
            print("!Failed to delete values from table " + table_name +
              " because the attribute does not exist.")
        else:
            #find the index of the attribute asked to be deleted
            for each in attribute_list:
                if each == attribute_name:
                    attribute_index = attribute_list.index(each)
                    break
        #store the schema of the table and data in a 2d list
        file = open(table_name, "r")
        two_d_list = []
        for line in file:
            line_list = line.split(" | ")
            two_d_list.append(line_list)
        file.close()

        #get the length of the first element of the 2d list
        first_element = two_d_list[0]
        len_first_element = len(first_element)
        #remove the first element of the 2d list to maintain the attribute names
        two_d_list = two_d_list[1:]

        #iterate over the last element of the 2d list to remove the "\n" character
        for i in range(0, len(two_d_list)):
            two_d_list[i][len_first_element - 1] = two_d_list[i][len_first_element - 1].strip("\n")
        
        #count the number of values that was found before deletion
        before_deletion = len(two_d_list)
        #delete the values from the 2d list
        updated_two_d_list = delete_operation(operator, two_d_list, attribute_index, operator_value)
        #count the number of values that was found after deletion
        after_deletion = len(updated_two_d_list)
        #calculate the number of deleted values
        count_of_deleted_values = before_deletion - after_deletion

        if updated_two_d_list == None:
            print("No values matched the condition.")

        #print the two_d_list to the file from the beginning after attribute names
        file = open(table_name, "w")
        file.write(" | ".join(first_element))
        file = open(table_name, "a")
        for i in updated_two_d_list:
            joining_string = " | ".join(i) + "\n"
            file.write(joining_string)
        file.close()

        #print the number of deleted values
        if count_of_deleted_values <= 1:
            print(str(count_of_deleted_values) + " record deleted.")
        else:
            print(str(count_of_deleted_values) + " records deleted.")

    # if the table does not exist, print an error message
    else:
        print("!Failed to delete values from table " + table_name +
              " because it does not exist.")

#this function deletes the values from table that matches the condition given =, >
#If the conditional segment of the commands contains invalid data types of values, then the function returns None

def delete_operation(operator, two_d_list, attribute_index, operator_value):
    try:
        removed_list = []
        #for =, check if the value at the attribute index is equal to the operator value
        #if it is, then pass
        #if it is not, then append the list to the removed list
        if operator == "=":
            for i in two_d_list:
                if i[attribute_index] == operator_value:
                    pass
                else:
                    removed_list.append(i)
        #for >, check if the value at the attribute index is greater than the operator value
        #if it is, then pass
        #if it is not, then append the list to the removed list
        if operator == ">":
            for i in two_d_list:
                if operator_value.isalpha() == True:
                    if i[attribute_index] > operator_value:
                        pass
                    else:
                        removed_list.append(i)
                else:
                    if float(i[attribute_index]) > float(operator_value):
                        pass
                    else:
                        removed_list.append(i)
                

        #for "!=", check if the value at the attribute index is not equal to the operator value
        #if it is, then pass
        #if it is not, then append the list to the removed list
        elif operator == "!=":
            for i in two_d_list:
                if i[attribute_index] != operator_value:
                    pass
                else:
                    removed_list.append(i)


        return removed_list
    except:
        return None


#this function updates the values in the table
def update_table(table_name, set_name, attribute_name, operator, operator_value, new_value):
    # if current directory is same as the directory of the program, then the database is not selected
    if os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
        print("!Failed to update values in " + table_name +
              " because no database is selected.")
        return
    # check if the table exists, open the file and print the contents.
    if os.path.exists(table_name):
        file = open(table_name, "r")
        #check if the attribute exists in the first line and if it does, get its index. Otherwise, print an error message
        first_line = file.readline()
        file.close()
        attribute_list = first_line.split(" | ")
        for i in range(0, len(attribute_list)):
            attr_type = attribute_list[i].split(" ")
            attribute_list[i] = attr_type[0]

        if attribute_name not in attribute_list:
            print("!Failed to update values in table " + table_name +
              " because the attribute does not exist.")
            return

        if set_name not in attribute_list:
            print("!Failed to update values in table " + table_name +
              " because the set_attribute does not exist.")
            return
        attribute_index = attribute_list.index(attribute_name)
        set_index = attribute_list.index(set_name)

        file = open(table_name, "r")
        two_d_list = []
        for line in file:
            two_d_list.append(line.split(" | "))
        file.close()

        #get the length of the first element of the 2d list
        first_element = two_d_list[0]
        len_first_element = len(first_element)
        #remove the first element of the 2d list to maintain the attribute names
        two_d_list = two_d_list[1:]

       #iterate over the last element of the 2d list to remove the "\n" character
        for i in range(0, len(two_d_list)):
            two_d_list[i][len_first_element - 1] = two_d_list[i][len_first_element - 1].strip("\n")
        
        #update the values in the 2d list
        updated_two_d_list, update_count = update_operation(operator, two_d_list, attribute_index, set_index, operator_value, new_value)
        

        if updated_two_d_list == None:
            print("No value matched the condition.")
            return

        
        #open the file and write the updated values
        file = open(table_name, "w")
        file.write(" | ".join(first_element))
        file = open(table_name, "a")
        for i in updated_two_d_list:
            joining_string = " | ".join(i) + "\n"
            file.write(joining_string)
        file.close()
        if update_count <= 1:
            print(str(update_count) + " record modified.")
        else:   
            print(str(update_count) + " record modified.")
    # if the table does not exist, print an error message
    else:
        print("!Failed to update values in table " + table_name +
              " because it does not exist.")
 
    
#this function updates the values in the table that matches the condition given =, > and !=, and returns the updated 2d list with the count of the number of values updated
# If the conditional segment of the commands contains invalid data types of values, then the function returns None
def update_operation(operator, two_d_list, attribute_index, set_index, operator_value, new_value):
    try:
        updated_list = []
        count = 0
        if operator == "=":
            for i in two_d_list:
                if i[attribute_index] == operator_value:
                    i[set_index] = new_value
                    updated_list.append(i)
                    count += 1
                else:
                    updated_list.append(i)
        elif operator == ">":
            if operator_value.isalpha() == True:
                for i in two_d_list:
                    if i[attribute_index] > operator_value:
                        i[set_index] = new_value
                        updated_list.append(i)
                        count += 1
                    else:
                        updated_list.append(i)
            else:
                for i in two_d_list:
                    if float(i[attribute_index]) > float(operator_value):
                        i[set_index] = new_value
                        updated_list.append(i)
                        count += 1
                    else:
                        updated_list.append(i)
        elif operator == "!=":
            for i in two_d_list:
                if i[attribute_index] != operator_value:
                    i[set_index] = new_value
                    updated_list.append(i)
                    count += 1
                else:
                    updated_list.append(i)
        
        return updated_list, count
    except:
        return None, None

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
