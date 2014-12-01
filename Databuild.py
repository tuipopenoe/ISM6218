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
        Tk.Frame.__init__(self, parent)
        self.parent = parent
        self.init_ui()
        # MySQL database info
        self.db = None
        self.cursor = None
        # Connection info
        self.host = None
        self.user = None
        self.password = None
        self.database = None
        # Store data from queries
        self.data = None

    def init_ui(self):
        # Set the title
        self.parent.title("Databuild 2.0");

        # Connection Elements
        self.conn_button = Tk.Button(self.parent, text='Connect to Database',
                                     command=self.open_connection_dialog)
        self.conn_button.pack()

        # Display Data
        self.data_display = Tk.Listbox(self.parent)
        self.data_display.pack()

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
                self.open_connection(e_host.get(), e_user.get(), e_pass.get(),
                                     e_data.get())
                t.destroy()
            else:
                self.open_connection()
                t.destroy()

        b_conn = Tk.Button(t, text='Connect', command=_open_connection)
        b_conn.pack()

    def populate_display(self):
        self.data =  

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
            tkMessageBox.showinfo("", "Connection to database %s opened"
                                  % self.database)
        except:
            #TODO
            traceback.print_exc()

    def close_connection(self):
        try:
            # Disconnect from the server
            self.db.close()
            tkMessageBox.showinfo("", "Connection closed")
        except:
            #TODO
            traceback.print_exc()

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
            self.execute_command(sql)
        except:
            #TODO
            traceback.print_exc()

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