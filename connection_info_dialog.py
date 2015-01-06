#!python2
# Tui Popenoe
# connection_info_dialog.py

import Tkinter as Tk

class ConnectionInfoDialog(Tk.Toplevel):
    """Dialog Frame displaying the connection information."""
    def __init__(self, parent):
        """Constructor"""
        Tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.title('Connection Info')
        self.view_connection_info()

    def view_connection_info(self):
        """Display the connection info."""
        try:
            lbl_host = Tk.Label(self, text='Host: ')\
                .grid(row=0, column=0)
            lbl_host2 = Tk.Label(self, text=self.parent.host)\
                .grid(row=0, column=1)
            lbl_user = Tk.Label(self, text='User: ')\
                .grid(row=1, column=0)
            lbl_user2 = Tk.Label(self, text=self.parent.user)\
                .grid(row=1, column=1)
            lbl_pass = Tk.Label(self, text='Password: ')\
                .grid(row=2, column=0)
            lbl_pass2 = Tk.Label(self, text=self.parent.password)\
                .grid(row=2, column=1)
            lbl_data = Tk.Label(self, text='Database: ')\
                .grid(row=3, column=0)
            lbl_data2 = Tk.Label(self, text=self.parent.database)\
                .grid(row=3, column=1)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()