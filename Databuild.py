#!python2
# Tui Popenoe

import paramiko
import urllib2
import json
import Tkinter as Tk
import tkMessageBox
import MySQLdb
import traceback

class Databuild(Tk.Frame):
    def __init__(self, parent):
        # Init the class frame
        Tk.Frame.__init__(self, parent)
        # Set the parent frame
        self.parent = parent

        ############################
        # Initialize Class Variables
        ############################
        # MySQL database info
        self.db = None
        self.cursor = None
        self.current_table = None
        # Connection Variables
        self.host = None
        self.user = None
        self.password = None
        self.database = None
        # Store data from queries
        self.data = None
        self.tables = None
        self.table = 'databuild'

        # Open initial connection
        self.open_connection()
        # Setup the UI
        self.init_ui()
        # Populate the inital data
        self.init_data()

    def init_ui(self):
        # Set the title
        self.parent.title("Databuild 2.0");

        # Connection Elements
        self.conn_button = Tk.Button(self.parent,
                                     text='Connect to Database',
                                     command=self.open_connection_dialog)\
                                    .grid(row=0, column=5, columnspan=2)

        # Populate button
        self.pop_disp_button = Tk.Button(self.parent, text='Populate Display',
                                         command=self.populate_display)\
                                        .grid(row=1, column=5, columnspan=2)
        # Tables in the Database
        self.tables_list = None

        # Display Data
        self.data_display = Tk.Listbox(self.parent, height=10, width=20)
        self.data_display.grid(row=3, column=0)
        yscroll = Tk.Scrollbar(command=self.data_display.yview,
                               orient=Tk.VERTICAL)
        yscroll.grid(row=3, column=5, sticky='ns')

    def init_data(self):
        self.populate_table_dropdown()
        #self.populate_display()

    def execute_command(self, sql):
        try:
            # Execute the sql command
            self.cursor.execute(sql)
            # Commit changes to the db
            self.db.commit()
            # return output
            return self.cursor.fetchall()
        except:
            # If there is an error, rollback the changes
            self.db.rollback()
            return None

    def open_connection_dialog(self):
        t = Tk.Toplevel(self)
        l_host = Tk.Label(t, text='Host: ')
        l_host.pack()
        e_host = Tk.Entry(t, justify=Tk.RIGHT)
        e_host.pack()
        l_user = Tk.Label(t, text='User: ')
        l_user.pack()
        e_user = Tk.Entry(t, justify=Tk.RIGHT)
        e_user.pack()
        l_pass = Tk.Label(t, text='Password: ')
        l_pass.pack()
        e_pass = Tk.Entry(t, justify=Tk.RIGHT)
        e_pass.pack()
        l_data = Tk.Label(t, text='Database: ')
        l_data.pack()
        e_data = Tk.Entry(t, justify=Tk.RIGHT)
        e_data.pack()

        def _open_connection():
            if e_host.get() and e_user.get() and e_pass.get() and e_data.get():
                self.open_new_connection(e_host.get(),
                                         e_user.get(), 
                                         e_pass.get(),
                                         e_data.get())
                t.destroy()
            else:
                self.open_new_connection()
                t.destroy()

        b_conn = Tk.Button(t, text='Connect', command=_open_connection)
        b_conn.pack()

    def populate_table_dropdown(self):
        options = self.show_tables()
        var = Tk.StringVar()
        var.set(options[0])
        self.tables_list = Tk.OptionMenu(self.parent, 
                                         var,
                                         *options,
                                         command=self.select_table)\
                                        .grid(row=2, column=5, columnspan=2)

    def select_table(self, table):
        """Set the current table to table."""
        try:
            self.table = table[0]
        except:
            traceback.print_exc()

    def populate_display(self):
        # Clear the listbox
        self.data_display.delete(0, Tk.END)
        self.data = self.select_rows(self.table)
        for i in range(len(self.data)):
            self.data_display.insert(i+1, self.data[i])

    def open_connection(self, host='localhost', user='root',
                        password='passw0rd', database='databuild'):
        try:
            self.host = host
            self.user = user
            self.password = password
            self.database = database
            self.db = MySQLdb.connect(self.host, self.user, self.password,
                                      self.database)
            self.cursor = self.db.cursor()
        except:
            #TODO
            traceback.print_exc()

    def open_new_connection(self, host='localhost', user='root',
                        password='passw0rd', database='databuild'):
        try:
            self.open_connection(host, user, password, database)
            self.populate_table_dropdown()
            tkMessageBox.showinfo("", "Connection to database %s opened"
                                  % self.database)
        except:
            traceback.print_exc()

    def close_connection(self):
        try:
            # Disconnect from the server
            self.db.close()
            tkMessageBox.showinfo("", "Connection closed")
        except:
            #TODO
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

    def insert_row(self, table, **kwargs):
        """Insert records into a table."""
        try:
            sql = 'INSERT INTO ' + table + kwargs
            self.execute_command(sql)
        except:
            #TODO
            traceback.print_exc()

    def update_row(self, table, **kwargs):
        """Update records in a table."""
        try:
            sql = 'UPDATE ' + table + kwargs
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
        print('log')

def main():
    root = Tk.Tk()
    databuild = Databuild(root)
    root.configure(background = 'white')
    root.mainloop()

if __name__ == '__main__':
    main()