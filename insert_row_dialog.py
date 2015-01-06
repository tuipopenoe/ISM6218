#!python2
# Tui Popenoe
# insert_row_dialog.py

import Tkinter as Tk

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