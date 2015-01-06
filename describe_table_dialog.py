#!python2
# Tui Popenoe
# describe_table_dialog.py

import Tkinter as Tk

class DescribeTableDialog(Tk.Toplevel):
    """Dialog Frame displaying table properties."""
    def __init__(self, parent):
        """Constructor"""
        Tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.title('Table Properties')
        self.geometry("640x200")
        self.show_table_properties()

    def show_table_properties(self):
        """Display the table properties.
        Args: None, 
        Rets: None
        """
        try:
            properties = ttk.Treeview(self)
            data = self.parent.describe_table(self.parent.table)
            list_columns = self.parent.get_column_cursor_names()[1:]
            properties['columns'] = list_columns
            map(properties.delete, properties.get_children())
            for column in list_columns:
                properties.column(column,minwidth=10, width = 15)
                properties.heading(column, text=str(column))
            for row in data:
                if row is None:
                    row = 'None'
                properties.insert("", 'end', text="", values=row)
            properties['show'] = 'headings'
            properties.pack(expand=Tk.YES, fill=Tk.BOTH)
        except Exception, ex:
            logging.error(ex)
            traceback.print_exc()