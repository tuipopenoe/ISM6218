#!python2
# Tui Popenoe
# delete_row_dialog.py

class DeleteRowDialog(Tk.Toplevel):
    """Dialog confirmation for deleting a row."""
    def __init__(self, parent):
        """Constructor"""
        Tk.Toplevel.__init__(self)
        self.parent = parent
        self.title('Delete Row')
        self.delete_row()

    def delete_row(self):
        """Delete a row from the table.
        Args: None
        Rets: None
        """
        try:
            lbl_confirm = Tk.Label(self, text='Confirm Delete Row?').pack()
            btn_cancel = Tk.Button(self, text='Cancel',
                                   command=self.destroy).pack()
            def _delete_row():
                self.parent.delete_current_row()
                self.destroy()
                self.parent.populate_display()
            btn_confirm = Tk.Button(self, text='Delete Row',
                        command=_delete_row).pack()
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()
