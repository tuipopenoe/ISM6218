#!python2
# Tui Popenoe

import paramiko
import urllib2
import json
import Tkinter as Tk
import ttk
import tkMessageBox
import MySQLdb
import traceback
import logging

class Databuild(Tk.Frame):
    def __init__(self, parent):
        """Constructor"""
        # Call the superclass __init__ method to initialize the Frame
        Tk.Frame.__init__(self, parent)
        # Initialize logging
        logging.basicConfig(filename='databuild.log', level=logging.INFO)
        # Set the parent Tkinter.Frame
        self.parent = parent
        # Set minimum size
        self.parent.minsize(width=640, height=480)
        # Initialize the class variables
        self.init_data()
        # Initialize the MySQL database connection
        self.init_connection()
        # Initialize the application GUI elements
        self.init_ui()
        # Initialize the data displayed in the GUI
        self.init_display()

################################################################################
#################### Execute Command ###########################################
################################################################################

    def execute_command(self, sql):
        """Execute a MySQL command upon the database.
        Args: sql -> The SQL statement to be executed.
        Rets: Returns all rows of the query as a list of tuples.
        """
        try:
            # Execute the sql command
            self.cursor.execute(sql)
            # Commit any changes to the db
            self.db.commit()
            # return query output as a list of tuples
            return self.cursor.fetchall()
        except Exception, ex:
            # If there is an error, rollback the changes
            self.db.rollback()
            logging.error(ex)
            traceback.print_exc()
            return None

################################################################################
#################### Init ######################################################
################################################################################

    def init_connection(self):
        """Initialize the MySQL database connection.
        Args: None
        Rets: None
        """
        try:
            self.open_connection()
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def init_data(self):
        """Initialize the class variables.
        Args: None
        Rets: None
        """
        try:
            ############################
            # Initialize Class Variables
            ############################
            # MySQL database variables
            self.db = None
            self.cursor = None
            # Connection Variables
            self.host = None
            self.user = None
            self.password = None
            self.database = None
            # Store data from queries
            self.data = None
            # Currently Selected Row, Column, Table
            self.current_table = None
            self.current_row = None
            self.current_column = None
            self.table = 'databuild'
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def init_ui(self):
        """Initialize the application GUI elements.
        Args: None
        Rets: None
        """
        # Set the title
        self.parent.title('Databuild 2.0')
        # Initialize the UI Menus
        self.init_ui_menus()
        # Initialize the main window display
        self.init_display()

    def init_display(self):
        """Load the UI dropdown list that displays the database tables.
        Args: None
        Rets: None
        """
        try:
            # Tables in the Database
            self.table_label = Tk.Label(self.parent, text='Current Table: ')\
                                        .grid(row=0, column=3, sticky=Tk.W+Tk.E)
            #TODO change this as data will be initialized
            self.tables_list = None
            # Data Display
            self.display = ttk.Treeview(self.parent)
            # Scrollbar
            yscroll = Tk.Scrollbar(command=self.display.yview,
                                   orient=Tk.VERTICAL)
            yscroll.grid(row=1, column=5, sticky='ns')
            # Initialize the displays with data
            self.populate_table_dropdown()
            self.populate_display()
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

################################################################################
#################### Connections ###############################################
################################################################################

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
        try:
            # Set class variables for future use
            self.host = host
            self.user = user
            self.password = password
            self.database = database
            # Sets the database object to the connected database
            self.db = MySQLdb.connect(self.host, self.user, self.password,
                                      self.database)
            # Sets the cursor for later access
            self.cursor = self.db.cursor()
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def close_connection(self):
        """Disconnect from the MySQL database.
        Args: None
        Rets: None
        """
        try:
            # Disconnect from the MySQL datab
            self.db.close()
            tkMessageBox.showinfo("", "Connection closed")
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def open_new_connection(self, host='localhost', user='root',
                        password='passw0rd', database='databuild'):
        """Open a new connection and display a message box if successful.
        Args: host-> IP address of the host for the database
              user-> The user for the MySQL database
              password-> The password for the MySQL database
              database-> The default database in MySQL
        Rets: None
        """
        try:
            # Open a new connection
            self.open_connection(host, user, password, database)
            # Populate the tables from the new database.
            self.populate_table_dropdown()
            # Display message if connection succesful.
            tkMessageBox.showinfo("", "Connection to database %s opened"
                                  % self.database)
        except Exception, ex:
            tk.MessageBox.showinfo("", "Failed to connect to %s database"
                                   % self.database)
            logging.error(ex)
            traceback.print_exc()

################################################################################
#################### Init Menus ################################################
################################################################################
    def init_ui_menus(self):
        """Initialize the menus for the GUI.
        Args: None
        Rets: None
        """
        try:
            # root menu bar object
            self.menu_bar = Tk.Menu(self.parent)
            # File Menu
            self.init_ui_file_menu()
            # Connection Menu
            self.init_ui_connection_menu()
            # Relationships Menu
            self.init_ui_relationships_menu()
            # Insert Menu
            self.init_ui_insert_menu()
            # Update Menu
            self.init_ui_update_menu()
            # View Menu
            self.init_ui_view_menu()
            # Delete Menu
            self.init_ui_delete_menu()
            # Help Menu
            self.init_ui_help_menu()
            # Set menu bar for root frame 
            self.parent.config(menu=self.menu_bar)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def init_ui_file_menu(self):
        """Initialize the menu for application commands.
        Args: None
        Rets: None
        """
        try:
            self.file_menu = Tk.Menu(self.menu_bar, tearoff=0)
            #TODO
            self.file_menu.add_separator()
            self.menu_bar.add_cascade(label='File',
                                      menu=self.file_menu)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def init_ui_connection_menu(self):
        """Initialize menu for viewing opening and closing database connections.
        Args: None
        Rets: None
        """
        try:
            # Connection Elements
            self.conn_menu = Tk.Menu(self.menu_bar, tearoff=0)
            self.conn_menu.add_command(label='Open Connection',
                                       command=self.open_connection_dialog)
            self.conn_menu.add_separator()
            self.conn_menu.add_command(label='Close Connection',
                                       command=self.close_connection)
            self.conn_menu.add_separator()
            self.conn_menu.add_command(label='View Connection Info',
                                       command=self.view_connection_info_dialog)
            self.menu_bar.add_cascade(label='Connections',
                                      menu=self.conn_menu)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def init_ui_relationships_menu(self):
        """Initialize the menu for viewing database relationships.
        Args: None
        Rets: None
        """
        try:
            self.rel_menu = Tk.Menu(self.menu_bar, tearoff=0)
            self.rel_menu.add_command(label='View Relationships',
                                      command=self.view_relationships_dialog)
            self.rel_menu.add_separator()
            self.rel_menu.add_command(label='Describe Table',
                                      command=self.describe_table_dialog)
            self.menu_bar.add_cascade(label='Relationships',
                                      menu=self.rel_menu)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def init_ui_insert_menu(self):
        """Initialize the menu for inserting rows, columns, and tables.
        Args: None
        Rets: None
        """
        try:
            self.insert_menu = Tk.Menu(self.menu_bar, tearoff=0)
            self.insert_menu.add_command(label='Insert Row',
                                         command=self.insert_row_dialog)
            self.insert_menu.add_separator()
            self.insert_menu.add_command(label='Insert Column',
                                         command=self.insert_column_dialog)
            self.menu_bar.add_cascade(label='Insert',
                                      menu=self.insert_menu)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def init_ui_update_menu(self):
        """Initialize the menu for updating rows, columns, and tables.
        Args: None
        Rets: None
        """
        try:
            self.update_menu = Tk.Menu(self.menu_bar, tearoff=0)
            self.update_menu.add_command(label='Update Row',
                                         command=self.update_row_dialog)
            self.update_menu.add_separator()
            self.update_menu.add_command(label='Update Column',
                                         command=self.update_column_dialog)
            self.menu_bar.add_cascade(label='Update',
                                      menu=self.update_menu)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def init_ui_view_menu(self):
        """Initialize the menu for viewing application logs.
        Args: None
        Rets: None
        """
        try:
            self.view_menu = Tk.Menu(self.menu_bar, tearoff=0)
            self.view_menu.add_command(label='View Log',
                                      command=self.view_log_dialog)
            self.view_menu.add_separator()
            self.menu_bar.add_cascade(label='View',
                                      menu=self.view_menu)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def init_ui_delete_menu(self):
        """Initialize the menu for deleting rows, columns, and tables.
        Args: None
        Rets: None
        """
        try:
            self.delete_menu = Tk.Menu(self.menu_bar, tearoff=0)
            self.delete_menu.add_command(label='Delete Row',
                                         command=self.delete_row_dialog)
            self.delete_menu.add_separator()
            self.delete_menu.add_command(label='Delete Column',
                                         command=self.delete_column_dialog)
            self.menu_bar.add_cascade(label='Delete', menu=self.delete_menu)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def init_ui_help_menu(self):
        """Initialize the help menu.
        Args: None
        Rets: None
        """
        try:
            self.help_menu = Tk.Menu(self.menu_bar, tearoff=0)
            self.help_menu.add_command(label='Help',
                                       command=self.help_menu_dialog)
            self.help_menu.add_separator()
            self.help_menu.add_command(label='Application Info',
                                       command=self.app_info_dialog)
            self.menu_bar.add_cascade(label='Help', menu=self.help_menu)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

################################################################################
#################### Open Dialogs ##############################################
################################################################################

    def open_connection_dialog(self):
        t = Tk.Toplevel(self)
        l_host = Tk.Label(t, text='Host: ').grid(row=0, column=0)
        e_host = Tk.Entry(t, justify=Tk.RIGHT).grid(row=0, column=1)
        l_user = Tk.Label(t, text='User: ').grid(row=1, column=0)
        e_user = Tk.Entry(t, justify=Tk.RIGHT).grid(row=1, column=1)
        l_pass = Tk.Label(t, text='Password: ').grid(row=2, column=0)
        e_pass = Tk.Entry(t, justify=Tk.RIGHT).grid(row=2, column=1)
        l_data = Tk.Label(t, text='Database: ').grid(row=3, column=0)
        e_data = Tk.Entry(t, justify=Tk.RIGHT).grid(row=3, column=1)

        def _open_connection():
            try:
                self.open_new_connection(e_host.get(),
                                         e_user.get(), 
                                         e_pass.get(),
                                         e_data.get())
            except:
                self.open_new_connection()
            t.destroy()

        b_conn = Tk.Button(t, text='Connect', command=_open_connection)\
                          .grid(row=4, column=0, columnspan=2)

    def view_connection_info_dialog(self):
        try:
            connection_info_dialog = ConnectionInfoDialog(self)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def insert_row_dialog(self):
        """Create a dialog to insert rows into a table.
        Args: None
        Rets: None
        """
        try:
            insert_row_dialog = InsertRowDialog(self)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def insert_column_dialog(self):
        try:
            insert_column_dialog = InsertColumnDialog(self)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def update_row_dialog(self):
        try:
            update_row_dialog = UpdateRowDialog(self)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def update_column_dialog(self):
        try:
            update_column_dialog = UpdateColumnDialog(self)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def delete_row_dialog(self):
        try:
            delete_row_dialog = DeleteRowDialog(self)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def delete_column_dialog(self):
        try:
            delete_column_dialog = DeleteColumnDialog(self)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def help_menu_dialog(self):
        try:
            help_menu_dialog = HelpMenuDialog(self)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def app_info_dialog(self):
        try:
            app_info_dialog = AppInfoDialog(self)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def view_relationships_dialog(self):
        """Create a dialog box that describes the column layout.
        Args: None
        Rets: None
        """
        try:
            column_relationship_dialog = ColumnRelationshipDialog(self)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def describe_table_dialog(self):
        """Create a dialog box that describes the table layout.
        Args: None
        Rets: None
        """
        try:
            describe_table_dialog = DescribeTableDialog(self)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

################################################################################
#################### Populate Display ##########################################
################################################################################

    def populate_table_dropdown(self):
        try:
            options = self.show_tables()
            var = Tk.StringVar()
            var.set(options[0])
            self.tables_list = Tk.OptionMenu(self.parent, 
                                             var,
                                             *options,
                                             command=self.select_table)\
                                                .grid(row=0,
                                                      column=4,
                                                      columnspan=2,
                                                      sticky=Tk.W+Tk.E)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def populate_display(self):
        """Populate the display listbox with the column names and row data
        Args: None
        Rets: None"""
        try:
            #self.display.delete(0, Tk.END)
            self.data = self.select_rows(self.table)
            list_columns = self.get_column_names(self.table)
            # Accept tuple of column names
            self.display['columns'] = list_columns

            for column in list_columns:
                self.display.column(column, width=70)
                self.display.heading(column, text=str(column).capitalize())
            for row in self.data:
                self.display.insert("", 0, text="", values=row)
            self.display.grid(row=1, column=4, sticky=Tk.W+Tk.E)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def select_cmd(self, selected):
        print('Selected items: %s' % selected)

################################################################################
#################### Select Data ###############################################
################################################################################

    def select_table(self, table):
        """Set the current table to table.
        Args: table-> The MySQL table to view and manipulate
        Rets: None
        """
        try:
            self.table = table[0]
            self.populate_display()
        except:
            traceback.print_exc()


    def select_database(self, database='databuild'):
        """Select which database to use from the MySQL instance
        Args: database -> The database to use in the instance
        Rets: None
        """
        try:
            # Close the existing connection
            self.db.close()
            self.open_connection(database=database)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

################################################################################
#################### SQL Queries ###############################################
################################################################################

    def show_databases(self):
        """Show which databases are available.
        Args: None
        Rets: None
        """
        try:
            sql = 'SHOW DATABASES;'
            return self.execute_command(sql)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def insert_database(self, database):
        """Create a new database in the MySQL instance
        Args: database-> Name of the database to create
        Rets: Result of the SQL query
        """
        try:
            sql = 'CREATE DATABASE %s%s' % (database, ';')
            return self.execute_command(sql)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def use_database(self, database='databuild'):
        """Select a database to use.
        Args: database-> The database to use
        Rets: None
        """
        try:
            sql = 'USE %s%s' % (database, ';')
            self.execute_command(sql)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def drop_database(self, database):
        """Delete a database from the MySQL instance
        Args: database-> The database to delete
        Rets: The outputs of the SQL query"""
        try:
            sql = 'DROP ' + database + ';'
            return self.execute_command(sql)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def show_tables(self):
        """Show available tables in the MySQL database
        Args: None
        Rets: Output from the MySQL query"""
        try:
            sql = 'SHOW tables;'
            return self.execute_command(sql)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def create_table(self, table):
        """Create a new table in the database.
        Args: table-> name of the table to be created
        Rets: Output from the MySQL query
        """
        try:
            sql = 'CREATE TABLE IF NOT EXISTS %s;' % table
            return self.execute_command(sql)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def describe_table(self, table):
        """Display table organization."""
        try:
            sql = 'DESCRIBE %s;' % table
            return self.execute_command(sql)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def show_column_relationships(self, table):
        """Display the relationships between columns in a table.
        Args: table-> The table to display the relationships from
        Rets: Output from the SQL query.
        """
        try:
            sql = 'SELECT * FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS;'
            return self.execute_command(sql)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def flatten_nested_hierarchy(self, hierarchy):
        """Flatten the hiearchy into a single list.
        Args: hierarchy-> The nested lists to be flattened
        Rets: The list containing the flattened hierarchy
        """
        try:
            return [element for tupl in hierarchy for element in tupl]
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def select_rows(self, table, where=''):
        """Select * rows from table, with where clause.
        Args: table-> Name of the table to select from
              where-> Where clause for the SQL query
        Rets: Output of the SQL query"""
        try:
            # Initialize the select statement
            sql = 'SELECT * FROM %s;' % table
            # If a where clause is present, add it to the end
            if where:
                sql = 'SELECT * FROM %s WHERE %s;' % (table, where)
            # return the values from the executed command
            return self.execute_command(sql)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()
            return None

    def insert_row(self, table, values):
        """Insert records into a table.
        Args: table-> Name of the table to insert a row into
        Rets: Output of the SQL query"""
        try:
            sql = 'INSERT INTO %s VALUES (%s);' % (table, values)
            logging.info(sql)
            self.execute_command(sql)
        except:
            logging.error('Failed to insert row')
            traceback.print_exc()

    def get_column_names(self, table):
        """Get the column names for the specified table.
        Args: table-> Table to get the column names from
        Rets: Output of the SQL query"""
        try:
            sql = 'SELECT column_name FROM information_schema.columns WHERE '\
                  'table_name="%s";' % table
            return self.execute_command(sql)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def update_row(self, table, values):
        """Update records in a table.
        Args: table-> Table to update values in
              values-> Values to update in the table
        Rets: Output of the SQL query"""
        try:
            sql = 'UPDATE %s %s;' % (table, values)
            return self.execute_command(sql)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def delete_row(self, table, column_name, value):
        """Delete a row from the table.
        Args: table-> Table to delete a row from
              column_name-> Column to compare where clause against
              value-> value to match against the column
        Rets: Output of the SQL query"""
        try:
            sql = 'DELETE FROM %S WHERE %s=%s;' % (table, column_name, value)
            return self.execute_command(sql)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def insert_column(self, table, column_name, column_type):
        """Add a column to a table
        Args: table->Table name to add a column to
              column_name->Name of the column to be added
              column_type->Type of the column to be added
        Rets: Output of the SQL query"""
        try:
            sql ='ALTER TABLE %s ADD %s %s;' % (table, column_name, column_type)
            return self.execute_command(sql)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def delete_column(self, table, column_name):
        """Delete a column from a table."""
        try:
            sql = 'ALTER TABLE %s DROP %s;' % (table, column_name)
            self.execute_command(sql)
        except:
            #TODO
            traceback.print_exc()

    def generate_output(self, data, filename='output', filetype='.csv'):
        """Write a table to a file."""
        try:
            with open(filename + filetype, 'w') as f:
                f.write(data)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def view_log_dialog(self):
        try:
            view_log_dialog = ViewLogDialog(self)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()


################################################################################
#################### Dialog Classes ############################################
################################################################################

class InsertRowDialog(Tk.Toplevel):
    """Dialog frame to insert rows into a table."""
    def __init__(self, parent):
        """Constructor"""
        Tk.Toplevel.__init__(self, parent)
        # Set a reference to the main databuild Frame
        self.parent = parent
        self.title('Insert Row')
        self.insert_row()

    def insert_row(self):
        """Insert a row into the parent table.
        Args: None
        Rets: None
        """
        try:
            column_names = list(self.parent.get_column_names(self.parent.table))
            entry = {}
            label = {}
            i = 0
            for name in column_names:
                e = Tk.Entry(self)
                e.grid(column=1, sticky=Tk.E)
                entry[name] = e
                lb = Tk.Label(self, text=name)
                lb.grid(row=i, column=0, sticky=Tk.W)
                label[name] = lb
                i += 1

            def _insert_row():
                values = []
                for name in column_names:
                    values.append(entry[name].get())
                values = ', '.join(map(lambda x: "'" + x + "'", values))
                self.parent.insert_row(self.parent.table, values)
                self.destroy()
                self.parent.populate_display()

            b_ins = Tk.Button(self,
                              text='Insert Row',
                              command=_insert_row)\
                             .grid(row=i+1, column=1, sticky=Tk.W+Tk.E)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

class InsertColumnDialog(Tk.Toplevel):
    """Dialog frame to insert columns into a table."""
    def __init__(self, parent):
        """Constructor"""
        Tk.Toplevel.__init__(self)
        # Set a reference to the main databuild Frame
        self.parent = parent
        self.title("Insert Column")
        self.insert_column()

    def insert_column(self):
        """Insert a column into the table
        Args: None
        Rets: None
        """
        try:
            lbl_name = Tk.Label(self, text='Enter a column name: ')
            lbl_name.grid(row=0, column=0, sticky=Tk.W+Tk.E)
            ent_name = Tk.Entry(self)
            ent_name.grid(row=0, column=1, sticky=Tk.W+Tk.E)
            lbl_type = Tk.Label(self, text='Enter a column type: ')
            lbl_type.grid(row=1, column=0, sticky=Tk.W+Tk.E)
            ent_type = Tk.Entry(self)
            ent_type.grid(row=1, column=1, sticky=Tk.W+Tk.E)

            def _insert_column():
                c_name = ent_name.get()
                c_type = ent_type.get()
                self.parent.insert_column(self.parent.table, c_name, c_type)
                self.destroy()
                self.parent.populate_display()
            b_ins = Tk.Button(self,
                              text='Insert Column',
                              command=_insert_column)\
                              .grid(row=2, column=1, sticky=Tk.W+Tk.E)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

class UpdateRowDialog(Tk.Toplevel):
    """Dialog frame to update rows into a table."""
    def __init__(self, parent):
        """Constructor"""
        Tk.Toplevel.__init__(self, parent)
        # Set a reference to the main databuild Frame
        self.parent = parent
        self.title('Update Row')
        self.update_row()

    def update_row(self):
        """Update a row into the parent table.
        Args: None
        Rets: None
        """
        try:
            column_names = list(self.parent.get_column_names(self.parent.table))
            entry = {}
            label = {}
            i = 0
            for name in column_names:
                e = Tk.Entry(self)
                e.grid(column=1, sticky=Tk.E)
                entry[name] = e
                lb = Tk.Label(self, text=name)
                lb.grid(row=i, column=0, sticky=Tk.W)
                label[name] = lb
                i += 1

            def _update_row():
                values = []
                for name in column_names:
                    values.append(entry[name].get())
                values = ', '.join(map(lambda x: "'" + x + "'", values))
                self.parent.update_row(self.parent.table, values)
                self.destroy()
                self.parent.populate_display()

            b_ins = Tk.Button(self,
                              text='Update Row',
                              command=_update_row)\
                             .grid(row=i+1, column=1, sticky=Tk.W+Tk.E)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

class UpdateColumnDialog(Tk.Toplevel):
    """Dialog frame to update columns into a table."""
    def __init__(self, parent):
        """Constructor"""
        Tk.Toplevel.__init__(self)
        # Set a reference to the main databuild Frame
        self.parent = parent
        self.title("Update Column")
        self.update_column()

    def update_column(self):
        """Insert a column into the table
        Args: None
        Rets: None
        """
        try:
            lbl_name = Tk.Label(self, text='Enter a column name: ')
            lbl_name.grid(row=0, column=0, sticky=Tk.W+Tk.E)
            ent_name = Tk.Entry(self)
            ent_name.grid(row=0, column=1, sticky=Tk.W+Tk.E)
            lbl_type = Tk.Label(self, text='Enter a column type: ')
            lbl_type.grid(row=1, column=0, sticky=Tk.W+Tk.E)
            ent_type = Tk.Entry(self)
            ent_type.grid(row=1, column=1, sticky=Tk.W+Tk.E)

            def _update_column():
                c_name = ent_name.get()
                c_type = ent_type.get()
                self.parent.update_column(self.parent.table, c_name, c_type)
                self.destroy()
                self.parent.populate_display()
            b_ins = Tk.Button(self,
                              text='Update Column',
                              command=_update_column)\
                              .grid(row=2, column=1, sticky=Tk.W+Tk.E)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

class DeleteRowDialog(Tk.Toplevel):
    """Dialog confirmation for deleting a row."""
    def __init__(self, parent):
        """Constructor"""
        Tk.Toplevel.__init__(self)
        self.parent = parent
        self.title('Delete Row')
        self.delete_row()

    def delete_row(self):
        """Delete a row from the table.
        Args: None
        Rets: None
        """
        try:
            lbl_confirm = Tk.Label(self, text='Confirm Delete Row?').pack()
            btn_cancel = Tk.Label(self, text='Cancel',
                                  command=self.destroy).pack
            btn_confirm = Tk.Button(self, text='Delete Row',
                                    command=_delete_row)

            def _delete_row():
                self.parent.delete_row(self.parent.current_row)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

class DeleteColumnDialog(Tk.Toplevel):
    """Dialog confirmation for deleting a column."""
    def __init__(self, parent):
        """Constructor"""
        Tk.Toplevel.__init__(self)
        self.parent = parent
        self.title('Delete column')
        self.delete_column()

    def delete_column(self):
        """Delete a column from the table.
        Args: None
        Rets: None
        """
        try:
            lbl_confirm = Tk.Label(self, text='Confirm Delete Column?').pack()
            btn_cancel = Tk.Label(self, text='Cancel',
                                  command=self.destroy).pack
            btn_confirm = Tk.Button(self, text='Delete Column',
                                    command=_delete_column)

            def _delete_column():
                self.parent.delete_column(self.parent.current_column)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

class DescribeTableDialog(Tk.Toplevel):
    """Dialog Frame displaying table properties."""
    def __init__(self, parent):
        """Constructor"""
        Tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.title('Table Properties')
        self.show_table_properties()

    def show_table_properties(self):
        """Display the table properties.
        Args: None, 
        Rets: None
        """
        try:
            properties = Tk.Listbox(self, height=10, width=50)
            data = self.parent.describe_table(self.parent.table)
            data = self.parent.flatten_nested_hierarchy(data)
            properties.delete(0, Tk.END)
            for i, item in enumerate(data):
                properties.insert(i+1, data[i])
                logging.info(data[i])
            properties.pack()
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

class ColumnRelationshipDialog(Tk.Toplevel):
    """Dialog Frame displaying column relationship"""
    def __init__(self, parent):
        """Constructor"""
        Tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.title('Column Relationships')
        self.show_column_relationships()

    def show_column_relationships(self):
        """Display the column relationships.
        Args: None
        Rets: None
        """
        try:
            relationships = Tk.Listbox(self, height=10, width=50)
            data = self.parent.show_column_relationships(self.parent.table)
            data = self.parent.flatten_nested_hierarchy(data)
            logging.info(data)
            relationships.delete(0, Tk.END)
            for i, item in enumerate(data):
                relationships.insert(i+1, data[i])
                logging.info(data[i])
            relationships.pack()
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

class ViewLogDialog(Tk.Toplevel):
    """Dialog Frame displaying the application log."""
    def __init__(self, parent):
        """Constructor"""
        Tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.title('Log')
        self.view_log_dialog()

    def view_log_dialog(self):
        """Display the application log.
        Args: None
        Rets: None
        """
        try:
            with open('databuild.log', 'r') as f:
                data = f.readlines()
                log = Tk.Listbox(self, height=20, width=50)
                for i, item in enumerate(data):
                    log.insert(i+1, data[i])
                log.pack()
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

class ConnectionInfoDialog(Tk.Toplevel):
    """Dialog Frame displaying the connection information."""
    def __init__(self, parent):
        """Constructor"""
        Tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.title('Connection Info')
        self.view_connection_info()

    def view_connection_info(self):
        """Display the connection info."""
        try:
            lbl_host = Tk.Label(self, text='Host: ').pack()
            lbl_host2 = Tk.Label(self, text=self.parent.host).pack()
            lbl_user = Tk.Label(self, text='User: ').pack()
            lbl_user2 = Tk.Label(self, text=self.parent.user).pack()
            lbl_pass = Tk.Label(self, text='Password: ').pack()
            lbl_pass2 = Tk.Label(self, text=self.parent.password).pack()
            lbl_data = Tk.Label(self, text='Database: ').pack()
            lbl_data2 = Tk.Label(self, text=self.parent.database).pack()
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

class HelpMenuDialog(Tk.Toplevel):
    """Dialog frame displaying help topics."""
    def __init__(self, parent):
        """Constructor"""
        Tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.title('Help Info')
        self.view_help_info()

    def view_help_info(self):
        """Display the connection info."""
        try:
            lbl_host = Tk.Label(self, text='Help: ').pack()
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

class AppInfoDialog(Tk.Toplevel):
    """Dialog frame displaying help topics."""
    def __init__(self, parent):
        """Constructor"""
        Tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.title('App Info')
        self.view_help_info()

    def view_help_info(self):
        """Display the connection info."""
        try:
            lbl_host = Tk.Label(self, text='Copyright 2014').pack()
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()


################################################################################
#################### Main Method ###############################################
################################################################################

def main():
    root = Tk.Tk()
    databuild = Databuild(root)
    root.mainloop()

if __name__ == '__main__':
    main()