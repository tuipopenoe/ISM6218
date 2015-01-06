#!python2
# Tui Popenoe
# databuild_gui.py GUI for the Databuild Application

import Tkinter as Tk
import ttk
import tkMessageBox

class DataBuildGUI(Tk.Frame):
    def __init__(self, parent):
        '''Constructor'''
        # python2 super()
        Tk.Frame.__init__(self, parent)
        # Set minimum size
        self.parent.minsize(width=720, height=300)
        # Initialize the application GUI elements
        self.init_ui()

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
            # Generate Menu
            self.init_ui_generate_menu()
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
            self.insert_menu.add_separator()
            self.insert_menu.add_command(label='Insert Table',
                                         command=self.insert_table_dialog)
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

    def init_ui_generate_menu(self):
        """Initialize the generate menu for importing and exporting files.
        Args: None
        Rets: None
        """
        try:
            self.gen_menu = Tk.Menu(self.menu_bar, tearoff=0)
            self.gen_menu.add_command(label='Import from File',
                                      command=self.import_file)
            self.gen_menu.add_separator()
            self.gen_menu.add_command(label='Export to File',
                                      command=self.export_file)
            self.menu_bar.add_cascade(label='Generate', menu=self.gen_menu)
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