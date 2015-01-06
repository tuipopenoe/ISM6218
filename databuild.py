#!python2
# Tui Popenoe
# databuild.py - Databuild Workbench application

import csv
import urllib2
import Tkinter as Tk
import ttk
import tkMessageBox
import MySQLdb
import traceback
import logging

# Custom Classes
# import os
# import glob
# modules = glob.glob(os.path.dirname(__file__)+"/*.py")
# __all__ = [ os.path.basename(f)[:-3] for f in modules]
from app_info_dialog import *
from column_relationship_dialog import *
from connection_info_dialog import *
from delete_column_dialog import *
from delete_row_dialog import *
from describe_row_dialog import *
from describe_table_dialog import *
from help_menu_dialog import *
from insert_column_dialog import *
from insert_row_dialog import *
from insert_table_dialog import *
from open_connection_dialog import *
from update_column_dialog import *
from update_row_dialog import *
from view_log_dialog import *

class Databuild(Tk.Frame):
    def __init__(self, parent):
        """Constructor"""
        # Call the superclass __init__ method to initialize the Frame
        Tk.Frame.__init__(self, parent)
        # Initialize logging
        logging.basicConfig(filename='databuild.log', level=logging.INFO)
        # Set the parent Tkinter.Frame
        self.parent = parent
        # Initialize the class variables
        self.init_data()
        # Initialize the MySQL database connection
        self.open_connection()
        # Initialize the data displayed in the GUI
        self.init_display()

################################################################################
#################### Commands ##################################################
################################################################################

    def execute_command(self, sql, db, cursor):
        """Execute a MySQL command upon the database.
        Args: sql -> The SQL statement to be executed.
        Rets: Returns all rows of the query as a list of tuples.
        """
        try:
            # Execute the sql command
            cursor.execute(sql)
            # Commit any changes to the db
            db.commit()
            # return query output as a list of tuples
            return cursor.fetchall()
        except Exception, ex:
            # If there is an error, rollback the changes
            db.rollback()
            logging.error(ex)
            traceback.print_exc()
            return None

    def export_file(self, filename='databuild.csv'):
        """Export a database table to a csv flat file.
        Args: filename->filename to write to.
        Rets: None
        """
        try:
            self.data = self.select_rows(self.table)
            csv_writer = csv.writer(open(filename, "wb"))
            for row in data:
                csv_writer.writerow(row)
            tkMessageBox.showinfo('Database written to %s' % filename)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def import_file(self, filename='databuild.csv', table='temp_table'):
        """Import a file from CSV and create a table with the data.
        Args: filename->filename to read from
              table-> name of the table to create.
        Rets: None
        """
        try:
            sql_load_data = 'LOAD DATA LOCAL INFILE "csv?_%s.csv INTO TABLE %s'\
                % (filename, table)
            sql_load_data +=' FIELDS TERMINATED BY "," LINES TERMINATED BY "\n"'
            sql_load_data += ' IGNORE 1 LINES \n'
            sql_load_data += ''' ENCLOSED BY '"' ESCAPED BY "\\" '''
            self.execute_command(sql_load_data)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()


################################################################################
#################### Init ######################################################
################################################################################


    def init_display(self):
        """Load the main UI elements.
        Args: None
        Rets: None
        """
        try:
            # Tables in the Database
            self.table_label = Tk.Label(self.parent, text='Current Table: ')\
                                        .grid(row=0, column=0, sticky='ew')
            #Tables list is populated at runtime by self.populate_table_dropdown
            self.tables_list = None
            # Data Display
            self.display = ttk.Treeview(self.parent, selectmode='browse')
            # Bind the click event so that selected data can be used
            self.display.bind("<<TreeviewSelect>>",
                              self.get_current_row)
            self.display.grid(row=1, column=1, sticky='ews')
            # Scrollbar
            yscroll = Tk.Scrollbar(command=self.display.yview,
                                   orient=Tk.VERTICAL)
            yscroll.grid(row=1, column=2, sticky='ns')
            xscroll = Tk.Scrollbar(command=self.display.xview,
                                   orient=Tk.HORIZONTAL)
            xscroll.grid(row=2,column=1, sticky='ew')
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
            # Conncet to a MySQL database and return the connection
            db = MySQLdb.connect(host,user, password, database)
            #tkMessageBox.showinfo('','Connection opened on %s.' % host)
            return db
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def get_cursor(self, db):
        """Gets the cursor for the current Database connection.
        Args: db -> MySQL database connection
        Rets: Cursor for the current connection."""
        try:
            cursor = db.cursor()
            return cursor
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def close_connection(self, db):
        """Disconnect from the MySQL database.
        Args: None
        Rets: None
        """
        try:
            # Disconnect from the MySQL database
            db.close()
            tkMessageBox.showinfo('', 'Connection closed')
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

################################################################################
#################### Open Dialogs ##############################################
################################################################################

    def open_connection_dialog(self):
        """Create a dialog to open a connection to a database.
        Args: None
        Rets: None
        """
        try:
            connection_open_dialog = OpenConnectionDialog(self)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def view_connection_info_dialog(self):
        """Create a dialog to display the connection info.
        Args: None
        Rets: None
        """
        try:
            connection_info_dialog = ConnectionInfoDialog(self)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def insert_row_dialog(self):
        """Create a dialog to insert rows into the current table.
        Args: None
        Rets: None
        """
        try:
            insert_row_dialog = InsertRowDialog(self)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def insert_column_dialog(self):
        """Create a dialog to insert a column into the current table.
        Args: None
        Rets: None
        """
        try:
            insert_column_dialog = InsertColumnDialog(self)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def insert_table_dialog(self):
        """Create a dialog to insert a table into the database.
        Args: None
        Rets: None
        """
        try:
            insert_table_dialog = InsertTableDialog(self)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def update_row_dialog(self):
        """Create a dialog to update a row in the current table.
        Args: None
        Rets: None
        """
        try:
            update_row_dialog = UpdateRowDialog(self)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def update_column_dialog(self):
        """Create a dialog to update a column in the current table.
        Args: None
        Rets: None
        """
        try:
            update_column_dialog = UpdateColumnDialog(self)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def delete_row_dialog(self):
        """Create a dialog to delete a row in the current table.
        Args: None
        Rets: None
        """
        try:
            delete_row_dialog = DeleteRowDialog(self)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def delete_column_dialog(self):
        """Create a dialog to delete a column in the current table.
        Args: None
        Rets: None
        """
        try:
            delete_column_dialog = DeleteColumnDialog(self)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def help_menu_dialog(self):
        """Create a dialog to show a help menu with application documentation
        Args: None
        Rets: None
        """
        try:
            help_menu_dialog = HelpMenuDialog(self)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def app_info_dialog(self):
        """Create a dialog to show application info.
        Args: None
        Rets: None
        """
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
        """Fill the dropdown selection with tables from the current database
        Args: None
        Rets: None
        """
        try:
            options = self.show_tables()
            var = Tk.StringVar()
            var.set(options[0])
            self.tables_list = Tk.OptionMenu(self.parent, 
                                             var,
                                             *options,
                                             command=self.select_table)
            self.tables_list.grid(row=0, column=1,columnspan=1,sticky=Tk.W)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def populate_display(self):
        """Populate the display Treeview with the column names and row data
        Args: None
        Rets: None"""
        try:
            map(self.display.delete, self.display.get_children())
            self.data = self.select_rows(self.table)
            list_columns = self.get_column_names(self.table)
            list_columns = self.flatten_nested_hierarchy(list_columns)
            # Accept tuple of column names
            self.display['columns'] = list_columns

            for column in list_columns:
                self.display.column(column)
                self.display.heading(column, text=str(column).capitalize())
            for row in self.data:
                self.display.insert("", 'end', text="", values=row)
            self.display['show'] = 'headings'
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()
################################################################################
#################### ACTIONS ###################################################
################################################################################

    def get_current_row(self, instance):
        """Get the currently selected row in the display Treeview
        Args: instance -> The treeview instance
        Rets: None
        """
        try:
            selected_item = self.display.selection()
            if selected_item:
                self.current_columns = self.display['columns']
                self.current_row = self.display.item(selected_item)['values']
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def delete_current_row(self):
        """Delete the currently selected row from the table.
        Args: None
        Rets: None
        """
        try:
            where = ''
            for i, column in enumerate(self.current_columns):
                where += '%s = "%s" ' % (column, self.current_row[i])
            self.delete_row(self.table, where)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc(ex)

    def select_table(self, table):
        """Set the current table to table.
        Args: table-> The MySQL table to view and manipulate
        Rets: None
        """
        try:
            self.table = table[0]
            self.populate_display()
        except Exception, ex:
            logging.error(ex)
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
        Rets: The outputs of the SQL query
        """
        try:
            sql = 'DROP ' + database + ';'
            return self.execute_command(sql)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def show_tables(self):
        """Show available tables in the MySQL database
        Args: None
        Rets: Output from the MySQL query
        """
        try:
            sql = 'SHOW tables;'
            return self.execute_command(sql)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def insert_table(self, table):
        """Create a new table in the database.
        Args: table-> name of the table to be created
        Rets: Output from the MySQL query
        """
        try:
            init_id = '(id INT NOT NULL PRIMARY KEY AUTO_INCREMENT)'
            sql = 'CREATE TABLE IF NOT EXISTS %s %s;' % (table, init_id)
            return self.execute_command(sql)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def describe_table(self, table):
        """Display the table columns and their types.
        Args: table-> table to display
        Rets: Output of the SQL query
        """
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
        Rets: Output of the SQL query
        """
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
        Rets: Output of the SQL query
        """
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
        Rets: Output of the SQL query
        """
        try:
            sql = 'SELECT column_name FROM information_schema.columns WHERE '\
                  'table_name="%s";' % table
            return self.execute_command(sql)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def get_column_cursor_names(self):
        """Get the column names using the cursor in the MySQLdb connector
        Args: None
        Rets: None
        """
        try:
            column_names = []
            columns = self.cursor.description
            for column in columns:
                column_names.append(column[0])
            return column_names
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def update_row(self, table, values):
        """Update records in a table.
        Args: table-> Table to update values in
              values-> Values to update in the table
        Rets: Output of the SQL query
        """
        try:
            sql = 'UPDATE %s %s;' % (table, values)
            return self.execute_command(sql)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def delete_row(self, table, where):
        """Delete a row from the table.
        Args: table-> Table to delete a row from
              column_name-> Column to compare where clause against
              value-> value to match against the column
        Rets: Output of the SQL query
        """
        try:
            sql = 'DELETE FROM %s WHERE %s;' % (table, where)
            return self.execute_command(sql)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def insert_column(self, table, column_name, column_type):
        """Add a column to a table
        Args: table->Table name to add a column to
              column_name->Name of the column to be added
              column_type->Type of the column to be added
        Rets: Output of the SQL query
        """
        try:
            sql ='ALTER TABLE %s ADD %s %s;' % (table, column_name, column_type)
            return self.execute_command(sql)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

    def delete_column(self, table, column_name):
        """Delete a column from a table
        Args: table-> Table to delete the column from
              column_name-> Name of the column to delete
        Rets: Output of the SQL statement
        """
        try:
            sql = 'ALTER TABLE %s DROP %s;' % (table, column_name)
            return self.execute_command(sql)
        except:
            #TODO
            traceback.print_exc()

    def view_log_dialog(self):
        """Create a dialog box to display the application log file
        Args: None
        Rets: None
        """
        try:
            view_log_dialog = ViewLogDialog(self)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()

################################################################################
#################### Main Method ###############################################
################################################################################

def main():
    """Main method called at runtime."""
    root = Tk.Tk()
    databuild = Databuild(root)
    root.mainloop()

if __name__ == '__main__':
    main()