#!python2
# Tui Popenoe
# open_connection_dialog.py

import Tkinter as Tk

class OpenConnectionDialog(Tk.Toplevel):
    """Dialog to open a connection to a MySQL database"""
    def __init__(self, parent):
        """Constructor"""
        Tk.Toplevel.__init__(self)
        self.parent = parent
        self.title("Open Connection")
        self.open_connection()

    def open_connection(self):
        try:
            self.l_host = Tk.Label(self, text='Host: ').grid(row=0, column=0)
            self.e_host= Tk.Entry(self, justify=Tk.RIGHT)
            self.e_host.grid(row=0, column=1)
            self.l_user= Tk.Label(self, text='User: ').grid(row=1, column=0)
            self.e_user= Tk.Entry(self, justify=Tk.RIGHT)
            self.e_user.grid(row=1, column=1)
            self.l_pass= Tk.Label(self, text='Password: ').grid(row=2, column=0)
            self.e_pass= Tk.Entry(self, justify=Tk.RIGHT, show='*')
            self.e_pass.grid(row=2, column=1)
            self.l_data= Tk.Label(self, text='Database: ').grid(row=3, column=0)
            self.e_data= Tk.Entry(self, justify=Tk.RIGHT)
            self.e_data.grid(row=3, column=1)

            def _open_connection():
                try:
                    c_host = self.e_host.get()
                    c_user = self.e_user.get()
                    c_pass = self.e_pass.get()
                    c_data = self.e_data.get()

                    self.parent.open_new_connection(host=c_host,
                                                    user=c_user, 
                                                    password=c_pass,
                                                    database=c_data)
                    tables = self.parent.show_tables()
                    self.parent.select_table(tables[0])
                    self.parent.populate_table_dropdown()
                    self.parent.populate_display()
                    self.destroy()
                except Exception, ex:
                    logging.error(ex)
                    traceback.print_exc()

            b_conn = Tk.Button(self, text='Connect', command=_open_connection)\
                              .grid(row=4, column=0, columnspan=2)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()