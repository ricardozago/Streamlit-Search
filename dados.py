import sqlite3
import pandas as pd
import time


def get_textos(texto_buscado):
    start_time = time.time()
    conn = sqlite3.connect("sqlite/textos.db")

    textos = pd.read_sql(
        f"""
    select * from textos
    where title LIKE '%{texto_buscado}%' or text LIKE '%{texto_buscado}%'
    """,
        conn,
    )

    conn.close()

    return textos, textos.shape[0], time.time() - start_time
