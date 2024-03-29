#Author: Yeamin Chowdhury
#Date: 05/15/2023
#Description: Transaction with lock

# import the os and shutil modules
# os module provides functions for interacting with the operating system
# shutil module provides functions for copying files, as well as entire folders.
# fileinput module provides functions to iterate over standard input or a list of files.

import os
import shutil
from fileinput import filename, close
 
home = os.getcwd()
transaction = False
table_name_global = ''
table_header_global = []
data_global = []
counter_global = 0




def main():
    try:
        while True:
            c = 0
            input_command = ''
            while True:
                com_line = input().rstrip()
                c += 1
                input_command += com_line + ' '
                input_command = input_command.upper()
                if com_line.endswith(';') or c == 3 or  com_line == '':
                    break
                if com_line == '.exit' or com_line == '.EXIT':
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
            parsed_command[2] = parsed_command[2].split("(")[0]
            create_table(parsed_command[2], variable_list)
        elif parsed_command[0] == "SELECT" and parsed_command[1] == "*" and (len(parsed_command) == 4):
            select_table(parsed_command[3])
        elif parsed_command[0] == "INSERT" and parsed_command[1] == "INTO":
            v_list = input.split("(")[1]
            var_list = v_list[0: v_list.find(")")]
            
            final_list = var_list.split(",")
            for i in range(0, len(final_list)):
                final_list[i] = final_list[i].strip()
            insert_into(parsed_command[2], final_list)

        #Update Employee SET name = 'John' WHERE id = 1;
        elif parsed_command[0] == "UPDATE" and parsed_command[2] == "SET":
            update_table(parsed_command[1], parsed_command[3], parsed_command[7], parsed_command[8], parsed_command[9], parsed_command[5])
        
        #select * from Employee E, Sales S where E.id = S.employeeID;
        elif parsed_command[0] == "SELECT" and parsed_command[1] == "*" and parsed_command[7] == "WHERE":
            #store the table_name_1 and table_name_2 in a dictionary
            table_dict = {parsed_command[3]: parsed_command[4], parsed_command[5]: parsed_command[6]}
            #store the attribute_name_1 and attribute_name_2 in a dictionary
            attr_1, attr_2 = parsed_command[8].split("."), parsed_command[10].split(".")
            attr_dict = {attr_1[1]: attr_1[0], attr_2[1]: attr_2[0]}
            #store the operator in a variable
            operator = parsed_command[9]
            select_join(table_dict, attr_dict, operator)

        #select * from Employee E inner join Sales S on E.id = S.employeeID;
        elif parsed_command[0] == "SELECT" and parsed_command[1] == "*" and parsed_command[5] == "INNER" and parsed_command[6] == "JOIN" and parsed_command[9] == "ON":
            #store the table_name_1 and table_name_2 in a dictionary
            table_dict = {parsed_command[3]: parsed_command[4], parsed_command[7]: parsed_command[8]}
            #store the attribute_name_1 and attribute_name_2 in a dictionary
            attr_1, attr_2 = parsed_command[10].split("."), parsed_command[12].split(".")
            attr_dict = {attr_1[1]: attr_1[0], attr_2[1]: attr_2[0]}
            #store the operator in a variable
            operator = parsed_command[11]
            select_join(table_dict, attr_dict, operator)
        #select * from Employee E left outer join Sales S on E.id = S.employeeID;
        elif parsed_command[0] == "SELECT" and parsed_command[1] == "*" and parsed_command[5] == "LEFT" and parsed_command[6] == "OUTER" and parsed_command[7] == "JOIN" and parsed_command[10] == "ON":
            #store the table_name_1 and table_name_2 in a dictionary
            table_dict = {parsed_command[3]: parsed_command[4], parsed_command[8]: parsed_command[9]}
            #store the attribute_name_1 and attribute_name_2 in a dictionary
            attr_1, attr_2 = parsed_command[11].split("."), parsed_command[13].split(".")
            attr_dict = {attr_1[1]: attr_1[0], attr_2[1]: attr_2[0]}
            #store the operator in a variable
            operator = parsed_command[12]
            select_join_outer_left(table_dict, attr_dict, operator)

        #begin transaction;
        elif parsed_command[0] == "BEGIN" and parsed_command[1] == "TRANSACTION":
            beginTransaction()

        #commit;
        elif parsed_command[0] == "COMMIT":
            commit()
            
        else:
            print("Invalid command")

    #if there is not enough amount of armuents in the command, print Insufficient command arguments
    except IndexError:
        print("Insufficient command arguments")


#write the updated values to the file or can write values to a existing file
def write_to_file(table_name, two_d_list, count, first_element):
    #open the file and write the updated values
        file = open(table_name, "w")
        file.write(" | ".join(first_element))
        file.write("\n")
        file = open(table_name, "a")
        for i in two_d_list:
            joining_string = " | ".join(i) + "\n"
            file.write(joining_string)
        file.close()
        if count <= 1:
            print(str(count) + " record modified.")
        else:   
            print(str(count) + " record modified.")

#begins a transaction by locking the table that was created 
def beginTransaction():
    global transaction
    
    if(os.path.exists(os.getcwd() + "/" + "locked")):
        transaction = False
        print("Transaction starts.")
        return
    transaction = True
    file = open('locked', "w")
    file.close()
    print("Transaction starts.")



#commits the transaction by unlocking the table that was created
def commit():
    global transaction, table_name_global, data_global, counter_global, table_header_global

    #if data_global is empty, then there is no transaction to commit
    if not data_global or not table_header_global or not table_name_global:
        print("No active transaction.")
        return  


    # If table already exists, print error message
    if(os.path.exists(os.getcwd() + "/" + "locked")):
        transaction = False
        os.remove(os.getcwd() + "/" + "locked")
        print("Transaction committed.")
        write_to_file(table_name_global, data_global, counter_global, table_header_global)
        table_header_global = []
        data_global = []
        counter_global = 0

        return
    
    return








#this function performs inner joins on the two tables
def select_join(t_dict, a_dict, operator):
    #if the current directory is the same as the directory of the program, then the database is not selected
    if os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
        print("!Failed to select values from " + t_dict[0] + " and " + t_dict[1] + " because no database is selected.")
        return
    #check if the tables exist, open the files and print the contents.
    table_names = list(t_dict.items())
    attributes_names = list(a_dict.items())
    if os.path.exists(table_names[0][0]) and os.path.exists(table_names[1][0]):
        file_1 = open(table_names[0][0], "r")
        file_2 = open(table_names[1][0], "r")
    else:
        #use table_names
        print("!Failed to select values from " + table_names[0][0] + " and " + table_names[1][0] + " because one or more of the tables do not exist.")
        return
    

    #check if the attributes exist in the first line and if they do, get their indices. Otherwise, print an error message    
    first_line_1 = file_1.readline()
    first_line_2 = file_2.readline()
    file_1_items, file_2_items = [], []
    #read each line of the file, strip the newline character and split the line into a list by the delimiter " | "
    for line_1, line_2 in zip(file_1, file_2):
        file_1_items.append(line_1.strip("\n").split(" | "))
        file_2_items.append(line_2.strip("\n").split(" | ")) 
    file_1.close()
    file_2.close()


    first_line_list_1 = first_line_1.strip("\n").split(" | ")
    first_line_list_2 = first_line_2.strip("\n").split(" | ")
    first_line_list_printer = first_line_list_1 + first_line_list_2

    #now make a cross product of the two files_items lists
    cross_products = cross_product(file_1_items, file_2_items)
            

    #now check if the attributes exist in the first line and if they do, get their indices. Otherwise, print an error message
    att_name_without_type = separate_attributes_from_types(first_line_list_printer)

    #check if the attributes exist in the first line and if they do, get their indices. Otherwise, print an error message
    if attributes_names[0][0] in att_name_without_type and attributes_names[1][0] in att_name_without_type:
        index_1 = att_name_without_type.index(attributes_names[0][0])
        index_2 = att_name_without_type.index(attributes_names[1][0])
    else:
        print("!Failed to select values from " + table_names[0][0] + " and " + table_names[1][0] + " because one or more of the attributes do not exist.")
        return


    #checks if the operator is valid, and if it is, then call the function that returns the indices of the records that match the condition
    if operator == "=":
        indices = []
        indices = indices_of_records_that_match_condition(cross_products, index_1, index_2, operator)
        
        #print the first line
        print(" | ".join(first_line_list_printer)) 
        #now print the records that match the condition
        for i in indices:
            print(" | ".join(cross_products[i]))

#this function performs outer left joins on the two tables
def select_join_outer_left(t_dict, a_dict, operator):
    #if the current directory is the same as the directory of the program, then the database is not selected
    if os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
        print("!Failed to select values from " + t_dict[0] + " and " + t_dict[1] + " because no database is selected.")
        return
    #check if the tables exist, open the files and print the contents.
    table_names = list(t_dict.items())
    attributes_names = list(a_dict.items())
    if os.path.exists(table_names[0][0]) and os.path.exists(table_names[1][0]):
        file_1 = open(table_names[0][0], "r")
        file_2 = open(table_names[1][0], "r")
    else:
        #use table_names
        print("!Failed to select values from " + table_names[0][0] + " and " + table_names[1][0] + " because one or more of the tables do not exist.")
        return
    

    #checks if the attributes exist in the first line and if they do, get their indices. Otherwise, print an error message    
    first_line_1 = file_1.readline()
    first_line_2 = file_2.readline()
    file_1_items, file_2_items = [], []
    #reads each line of the file, strip the newline character and split the line into a list by the delimiter " | "
    for line_1, line_2 in zip(file_1, file_2):
        file_1_items.append(line_1.strip("\n").split(" | "))
        file_2_items.append(line_2.strip("\n").split(" | ")) 
    file_1.close()
    file_2.close()


    first_line_list_1 = first_line_1.strip("\n").split(" | ")
    first_line_list_2 = first_line_2.strip("\n").split(" | ")
    first_line_list_printer = first_line_list_1 + first_line_list_2

    #makes a cross product of the two files_items lists
    cross_products = cross_product(file_1_items, file_2_items)
            

    #checks if the attributes exist in the first line and if they do, get their indices. Otherwise, print an error message
    att_name_without_type = separate_attributes_from_types(first_line_list_printer)

    #checks if the attributes exist in the first line and if they do, get their indices. Otherwise, print an error message
    if attributes_names[0][0] in att_name_without_type and attributes_names[1][0] in att_name_without_type:
        index_1 = att_name_without_type.index(attributes_names[0][0])
        index_2 = att_name_without_type.index(attributes_names[1][0])
    else:
        print("!Failed to select values from " + table_names[0][0] + " and " + table_names[1][0] + " because one or more of the attributes do not exist.")
        return


    #checks if the operator is valid, and if it is, then call the function that returns the indices of the records that match the condition
    if operator == "=":
        indices = []
        indices = indices_of_records_that_match_condition(cross_products, index_1, index_2, operator)
        #move element from cross_products to a new list if the index is in indices
        left_join_list = []
        for i in range(0, len(cross_products)):
            if i in indices:
                left_join_list.append(cross_products[i])

        len_2 = len(file_1_items[0])
        #perform union
        for item in file_1_items:
            found = False
            for i in left_join_list:
                if item[:len_2] == i[:len_2]:
                    found = True
                    break
            if not found:
                left_join_list.append(item)

        #fill all cells of a row that does not match the length of the first line witn "NULL"
        for i in range(0, len(left_join_list)):
            while len(left_join_list[i]) < len(first_line_list_printer):
                left_join_list[i].append("")


        
        #print the first line
        print(" | ".join(first_line_list_printer)) 
        #print the rest of the elements
        for item in left_join_list:
            print(" | ".join(item))

#this function takes two lists and returns a cross product of the two lists
def cross_product(list_1, list_2):
    cross_product = []
    for each_1 in list_1:
        for each_2 in list_2:
            cross_product.append(each_1 + each_2)
    return cross_product

#this function takes a list of attributes and returns a list of attributes without the type
def separate_attributes_from_types(attributes):
    attributes_without_type = []
    for each in attributes:
        attributes_without_type.append(each.split(" ")[0])
    return attributes_without_type

#this function takes a cross product, the indices of the attributes to be compared, and the operator and returns a list of indices of the records that match the condition
def indices_of_records_that_match_condition(cross_product, index_1, index_2, operator):
    indices = []
    for i in range(0, len(cross_product)):
        if operator == "=":
            if cross_product[i][index_1] == cross_product[i][index_2]:
                indices.append(i)
    return indices




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


#this function updates the values in the table
def update_table(table_name, set_name, attribute_name, operator, operator_value, new_value):
    # if current directory is same as the directory of the program, then the database is not selected
    if os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
        print("!Failed to update values in " + table_name +
              " because no database is selected.")
        return

    if (transaction == False):
        print("Error: Table " + table_name + " is locked!")
        print("Transaction abort.")
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
        
        if (transaction == True):
            global table_name_global, data_global, counter_global
            table_name_global = table_name
            data_global = updated_two_d_list
            counter_global = update_count
            #copy the element of first_element to table_header_global
            for i in range(0, len(first_element)):
                table_header_global.append(first_element[i].strip("\n"))
            print("Now commit the transaction.")

        if updated_two_d_list == None:
            print("No value matched the condition.")
            return

        
        
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
