import mysql.connector
from mysql.connector import errorcode
import csv
import os
###################################################################
#####   Earmyas Measho Gebre (eg223di ) #####
###################################################################                
database_name = "Gebre"  ## we assign the databse name
path= os.getcwd() + '\data_files'
print(path)


# first try if the database is already exis 
try:
    cnx = mysql.connector.connect( user = 'root',
          password = 'root' , 
          host = '127.0.0.1', 
          database=database_name)
except mysql.connector.Error as e:  
    database = input("the request4ed Database "+ database_name + " does not exist, do you want to create it?(Y/N): ") # If it does not exist, the system will asks the user if he/she wants to create one
    if database == "Y" or database == "y":
        # Query for creating planate table
        create_planets_table = "CREATE TABLE planets (name VARCHAR(255) NOT NULL,rotation_period INT,orbital_period INT,diameter INT, climate nvarchar(20),gravity nvarchar(20),terrain nvarchar(255),surface_water INT,population INT,primary key(name));"
        create_species_table = "CREATE TABLE species (name VARCHAR(255) NOT NULL,classification nvarchar(50),designation nvarchar(50),average_height INT,skin_colors nvarchar(50),hair_colors nvarchar(50),eye_colors nvarchar(50),average_lifespan INT,language nvarchar(50),homeworld nvarchar(50),primary key(name));"

        # Connecting to mamp, creating a database if the user wants and creating tables for 
        # both planets and species 
        cnx = mysql.connector.connect(user = 'root', password = 'root', host = '127.0.0.1')
        e = cnx.cursor()
        e.execute("create database "+ database_name + ";")
        e.execute("use the database" + database_name + ";")
        e.execute(create_planets_table)
        e.execute(create_species_table)
        e.execute('SET Global sql_mode ="";')
        e.execute('Set session sql_mode ="";')
        file = open(path+'\planets.csv')    # Opening planets.csv
        # Reading the file 
        csv_data = csv.reader(file)
        skipHeader = True
        for ele in csv_data:
            if skipHeader:
                skipHeader = False
                continue
            # Inserting the data in planets.csv into the databasse
            e.execute('Insert into planets(name, rotation_period,orbital_period, diameter, climate, gravity, terrain, surface_water, population)' 'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)', ele)
            e.execute("commit;")

        # Opening species.csv    
        file = open(path+'\species.csv') 
        skipHeader = True
        # Reading the file
        csv_data2 = csv.reader(file)
        for ele in csv_data2:
            if skipHeader:
                skipHeader = False
                continue
            # Inserting the data in species.csv into the databasse
            e.execute('Insert into species(name, classification, designation, average_height, skin_colors, hair_colors, eye_colors, average_lifespan, language, homeworld)' 'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', ele)
            e.execute("commit;")
            
    else:
        # Exits if the user doesn't want to create a database
        print("Database "+ database_name + " not created!")
        raise SystemExit
if cnx.is_connected():
    print("Database", database_name, "is connected and data has been inserted into it.")
    # Shows the menu
    while True:
        
        user_input = input("Press 1 to List all planets.\n"+
        "Press 2 to Search for planet details.\n"+
        "Press 3 to Search for species with height higher than given number.\n"+
        "Press 4 to know the most likely desired climate of the given species?\n"+
        "Press 5 to know the average lifespan per species classification?\n"+
        "Press 0 to exit\n")
       ## Answering question 1 is listing all planets
        if user_input == "1":  ## Answering question 1 is listing all planets
            x = cnx.cursor()
            x.execute("select name from planets;")
            for i in x:
                print(i)
            input()
        elif user_input == "2":  # Answering question 2 Search for planet details.
            planet_name = input("Enter name of the planet: ")
            y = cnx.cursor()
            y.execute("select * from planets where name="+"'"+planet_name+"'"+";")
            for j in y:
                print(j, end="")
            input("Hit any key to go to the main menu")
        elif user_input == "3": # Answering question 3 Search for species with height higher than given number.
            height = int(input("Height of the species: "))
            z = cnx.cursor()
            z.execute("select * from species where average_height > " +str(height)+";")
            for x in z:
                print(x)
            input()
       
        elif user_input == "4":   # Answering question 4 What is the most likely desired climate of the given species?
            species_name = input("please Enter the name of the species: ")   #
            a = cnx.cursor()
            a.execute("select climate from planets where name in (select homeworld from species where name="+"'"+species_name+"'"+");")
            for i in a:
                print(i)
            input("Hit any key to go to the main menu")
        #Answering question 5 search for the average lifespan per species classification?
        elif user_input == "5":  
            b = cnx.cursor()
            b.execute("select classification,average_lifespan from species;")
            print("Species name | Average lifespan")
            for y in b:
                print(y)
            input("press any key to go to the main menu")
        # If the input is Q,then exit
        elif user_input == "Q":
            cnx.close()
            break




    


