# Databuild Version 2.0
# =======================

The databuild application has been rebuilt to use two of the most widely used 
programming and database languages: Python and MySQL. It takes advantage of
python's wide array of libraries to connect to remote databases, create a UI
and format queries in SQL for the database. 

## Libraries
## =========

Urllib2 -> A python library used for making REST requests and reading data 

csv -> A python library for reading and writing from CSV flat files. Used to 
convert legacy files to MySQL

Tkinter -> A python library for creating GUI elements

ttk -> A python GUI library for displaying tables, using Treeview.

tkMessageBox -> A python library for displaying message boxes

MySQLdb -> A python library for connecting, reading and querying MySQL databases

logging -> A python library for creating application logs.

Also, Databuild 2.0 requires access to a valid MySQL instance, hosted locally,
or on a remote server. 

## Summary
## =======

At it's core, the Databuild 2.0 application is a Database CRUD application, 
allowing the user to Create, Read, Update and Delete databases, tables and rows.
This includes the ability to write files as CSV flat files, and read the legacy
Databuild flat files, convert them to Python objects and insert them into MySQL
tables, providing a means of upgrading for existing customers.


## Application Design
## ==================


The design of the Databuild 2.0 application is influenced by the Tkinter library
used to create the GUI. The databuild class inherits from the Tkinter.Frame 
class, and uses layout methods like .pack() and .grid() to arrange it's
elements. Upon running the class, the python code initializes and a operating
system specific window frame (Linux, Windows and Mac), and calls the 
Databuild constructor __init__(). This constructor initializes logging, creates 
class variables that will store and pass data, opens the initial connection to
the default MySQL server, creates the initial GUI elements, and populates the
display with data. Once these tasks are complete, the user can insert and delete
rows, columns and tables. The user can also switch between tables ('Master 
Files' in the old databuild app) and view the tables layout and relationships.

If a new or remote database is desired, the user can open a connection and 
provide the connection info. Throughout the whole application lifecycle, 
a python logging class logs errors, exceptions, and important events. This log
is stored as databuild.log in the same directory as the .py files. The class 
file itself is well documented, with each python method using a docstring.

The main application frame acts as the parent, with dialog windows as child
Tk.Toplevel objects. 

                         Main Frame
                    /        |           \
        Dialog Window   Dialog Window   Dialog Window

The application sits in the Tk.Tk() mainloop, listening for input, until a user
gives a command through the GUI. Once an action involving SQL has been 
requested, the Databuild class uses the connection through the MySQLdb connector
to execute the SQL query against the database.


## Application Flow
## ================
The application initializes with the main method, creating the Databuild class
which inherits from Tk.Frame and acts as the main view and application 
controller. Init methods are then called to populate class variables, create 
the menus on the frame, open a connection to the default database, and populate 
the initial data on the main screen. Actions via the main frame menus open child
dialogs of the Databuild class, which pass data back to the main class once 
their action executes. The main databuild class then interprets this input
into SQL queries, and executes them against the connected database. 


## Execution
## =========

To execute the application, simply call

python databuild.py 

from the commandline, with python 2.x installed.


## Functions
## =========

A description of the functions, their arguments and return values are listed
below.

'''
    def execute_command(self, sql):
        """Execute a MySQL command upon the database.
        Args: sql -> The SQL statement to be executed.
        Rets: Returns all rows of the query as a list of tuples.
        """

    def export_file(self, filename='databuild.csv'):
        """Export a database table to a csv flat file.
        Args: filename->filename to write to.
        Rets: None
        """

    def import_file(self, filename='databuild.csv', table='temp_table'):
        """Import a file from CSV and create a table with the data.
        Args: filename->filename to read from
              table-> name of the table to create.
        Rets: None
        """

    def init_connection(self):
        """Initialize the MySQL database connection.
        Args: None
        Rets: None
        """

    def init_data(self):
        """Initialize the class variables.
        Args: None
        Rets: None
        """

    def init_ui(self):
        """Initialize the application GUI elements.
        Args: None
        Rets: None
        """

    def init_display(self):
        """Load the main UI elements.
        Args: None
        Rets: None
        """

    def open_connection(self, host='localhost', user='root',
                        password='passw0rd', database='databuild'):
        """Tries to open a connection to a MySQL database. Sets the class
        connection parameters.
        Args: host -> The host of the MySQL database. Default is 'localhost'
              user -> The user for the MySQL database. Default is 'user'
              password -> Password for user on the host. Default is 'passw0rd'
              database -> The database to connect to. Default is 'databuild'
        Rets: None
        """

    def close_connection(self):
        """Disconnect from the MySQL database.
        Args: None
        Rets: None
        """

    def open_new_connection(self, host='localhost', user='root',
                        password='passw0rd', database='databuild'):
        """Open a new connection and display a message box if successful.
        Args: host-> IP address of the host for the database
              user-> The user for the MySQL database
              password-> The password for the MySQL database
              database-> The default database in MySQL
        Rets: None
        """

    def init_ui_menus(self):
        """Initialize the menus for the GUI.
        Args: None
        Rets: None
        """

    def init_ui_file_menu(self):
        """Initialize the menu for application commands.
        Args: None
        Rets: None
        """

    def init_ui_connection_menu(self):
        """Initialize menu for viewing opening and closing database connections.
        Args: None
        Rets: None
        """

    def init_ui_relationships_menu(self):
        """Initialize the menu for viewing database relationships.
        Args: None
        Rets: None
        """

    def init_ui_insert_menu(self):
        """Initialize the menu for inserting rows, columns, and tables.
        Args: None
        Rets: None
        """

    def init_ui_update_menu(self):
        """Initialize the menu for updating rows, columns, and tables.
        Args: None
        Rets: None
        """

    def init_ui_view_menu(self):
        """Initialize the menu for viewing application logs.
        Args: None
        Rets: None
        """

    def init_ui_delete_menu(self):
        """Initialize the menu for deleting rows, columns, and tables.
        Args: None
        Rets: None
        """

    def init_ui_generate_menu(self):
        """Initialize the generate menu for importing and exporting files.
        Args: None
        Rets: None
        """

    def init_ui_help_menu(self):
        """Initialize the help menu.
        Args: None
        Rets: None
        """

    def open_connection_dialog(self):
        """Create a dialog to open a connection to a database.
        Args: None
        Rets: None
        """

    def view_connection_info_dialog(self):
        """Create a dialog to display the connection info.
        Args: None
        Rets: None
        """

    def insert_row_dialog(self):
        """Create a dialog to insert rows into the current table.
        Args: None
        Rets: None
        """

    def insert_column_dialog(self):
        """Create a dialog to insert a column into the current table.
        Args: None
        Rets: None
        """

    def insert_table_dialog(self):
        """Create a dialog to insert a table into the database.
        Args: None
        Rets: None
        """

    def update_row_dialog(self):
        """Create a dialog to update a row in the current table.
        Args: None
        Rets: None
        """

    def update_column_dialog(self):
        """Create a dialog to update a column in the current table.
        Args: None
        Rets: None
        """

    def delete_row_dialog(self):
        """Create a dialog to delete a row in the current table.
        Args: None
        Rets: None
        """

    def delete_column_dialog(self):
        """Create a dialog to delete a column in the current table.
        Args: None
        Rets: None
        """

    def help_menu_dialog(self):
        """Create a dialog to show a help menu with application documentation
        Args: None
        Rets: None
        """

    def app_info_dialog(self):
        """Create a dialog to show application info.
        Args: None
        Rets: None
        """

    def view_relationships_dialog(self):
        """Create a dialog box that describes the column layout.
        Args: None
        Rets: None
        """

    def describe_table_dialog(self):
        """Create a dialog box that describes the table layout.
        Args: None
        Rets: None
        """

    def populate_table_dropdown(self):
        """Fill the dropdown selection with tables from the current database
        Args: None
        Rets: None
        """

    def populate_display(self):
        """Populate the display Treeview with the column names and row data
        Args: None
        Rets: None"""

    def get_current_row(self, instance):
        """Get the currently selected row in the display Treeview
        Args: instance -> The treeview instance
        Rets: None
        """

    def delete_current_row(self):
        """Delete the currently selected row from the table.
        Args: None
        Rets: None
        """

    def select_table(self, table):
        """Set the current table to table.
        Args: table-> The MySQL table to view and manipulate
        Rets: None
        """

    def select_database(self, database='databuild'):
        """Select which database to use from the MySQL instance
        Args: database -> The database to use in the instance
        Rets: None
        """

    def show_databases(self):
        """Show which databases are available.
        Args: None
        Rets: None
        """

    def insert_database(self, database):
        """Create a new database in the MySQL instance
        Args: database-> Name of the database to create
        Rets: Result of the SQL query
        """

    def use_database(self, database='databuild'):
        """Select a database to use.
        Args: database-> The database to use
        Rets: None
        """

    def drop_database(self, database):
        """Delete a database from the MySQL instance
        Args: database-> The database to delete
        Rets: The outputs of the SQL query
        """

    def show_tables(self):
        """Show available tables in the MySQL database
        Args: None
        Rets: Output from the MySQL query
        """

    def insert_table(self, table):
        """Create a new table in the database.
        Args: table-> name of the table to be created
        Rets: Output from the MySQL query
        """

    def describe_table(self, table):
        """Display the table columns and their types.
        Args: table-> table to display
        Rets: Output of the SQL query
        """

    def show_column_relationships(self, table):
        """Display the relationships between columns in a table.
        Args: table-> The table to display the relationships from
        Rets: Output from the SQL query.
        """

    def flatten_nested_hierarchy(self, hierarchy):
        """Flatten the hiearchy into a single list.
        Args: hierarchy-> The nested lists to be flattened
        Rets: The list containing the flattened hierarchy
        """

    def select_rows(self, table, where=''):
        """Select * rows from table, with where clause.
        Args: table-> Name of the table to select from
              where-> Where clause for the SQL query
        Rets: Output of the SQL query
        """

    def insert_row(self, table, values):
        """Insert records into a table.
        Args: table-> Name of the table to insert a row into
        Rets: Output of the SQL query
        """

    def get_column_names(self, table):
        """Get the column names for the specified table.
        Args: table-> Table to get the column names from
        Rets: Output of the SQL query
        """

    def get_column_cursor_names(self):
        """Get the column names using the cursor in the MySQLdb connector
        Args: None
        Rets: None
        """

    def update_row(self, table, values):
        """Update records in a table.
        Args: table-> Table to update values in
              values-> Values to update in the table
        Rets: Output of the SQL query
        """

    def delete_row(self, table, where):
        """Delete a row from the table.
        Args: table-> Table to delete a row from
              column_name-> Column to compare where clause against
              value-> value to match against the column
        Rets: Output of the SQL query
        """

    def insert_column(self, table, column_name, column_type):
        """Add a column to a table
        Args: table->Table name to add a column to
              column_name->Name of the column to be added
              column_type->Type of the column to be added
        Rets: Output of the SQL query
        """

    def delete_column(self, table, column_name):
        """Delete a column from a table
        Args: table-> Table to delete the column from
              column_name-> Name of the column to delete
        Rets: Output of the SQL statement
        """

    def view_log_dialog(self):
        """Create a dialog box to display the application log file
        Args: None
        Rets: None
        """
'''


## Classes
## =======
Classes used in the Databuild application

'''
    class Databuild(Tk.Frame)
    class OpenConnectionDialog(Tk.Toplevel)
    class InsertRowDialog(Tk.Toplevel)
    class InsertColumnDialog(Tk.Toplevel)
    class UpdateRowDialog(Tk.Toplevel)
    class UpdateColumnDialog(Tk.Toplevel)
    class DeleteRowDialog(Tk.Toplevel)
    class DeleteColumnDialog(Tk.Toplevel)
    class DeleteTableDialog(Tk.Toplevel)
    class DescribeTableDialog(Tk.Toplevel)
    class ColumnRelationshipsDialog(Tk.Toplevel)
    class ViewLogDialog(Tk.Toplevel)
    class ConnectionInfoDialog(Tk.Toplevel)
    class HelpMenuDialog(Tk.Toplevel)
    class AppInfoDialog(Tk.Toplevel)
'''
