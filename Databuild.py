#!python2
# Tui Popenoe

import paramiko
import urllib2
import json
import Tkinter
import MySQLdb

class Databuild(Tkinter.Frame):
    def __init__(self, parent):
        Tkinter.Frame.__init__(self, parent)
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

    def init_ui(self):
        # Set the title
        self.parent.title("Databuild 2.0");


    def open_connection(self, host='localhost', user='root',
                        password='passw0rd', database='databuild'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.db = MySQLdb.connect(self.host, self.user, self.password,
                                  self.database)
        self.cursor = self.db.cursor()

    def close_connection(self):
        try:
            # Disconnect from the server
            self.db.close()
        except:
            #TODO

    def execute_command(self, sql):
        try:
            # Execute the sql command
            self.cursor.execute(sql)
            # Commit changes to the db
            self.db.commit()
            # TODO: RETURN OUTPUT
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

    def show_databases(self):
        """Show which databases are available."""
        try:
            sql = 'SHOW DATABASES;'
            self.execute_command(sql)
            #TODO pipe output to screen
        except:
            #TODO

    def create_database(self, database):
        """Create a new database"""
        try:
            sql = 'CREATE DATABASE ' + database + ';'
            self.execute_command(sql)
        except:
            #TODO

    def use_database(self, database):
        """Select a database to use."""
        try:
            sql = 'USE ' + database + ';'
            self.execute_command(sql)
        except:
            #TODO

    def drop_database(self, database):
        """Delete a database."""
        try:
            #TODO: Check for confirmation
            sql = 'DROP ' + database + ';'
            self.execute_command(sql)
        except:
            #TODO

    def show_tables(self):
        """Show available tables."""
        try:
            sql = 'SHOW tables;'
            self.execute_command(sql)
        except:
            #TODO

    def create_table(self, **kwargs):
        """Create a new table in the database."""
        try:
            sql = 'CREATE TABLE ' + kwargs[0]
            #TODO
        except:
            #TODO

    def describe_table(self, table):
        """Display table organization."""
        try:
            sql = 'DESCRIBE ' + table + ';'
            self.execute_command(sql)
        except:
            #TODO

    def insert_row(self, table, **kwargs):
        """Insert records into a table."""
        try:
            sql = 'INSERT INTO ' + table + kwargs
            self.execute_command(sql)
        except:
            #TODO

    def update_row(self, table, **kwargs):
        """Update records in a table."""
        try:
            sql = 'UPDATE ' + table + kwargs
            self.execute_command(sql)
        except:
            #TODO

    def delete_row(self, table, column_name, value):
        """Delete a row from the table."""
        try:
            sql = 'DELETE FROM %S WHERE %s=%s;' % (table, column_name, value)

    def add_column(self, table, column_name, column_type):
        """Add a column to a table."""
        try:
            sql ='ALTER TABLE %s ADD %s %s;' % (table, column_name, column_type)
            self.execute_command(sql)
        except:
            #TODO

    def delete_column(self, table, column_name):
        """Delete a column from a table."""
        try:
            sql = 'ALTER TABLE %s DROP %s;' % (table, column_name)
            self.execute_command(sql)
        except:
            #TODO

    def generate_output(self, data, filename='output', filetype='.csv'):
        """Write a table to a file."""
        try:
            with open(filename + filetype, 'w') as f:
                f.write(data)
        except:
            #TODO

    def view_log(self):
        print('log')

def main():
    root = Tkinter.Tk()
    databuild = Databuild(root)
    root.configure(background = 'white')
    root.mainloop()

if __name__ == '__main__':
    main()