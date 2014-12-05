#!python2
# Tui Popenoe

import paramiko
import urllib2
import json
import Tkinter as Tk
import tkMessageBox
import MySQLdb
import traceback
import logging

class Databuild(Tk.Frame):
    def __init__(self, parent):
        # Call the superclass __init__ method to initialize the Frame
        Tk.Frame.__init__(self, parent)
        # Initialize logging
        logging.basicConfig(filename='databuild.log', level=logging.INFO)
        # Set the parent Tkinter.Frame
        self.parent = parent
        # Initialize the class variables
        self.init_data()
        # Initialize the MySQL database connection
        self.init_connection()
        # Initialize the application GUI elements
        self.init_ui()
        # Initialize the data displayed in the GUI
        self.init_display()

    def init_connection(self):
        """Initialize the MySQL database connection.
        Args: None
        Rets: None
        """
        try:
            self.open_connection()
        except Exception, ex:
            logging.error(ex)

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
            self.tables = None
            self.current_table = None
            self.table = 'databuild'
        except Exception, ex:
            logging.error(ex)

    def init_ui(self):
        """Initialize the application GUI elements.
        Args: None
        Rets: None
        """
        # Set the title
        self.parent.title('Databuild 2.0')
        #self.parent.geometry('1280x720')
        # Initialize the UI Menus
        self.init_ui_menus()
        # Initialize the table selector dropdown
        self.init_ui_tables()
        # Initialize the data display
        self.init_ui_display()

    def init_display(self):
        """Fetch the initial data to display upon application start.
        Args: None
        Rets: None"""
        try:
            self.populate_table_dropdown()
            self.populate_display()
        except Exception, ex:
            logging.error(ex)

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
            return None

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
            # Set menu bar for root frame 
            self.parent.config(menu=self.menu_bar)
        except Exception, ex:
            logging.error(ex)

    def init_ui_file_menu(self):
        try:
            self.file_menu = Tk.Menu(self.menu_bar, tearoff=0)
            #TODO
            self.file_menu.add_separator()
            self.menu_bar.add_cascade(label='File',
                                      menu=self.file_menu)
        except Exception, ex:
            logging.error(ex)

    def init_ui_connection_menu(self):
        """Initialize the GUI elements for opening and closing connections.
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
                                       command=self.view_connection_info)
            self.menu_bar.add_cascade(label='Connections',
                                      menu=self.conn_menu)
        except Exception, ex:
            logging.error(ex)

    def init_ui_relationships_menu(self):
        """Initialize the menu for viewing database relationships.
        Args: None
        Rets: None
        """
        try:
            self.rel_menu = Tk.Menu(self.menu_bar, tearoff=0)
            self.rel_menu.add_command(label='View Relationsips',
                                      command=self.view_relationships_dialog)
            self.rel_menu.add_separator()
            self.rel_menu.add_command(label='Describe Table',
                                      command=self.describe_table_dialog)
            self.menu_bar.add_cascade(label='Relationships',
                                      menu=self.rel_menu)
        except Exception, ex:
            logging.error(ex)

    def init_ui_tables(self):
        try:
            # Tables in the Database
            self.table_label = Tk.Label(self.parent, text='Current Table: ')\
                                        .grid(row=1, column=3, sticky=Tk.W+Tk.E)
            #TODO change this as data will be initialized
            self.tables_list = None

        except Exception, ex:
            logging.error(ex)

    def init_ui_display(self):
        try:
            # Display Data
            self.data_display = Tk.Listbox(self.parent, height=20, width=50)
            self.data_display.grid(row=2, column=0, columnspan=5,
                                   sticky=Tk.W+Tk.E)
            yscroll = Tk.Scrollbar(command=self.data_display.yview,
                                   orient=Tk.VERTICAL)
            yscroll.grid(row=2, column=5, sticky='ns')
        except Exception, ex:
            logging.error(ex)

    def init_ui_insert_menu(self):
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

    def view_connection_info(self):
        try:
            raise NotImplementedError()
        except Exception, ex:
            logging.error(ex)

    def view_relationships_dialog(self):
        try:
            raise NotImplementedError()
        except Exception, ex:
            logging.error(ex)

    def insert_row_dialog(self):
        """Create a dialog to insert rows into a table.
        Args: None
        Rets: None
        """
        try:
            insert_row_dialog = InsertRowDialog(self)
        except Exception, ex:
            logging.error(ex)

    def insert_column_dialog(self):
        try:
            insert_column_dialog = InsertColumnDialog(self)
        except Exception, ex:
            logging.error(ex)

    def describe_table_dialog(self):
        """Create a dialog box that describes the table layout.
        Args: None
        Rets: None
        """
        try:
            describe_table_dialog = DescribeTableDialog(self)
        except Exception, ex:
            logging.error(ex)

    def populate_table_dropdown(self):
        try:
            options = self.show_tables()
            var = Tk.StringVar()
            var.set(options[0])
            self.tables_list = Tk.OptionMenu(self.parent, 
                                             var,
                                             *options,
                                             command=self.select_table)\
                                            .grid(row=1,
                                                  column=4,
                                                  columnspan=2,
                                                  sticky=Tk.W+Tk.E)
        except Exception, ex:
            logging.error(ex)

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

    def populate_display(self):
        """Populate the display listbox with the column names and row data
        Args: None
        Rets: None"""
        try:
            self.data_display.delete(0, Tk.END)
            self.data = self.select_rows(self.table)
            self.data_display.insert(0, self.flatten_nested_hierarchy(
                self.get_column_names(self.table)))
            for i in range(len(self.data)):
                self.data_display.insert(i+1, self.data[i])
        except Exception, ex:
            logging.error(ex)

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

    def create_database(self, database):
        """Create a new database in the MySQL instance
        Args: database-> Name of the database to create
        Rets: Result of the SQL query
        """
        try:
            sql = 'CREATE DATABASE %s%s' % (database, ';')
            return self.execute_command(sql)
        except Exception, ex:
            logging.error(ex)

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

    def drop_database(self, database):
        """Delete a database from the MySQL instance
        Args: database-> The database to delete
        Rets: The outputs of the SQL query"""
        try:
            sql = 'DROP ' + database + ';'
            return self.execute_command(sql)
        except Exception, ex:
            logging.error(ex)

    def show_tables(self):
        """Show available tables in the MySQL database
        Args: None
        Rets: Output from the MySQL query"""
        try:
            sql = 'SHOW tables;'
            return self.execute_command(sql)
        except Exception, ex:
            logging.error(ex)

    def create_table(self, table):
        """Create a new table in the database.
        Args: table-> name of the table to be created
        Rets: Output from the MySQL query
        """
        try:
            sql = 'CREATE TABLE IF NOT EXISTS %s' % table
            return self.execute_command(sql)
        except Exception, ex:
            logging.error(ex)

    def describe_table(self, table):
        """Display table organization."""
        try:
            sql = 'DESCRIBE ' + table + ';'
            return self.execute_command(sql)
        except Exception, ex:
            logging.error(ex)

    def flatten_nested_hierarchy(self, hierarchy):
        """Flatten the hiearchy into a single list.
        Args: hierarchy-> The nested lists to be flattened
        Rets: The list containing the flattened hierarchy
        """
        try:
            return [element for tupl in hierarchy for element in tupl]
        except Exception, ex:
            logging.error(ex)

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

    def add_column(self, table, column_name, column_type):
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

    def view_log(self):
        try:
            raise NotImplementedError()
        except Exception, ex:
            logging.error(ex)

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
            traceback.print_exc()
            logging.error(ex)

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
                logging.info(c_name, c_type)
                #self.parent.insert_column(self.parent.table, c_name, c_type)
                self.destroy()
                self.parent.populate_display()
            b_ins = Tk.Button(self,
                              text='Insert Column',
                              command=_insert_column)\
                              .grid(row=2, column=1, sticky=Tk.W+Tk.E)
        except Exception, ex:
            traceback.print_exc()
            logging.error(ex)


class DescribeTableDialog(Tk.Toplevel):
    """Dialog Frame displaying table properties."""
    def __init__(self, parent):
        """Constructor"""
        Tk.Toplevel.__init__(self)
        logging.info(parent)
        self.parent = parent
        self.show_table_properties()

    def show_table_properties(self):
        """Display the table properties.
        Args: None, 
        Rets: None
        """
        try:
            properties = Tk.Listbox(self.parent, height=10, width=50)
            data = self.parent.describe_table(self.parent.table)
            data = self.parent.flatten_nested_hierarchy(data)
            logging.info(self.parent.describe_table(self.parent.table))
            properties.delete(0, Tk.END)
            for i, item in enumerate(data):
                properties.insert(i+1, data[i])
                logging.info(data[i])
            properties.pack()
        except Exception, ex:
            logging.error(ex)

def main():
    root = Tk.Tk()
    databuild = Databuild(root)
    root.mainloop()

if __name__ == '__main__':
    main()