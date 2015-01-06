#!python2
# Tui Popenoe
# insert_row_dialog.py

import Tkinter as Tk

class InsertTableDialog(Tk.Toplevel):
    """Dialog to insert a table into the database."""
    def __init__(self, parent):
        """Constructor"""
        Tk.Toplevel.__init__(self)
        self.parent = parent
        self.title("Insert Table")
        self.insert_table()

    def insert_table(self):
        """Insert a table into the database.
        Args: None
        Rets: None
        """
        try:
            lbl_name = Tk.Label(self, text='Enter a table name: ').pack()
            ent_name = Tk.Entry(self)
            ent_name.pack()

            def _insert_tab():
                t_name = ent_name.get()
                self.parent.insert_table(t_name)
                self.destroy()
                self.parent.populate_table_dropdown()

            btn_name = Tk.Button(self, text='Insert Table', command=_insert_tab)
            btn_name.pack()
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()
