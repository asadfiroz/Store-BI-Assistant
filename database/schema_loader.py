from sqlalchemy import text

def get_schema_context(engine) -> str:
    schema_parts = []
    with engine.connect() as conn:
        tables = conn.execute(
            text("SELECT table_name FROM information_schema.tables WHERE table_schema = DATABASE()")
        ).fetchall()
        for (table,) in tables:
            columns = conn.execute(
                text(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name='{table}' AND table_schema=DATABASE()")
            ).fetchall()
            col_str = ", ".join([f"{c[0]} ({c[1]})" for c in columns])
            schema_parts.append(f"Table: {table}\nColumns: {col_str}")
    return "\n\n".join(schema_parts)
