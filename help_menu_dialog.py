#!python2
# Tui Popenoe
# help_menu_dialog.py

import Tkinter as Tk

class HelpMenuDialog(Tk.Toplevel):
    """Dialog frame displaying help topics."""
    def __init__(self, parent):
        """Constructor"""
        Tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.title('Help Info')
        self.view_help_info()

    def view_help_info(self):
        """Display the connection info."""
        try:
            with open('README.md', 'r') as f:
                data = f.readlines()
                log = Tk.Listbox(self, height=30, width=100)
                for i, item in enumerate(data):
                    log.insert(i+1, data[i])
                log.grid(row =0, column=0, sticky='ew')
                yscroll = Tk.Scrollbar(command=log.yview,
                                       orient=Tk.VERTICAL)
                yscroll.grid(row=0, column=1, sticky='ns')
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()