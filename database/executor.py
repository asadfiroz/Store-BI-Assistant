import pandas as pd
from sqlalchemy import text

def execute_query(engine, sql: str):
    sql = sql.strip().rstrip(";")
    try:
        with engine.connect() as conn:
            df = pd.read_sql(text(sql), conn)
            return df, None
    except Exception as e:
        return None, str(e)
