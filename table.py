class Table:
    def __init__(self, name, schema, validate_input=True):
        self.name = name
        self.schema = schema
        self.rows = []
        if validate_input:
            self.validate_schema()

    def validate_schema(self):
        for column, col_type in self.schema.items():
            if col_type.startswith("enum("):
                allowed_values = col_type[5:-1].split(";")
                self.schema[column] = {"type": "enum", "values": allowed_values}
            elif col_type not in {"integer", "real", "char", "string", "email"}:
                raise ValueError(f"Unsupported type: {col_type}")

    def validate_row(self, row):
        if len(row) != len(self.schema):
            raise ValueError("Row length does not match table schema.")
        for (column, schema), value in zip(self.schema.items(), row):
            col_type = schema["type"] if isinstance(schema, dict) else schema
            if col_type == "integer" and not isinstance(value, int):
                raise ValueError(f"Value '{value}' must be an integer.")
            elif col_type == "real" and not isinstance(value, (float, int)):
                raise ValueError(f"Value '{value}' must be a real number.")
            elif col_type == "char" and (not isinstance(value, str) or len(value) != 1):
                raise ValueError(f"Value '{value}' must be a single character.")
            elif col_type == "string" and not isinstance(value, str):
                raise ValueError(f"Value '{value}' must be a string.")
            elif col_type == "email":
                import re
                if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
                    raise ValueError(f"Value '{value}' must be a valid email.")
            elif col_type == "enum" and value not in schema["values"]:
                allowed = ", ".join(schema["values"])
                raise ValueError(f"Value '{value}' must be one of: {allowed}")

    def add_row(self, row):
        self.validate_row(row)
        self.rows.append(row)

    def delete_row(self, index):
        if index < 0 or index >= len(self.rows):
            raise IndexError("Row index out of range.")
        del self.rows[index]

    def to_dict(self):
        return {"name": self.name, "schema": self.schema, "rows": self.rows}

    @staticmethod
    def from_dict(data):
        table = Table(data["name"], data["schema"], validate_input=False)
        table.rows = data["rows"]
        return table
