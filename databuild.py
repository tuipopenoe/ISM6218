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

        self.init_ui_menus()
        self.init_ui_tables()
        self.init_ui_display()
        self.init_ui_insert()

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
        try:
            self.rel_menu = Tk.Menu(self.menu_bar, tearoff=0)
            self.rel_menu.add_command(label='View Relationsips',
                                      command=self.view_relationships_dialog)
            self.rel_menu.add_separator()
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
            self.data_display = Tk.Listbox(self.parent, height=10, width=40)
            self.data_display.grid(row=2, column=0, columnspan=5,
                                   sticky=Tk.W+Tk.E)
            yscroll = Tk.Scrollbar(command=self.data_display.yview,
                                   orient=Tk.VERTICAL)
            yscroll.grid(row=2, column=5, sticky='ns')
        except Exception, ex:
            logging.error(ex)

    def init_ui_insert(self):
        try:
            # Insert Rows
            self.insert_row_button = Tk.Button(self.parent,
                                               text='Insert Row',
                                               command=self.insert_row_dialog)\
                                     .grid(row=4, column=4, sticky=Tk.W+Tk.E)
            self.insert_column_button = \
                    Tk.Button(self.parent,
                              text='Insert Column',
                              command=self.insert_column_dialog)\
                              .grid(row=4, column=3, sticky=Tk.W+Tk.E)
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
        try:
            t = Tk.Toplevel(self)

            column_names = list(self.get_column_names(self.table))
            entry = {}
            label = {}
            i = 0
            for name in column_names:
                e = Tk.Entry(t)
                e.grid(column=1, sticky=Tk.E)
                entry[name] = e

                lb = Tk.Label(t, text=name)
                lb.grid(row=i, column=0, sticky=Tk.W)
                label[name] = lb
                i += 1

            def _insert_row():
                values = []
                for name in column_names:
                    values.append(entry[name].get())
                values = ', '.join(map(lambda x: "'" + x + "'", values))
                self.insert_row(self.table, values)

                t.destroy()
                self.populate_display()
            b_ins = Tk.Button(t, text='Insert Row', command=_insert_row)\
                             .grid(row=i+1, column=1, sticky=Tk.W+Tk.E)
            

        except:
            traceback.print_exc()

    def insert_column_dialog(self):
        try:
            t = Tk.Toplevel(self)
            lb = Tk.Label(t, text='Column Name: ').grid(row=0,
                                                      column=0,
                                                      sticky=Tk.W+Tk.E)
            e = Tk.Entry(t).grid(row=0, column=1, sticky=Tk.W+Tk.E)
            lbl = Tk.Label(t, text='Column Type: ').grid(row=1,
                                                        column=0,
                                                        sticky=Tk.W+Tk.E)
            en = Tk.Entry(t).grid(row=1, column=1, sticky=Tk.W+Tk.E)

            def _insert_column():
                t.destroy()

            col_ins_button = Tk.Button(t, text='Insert Column',
                                        command=_insert_column)\
                                        .grid(row=2, column=1, sticky=Tk.W+Tk.E)
        except:
            traceback.print_exc()

    def populate_table_dropdown(self):
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

    def select_table(self, table):
        """Set the current table to table."""
        try:
            self.table = table[0]
            self.populate_display()
        except:
            traceback.print_exc()

    def populate_display(self):
        # Clear the listbox
        self.data_display.delete(0, Tk.END)
        self.data = self.select_rows(self.table)
        for i in range(len(self.data)):
            self.data_display.insert(i+1, self.data[i])

    def open_new_connection(self, host='localhost', user='root',
                        password='passw0rd', database='databuild'):
        try:
            self.open_connection(host, user, password, database)
            self.populate_table_dropdown()
            tkMessageBox.showinfo("", "Connection to database %s opened"
                                  % self.database)
        except:
            traceback.print_exc()




    def select_database(self, database='databuild'):
        try:
            # Close the existing connection
            self.db.close()
            self.open_connection(database=database)
        except:
            #TODO
            traceback.print_exc()

    def show_databases(self):
        """Show which databases are available."""
        try:
            sql = 'SHOW DATABASES;'
            self.execute_command(sql)
            #TODO pipe output to screen
        except:
            #TODO
            traceback.print_exc()

    def create_database(self, database):
        """Create a new database"""
        try:
            sql = 'CREATE DATABASE ' + database + ';'
            self.execute_command(sql)
        except:
            #TODO
            traceback.print_exc()

    def use_database(self, database='databuild'):
        """Select a database to use."""
        try:
            sql = 'USE ' + database + ';'
            self.execute_command(sql)
        except:
            #TODO
            traceback.print_exc()

    def drop_database(self, database):
        """Delete a database."""
        try:
            #TODO: Check for confirmation
            sql = 'DROP ' + database + ';'
            self.execute_command(sql)
        except:
            #TODO
            traceback.print_exc()

    def show_tables(self):
        """Show available tables."""
        try:
            sql = 'SHOW tables;'
            return self.execute_command(sql)
        except:
            #TODO
            traceback.print_exc()
            return None

    def create_table(self, **kwargs):
        """Create a new table in the database."""
        try:
            sql = 'CREATE TABLE ' + kwargs[0]
            #TODO
        except:
            #TODO
            traceback.print_exc()

    def describe_table(self, table):
        """Display table organization."""
        try:
            sql = 'DESCRIBE ' + table + ';'
            self.execute_command(sql)
        except:
            #TODO
            traceback.print_exc()

    def select_rows(self, table, where=''):
        """Select rows from the table."""
        try:
            # Initialize the select statement
            sql = 'SELECT * FROM %s' % table
            # If a where clause is present, add it to the end
            if where:
                sql += ' WHERE %s ' % where
            # Add the closing semicolon
            sql += ';'
            # return the values from the executed command
            return self.execute_command(sql)
        except:
            traceback.print_exc()
            return None

    def insert_row(self, table, values):
        """Insert records into a table."""
        try:
            sql = 'INSERT INTO %s VALUES (%s);'% (table, values)
            logging.info(sql)
            self.execute_command(sql)
        except:
            logging.error('Failed to insert row')
            traceback.print_exc()

    def get_column_names(self, table):
        """Get the column names for the specified table."""
        try:
            sql = 'SELECT column_name FROM information_schema.columns WHERE '\
                  'table_name="%s"' % table
            return self.execute_command(sql)
        except:
            traceback.print_exc()

    def update_row(self, table, values):
        """Update records in a table."""
        try:
            sql = 'UPDATE ' + table + values
            self.execute_command(sql)
        except:
            #TODO
            traceback.print_exc()

    def delete_row(self, table, column_name, value):
        """Delete a row from the table."""
        try:
            sql = 'DELETE FROM %S WHERE %s=%s;' % (table, column_name, value)
            self.execute_command(sql)
        except:
            traceback.print_exc()

    def add_column(self, table, column_name, column_type):
        """Add a column to a table."""
        try:
            sql ='ALTER TABLE %s ADD %s %s;' % (table, column_name, column_type)
            self.execute_command(sql)
        except:
            #TODO
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
        except:
            #TODO
            traceback.print_exc()

    def view_log(self):
        try:
            raise NotImplementedError()
        except Exception, ex:
            logging.error(ex)

class InsertRowDialog(Tk.Toplevel):
    """Dialog frame to insert rows into a table."""
    def __init__(self, parent):
        """Constructor"""
        DatabuildDialog.__init__(self)
        # Set a reference to the main databuild Frame
        self.parent = parent
        self.geometry("400x300")
        self.title("Insert Row: ")

    def on_close(self):
        """Action to be performed on closing the frame.
        Args: None
        Rets: None
        """
        try:
            # Destroy this frame
            self.destroy()
            # Show the parent frame
            self.parent.show()
        except Exception, ex:
            logging.error(ex)

class InsertColumnDialog(Tk.Toplevel):
    """Dialog frame to insert columns into a table."""
    def __init__(self, parent):
        """Constructor"""
        Tk.Toplevel.__init__(self)
        # Set a reference to the main databuild Frame
        self.parent = parent

    def on_close(self):
        """Action to be performed on closing the frame.
        Args: None
        Rets: None
        """
        try:
            # Destroy this frame
            self.destroy()
            # Show the parent frame
            self.parent.show()
        except Exception, ex:
            logging.error(ex)

def main():
    root = Tk.Tk()
    databuild = Databuild(root)
    root.mainloop()

if __name__ == '__main__':
    main()