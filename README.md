# sheets-to-sql
Creates SQL tables out of copied google sheets cells for those like me that are, for some strange reason, better at using SQL than google sheets. This program can also be applied to other copied tables (outside of google sheets) as well. Usage should be self-explanatory, as the program, once run in a computer's terminal, will prompt the user as to what steps should be taken to complete the table creation, however, more detailed instructions are provided below:

  Upon running the program, the user will first be prompted for a database name. Do not include the file extension when typing in the name of the database; the file extension '.sqlite3' will automatically be added. Typing in the name of a database that already exists within the folder that the program is stored (or typing in the relative file path of a database that is stored in another folder) will open up that pre-existing database, otherwise, a new database with the input name will be created.
  
   Next, the program will ask the user to copy the cells of the google sheet/table that they want to turn into an SQL table. Do not input the copied cells into the program; simply hit enter when the cells have been properly copied. No inputting is required because the program will access the value currently stored in your clipboard to make the table. Be mindful that the cells that are copied could form a valid SQL table, as if the copied cells don't match SQL syntax, the program could throw errors or form the table incorrectly. The program will automatically turn invalid column names into valid column names by replacing invalid characters (such as spaces) with underscores, has the ability to "rotate" the input cells 90º such that the row headers become column headers (all other cells are similarly "rotated"), and has a few options for determining data types for each column, but errors that cannot be corrected by these tools will be problematic. Hit return to continue.
   
   Then, the program will ask if the table should be flipped. Answering with y will activate the table "rotating" tool described in the above paragraph. Answering n will keep the inputted cells unchanged in this regard.
   
   Next, the program will ask if it should determine and assign datatypes for each column of the table. Answering y will allow the program to assign datatypes to each column based on the types of data in the first row of each column. It's important to note that if there are varying data types in a single column, this is likely to cause errors as that would result in an invlaid SQL table. Answering y will also result in a follow up prompt asking if REAL should be preferred over INT. Answering y will cause any column that would have been assigned the data type INTEGER to be assigned the data type REAL. This prompt should really only be answered with y if both numbers with decimal points and integers both appear in any singular column, as this will help avoid errors. For simplicity's sake, columns will only be assigned the data types INTEGER, REAL, or TEXT. Answering n to the first prompt will default the data type of all columns to TEXT. The program will then print the name and data type of each column for clarity.
   
   Finally, the program will print out the created table and terminate. The printed table will be in the form of a list of tuples, which is the way that Python reads SQL tables. The first tuple will be all of the column headers and the consecutive tuples will be the consecutive rows in the table. With the table created, the database that it was created in can be opened up and the table can be manipulated as usual with SQL queries.
   
   Enjoy!

NOTE: Python modules pyperclip and sqlite3 must be downloaded before usage. These modules can be downloaded by visiting their respective websites and following the instructions there on how to proceed to download them. 
