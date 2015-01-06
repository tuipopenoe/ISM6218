#!python2
# Tui Popenoe
# column_relationship_dialog.py

class ColumnRelationshipDialog(Tk.Toplevel):
    """Dialog Frame displaying column relationship"""
    def __init__(self, parent):
        """Constructor"""
        Tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.title('Column Relationships')
        self.geometry("760x720")
        self.show_column_relationships()

    def show_column_relationships(self):
        """Display the column relationships.
        Args: None
        Rets: None
        """
        try:
            properties = ttk.Treeview(self)
            data = self.parent.show_column_relationships(self.parent.table)
            list_columns = self.parent.get_column_cursor_names()[1:]
            properties['columns'] = list_columns
            map(properties.delete, properties.get_children())
            for column in list_columns:
                properties.column(column,minwidth=25)
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