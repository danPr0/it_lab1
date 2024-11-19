from database import Database


import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog


class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.database = None
        self.current_table = None
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Database Management System")

        menu_frame = tk.Frame(self.root)
        menu_frame.pack(pady=10)

        tk.Label(menu_frame, text="Database Name:").grid(row=0, column=0, padx=5)
        self.db_name_entry = tk.Entry(menu_frame)
        self.db_name_entry.grid(row=0, column=1, padx=5)

        tk.Button(menu_frame, text="Create Database", command=self.create_database).grid(row=0, column=2, padx=5)
        tk.Button(menu_frame, text="Load Database", command=self.load_database).grid(row=0, column=3, padx=5)
        tk.Button(menu_frame, text="Save Database", command=self.save_database).grid(row=0, column=4, padx=5)

        table_frame = tk.Frame(self.root)
        table_frame.pack(pady=10)

        tk.Button(table_frame, text="Create Table", command=self.create_table).pack(side=tk.LEFT, padx=5)
        tk.Button(table_frame, text="Delete Table", command=self.delete_table).pack(side=tk.LEFT, padx=5)
        tk.Button(table_frame, text="Open Table", command=self.open_table).pack(side=tk.LEFT, padx=5)
        tk.Button(table_frame, text="Show Tables", command=self.show_tables).pack(side=tk.LEFT, padx=5)
        tk.Button(table_frame, text="Cross Product", command=self.cross_product_tables).pack(side=tk.LEFT, padx=5)

        row_frame = tk.Frame(self.root)
        row_frame.pack(pady=10)

        tk.Button(row_frame, text="Add Row", command=self.add_row).pack(side=tk.LEFT, padx=5)
        tk.Button(row_frame, text="Edit Row", command=self.edit_row).pack(side=tk.LEFT, padx=5)
        tk.Button(row_frame, text="Delete Row", command=self.delete_row).pack(side=tk.LEFT, padx=5)

        self.output_text = tk.Text(self.root, height=15, width=80, state=tk.DISABLED)
        self.output_text.pack(pady=10)

    def create_database(self):
        db_name = self.db_name_entry.get()
        if not db_name:
            messagebox.showerror("Error", "Database name cannot be empty!")
            return
        self.database = Database(db_name)
        self.current_table = None
        self.show_message(f"Database '{db_name}' created successfully!")

    def load_database(self):
        filepath = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if filepath:
            self.database = Database.load_from_file(filepath)
            self.current_table = None
            self.show_message(f"Database '{self.database.name}' loaded successfully!")

    def save_database(self):
        if not self.database:
            messagebox.showerror("Error", "No database loaded!")
            return
        filepath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if filepath:
            self.database.save_to_file(filepath)
            self.show_message(f"Database '{self.database.name}' saved successfully!")

    def create_table(self):
        if not self.database:
            messagebox.showerror("Error", "No database loaded!")
            return
        table_name = simpledialog.askstring("Create Table", "Enter table name:")
        if not table_name:
            return
        schema = simpledialog.askstring("Table Schema", "Enter schema (format: column:type, e.g., name:string, age:integer):")
        if not schema:
            return
        try:
            schema_dict = {col.split(":")[0]: col.split(":")[1] for col in schema.split(",")}
            self.database.create_table(table_name, schema_dict)
            self.show_message(f"Table '{table_name}' created successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_table(self):
        if not self.database:
            messagebox.showerror("Error", "No database loaded!")
            return
        table_name = simpledialog.askstring("Delete Table", "Enter table name to delete:")
        if not table_name:
            return
        try:
            self.database.delete_table(table_name)
            self.show_message(f"Table '{table_name}' deleted successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def open_table(self):
        if not self.database:
            messagebox.showerror("Error", "No database loaded!")
            return
        table_name = simpledialog.askstring("Open Table", "Enter table name to open:")
        if not table_name:
            return
        if table_name not in self.database.tables:
            messagebox.showerror("Error", f"Table '{table_name}' not found!")
            return
        self.current_table = self.database.tables[table_name]
        self.display_table()

    def show_tables(self):
        if not self.database:
            messagebox.showerror("Error", "No database loaded!")
            return
        tables = self.database.tables
        if not tables:
            self.show_message("No tables in the current database.")
        else:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"Tables in Database '{self.database.name}':\n")
            for table_name, table in tables.items():
                self.output_text.insert(tk.END, f"  - {table_name} (Columns: {', '.join(table.schema.keys())})\n")
            self.output_text.config(state=tk.DISABLED)

    def cross_product_tables(self):
        if not self.database:
            messagebox.showerror("Error", "No database loaded!")
            return
        table1_name = simpledialog.askstring("Cross Product", "Enter the first table name:")
        table2_name = simpledialog.askstring("Cross Product", "Enter the second table name:")
        result_table_name = simpledialog.askstring("Cross Product", "Enter the result table name:")
        if not table1_name or not table2_name or not result_table_name:
            return
        try:
            result_table = self.database.cross_product(table1_name, table2_name, result_table_name)
            self.show_message(f"Cross product table '{result_table_name}' created successfully!")
            self.current_table = result_table
            self.display_table()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_table(self):
        if not self.current_table:
            messagebox.showerror("Error", "No table selected!")
            return
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"Table: {self.current_table.name}\n")
        self.output_text.insert(tk.END, "Schema:\n")
        for column, col_type in self.current_table.schema.items():
            self.output_text.insert(tk.END, f"  {column} ({col_type})\n")
        self.output_text.insert(tk.END, "\nRows:\n")
        for row in self.current_table.rows:
            self.output_text.insert(tk.END, f"  {row}\n")
        self.output_text.config(state=tk.DISABLED)

    def add_row(self):
        if not self.current_table:
            messagebox.showerror("Error", "No table selected!")
            return
        try:
            schema = self.current_table.schema
            row = []
            for column, col_type in schema.items():
                value = simpledialog.askstring("Add Row", f"Enter value for '{column}' ({col_type}):")
                if col_type == "integer":
                    value = int(value)
                elif col_type == "real":
                    value = float(value)
                elif col_type == "char":
                    if len(value) != 1:
                        raise ValueError(f"Value for '{column}' must be a single character!")
                row.append(value)
            self.current_table.add_row(row)
            self.display_table()
            self.show_message("Row added successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def edit_row(self):
        if not self.current_table:
            messagebox.showerror("Error", "No table selected!")
            return
        try:
            index = simpledialog.askinteger("Edit Row", "Enter row index to edit (starting from 0):")
            if index < 0 or index >= len(self.current_table.rows):
                raise IndexError("Row index out of range!")

            schema = self.current_table.schema
            row = self.current_table.rows[index]
            updated_row = []
            for (column, col_type), value in zip(schema.items(), row):
                new_value = simpledialog.askstring("Edit Row", f"Current value for '{column}' ({col_type}): {value}")
                if not new_value:
                    updated_row.append(value)  # Keep old value if no input
                    continue
                if col_type == "integer":
                    new_value = int(new_value)
                elif col_type == "real":
                    new_value = float(new_value)
                elif col_type == "char":
                    if len(new_value) != 1:
                        raise ValueError(f"Value for '{column}' must be a single character!")
                updated_row.append(new_value)
            self.current_table.rows[index] = updated_row
            self.display_table()
            self.show_message("Row updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_row(self):
        if not self.current_table:
            messagebox.showerror("Error", "No table selected!")
            return
        try:
            index = simpledialog.askinteger("Delete Row", "Enter row index to delete (starting from 0):")
            self.current_table.delete_row(index)
            self.display_table()
            self.show_message("Row deleted successfully!")
        except IndexError:
            messagebox.showerror("Error", "Row index out of range!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_message(self, message):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, f"{message}\n")
        self.output_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()
