#!python2
# Tui Popenoe
# app_info_dialog

import Tkinter as Tk

class AppInfoDialog(Tk.Toplevel):
    """Dialog frame displaying help topics."""
    def __init__(self, parent):
        """Constructor"""
        Tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.title('App Info')
        self.view_help_info()

    def view_help_info(self):
        """Display the connection info."""
        try:
            lbl_host = Tk.Label(self, text='Copyright 2014').pack()
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()
