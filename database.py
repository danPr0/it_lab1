import json

from table import Table


class Database:
    def __init__(self, name):
        self.name = name
        self.tables = {}

    def create_table(self, table_name, schema):
        if table_name in self.tables:
            raise ValueError("Table already exists!")
        self.tables[table_name] = Table(table_name, schema)

    def delete_table(self, table_name):
        if table_name not in self.tables:
            raise ValueError("Table not found!")
        del self.tables[table_name]

    def cross_product(self, table1_name, table2_name, result_table_name):
        if table1_name not in self.tables or table2_name not in self.tables:
            raise ValueError("One or both tables not found.")

        table1 = self.tables[table1_name]
        table2 = self.tables[table2_name]

        new_schema = {**table1.schema, **{f"{table2.name}.{col}": col_type for col, col_type in table2.schema.items()}}

        new_table = Table(result_table_name, new_schema, validate_input=False)

        for row1 in table1.rows:
            for row2 in table2.rows:
                new_table.add_row(row1 + row2)

        self.tables[result_table_name] = new_table
        return new_table

    def save_to_file(self, filepath):
        data = {table_name: table.to_dict() for table_name, table in self.tables.items()}
        with open(filepath, 'w') as f:
            json.dump({"name": self.name, "tables": data}, f)

    @staticmethod
    def load_from_file(filepath):
        with open(filepath, 'r') as f:
            data = json.load(f)
        db = Database(data["name"])
        for table_name, table_data in data["tables"].items():
            db.tables[table_name] = Table.from_dict(table_data)
        return db
