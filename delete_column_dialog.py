#!python2
# Tui Popenoe
# delete_column_dialog.py

import Tkinter as Tk

class DeleteColumnDialog(Tk.Toplevel):
    """Dialog confirmation for deleting a column."""
    def __init__(self, parent):
        """Constructor"""
        Tk.Toplevel.__init__(self)
        self.parent = parent
        self.title('Delete column')
        self.delete_column()

    def delete_column(self):
        """Delete a column from the table.
        Args: None
        Rets: None
        """
        try:
            lbl_confirm = Tk.Label(self,
                                   text='Enter the column to delete: ').pack()
            e_column = Tk.Entry(self)
            e_column.pack()
            def _delete_column():
                try:
                    self.parent.delete_column(self.parent.table,
                                              e_column.get())
                    self.parent.populate_display()
                except Exception, ex:
                    logging.error(ex)
                    traceback.print_exc()
            btn_confirm = Tk.Button(self, text='Delete Column',
                        command=_delete_column).pack()
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()