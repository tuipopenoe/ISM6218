#!python2
# Tui Popenoe
# view_log_dialog.py

import Tkinter as Tk

class ViewLogDialog(Tk.Toplevel):
    """Dialog Frame displaying the application log."""
    def __init__(self, parent):
        """Constructor"""
        Tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.title('Log')
        self.view_log_dialog()

    def view_log_dialog(self):
        """Display the application log.
        Args: None
        Rets: None
        """
        try:
            def _clear_log():
                with open('databuild.log', 'w') as f:
                    f.seek(0)
                    f.write('')
                self.view_log_dialog()
            clear_log = Tk.Button(self, text='Clear Log', command=_clear_log)
            clear_log.pack()
            with open('databuild.log', 'r') as f:
                data = f.readlines()
                log = Tk.Listbox(self, height=30, width=100)
                for i, item in enumerate(data):
                    log.insert(i+1, data[i])
                log.pack()
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()