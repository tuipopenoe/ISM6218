#!python2
# Tui Popenoe
# update_column_dialog.py

import Tkinter as Tk

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