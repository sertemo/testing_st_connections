import streamlit as st
from sqlalchemy import text
from datetime import datetime, timedelta
import sqlite3
from sqlite3 import Cursor

st.set_page_config(
    page_icon="🏰",
    page_title="Testing SQL"
)

FILE_NAME = "fake_database.txt"
NOMBRE_DB_SQLITE = "dbsqlite.db"

class DatabaseManager:
    def __init__(self, db_filename):
        self.db_filename = db_filename

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_filename)
        return self.conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()

def guardar_sqlite(texto: str):
    with DatabaseManager(NOMBRE_DB_SQLITE) as c:
        c.execute("""
                  INSERT INTO textos_guardados (texto) VALUES (:texto);
                  """,
                  {"texto": texto})

def cargar_sqlite() -> Cursor:
    with DatabaseManager(NOMBRE_DB_SQLITE) as c:
        result = c.execute("""
                  SELECT texto from textos_guardados
                  """)
        query = result.fetchall()
    return query

def agregar_salto(numero:int=1):
    st.markdown(numero * """
                <br>
                """, unsafe_allow_html=True)

def guardar_en_txt(texto:str, filename:str=FILE_NAME):
    with open(filename, "ab") as f:
        f.write(f"{texto}\n".encode("utf-8"))
    st.rerun()

def cargar_txt(filename:str=FILE_NAME):
    try:
        with open(filename, "rb") as f:
            for linea in f.readlines():
                st.text(linea.decode("utf-8"))
    except FileNotFoundError:
        pass

def guardar_sql(conn, texto):
    with conn.session as s:
        s.execute(statement=text("CREATE TABLE IF NOT EXISTS textos_guardados (id INTEGER PRIMARY KEY AUTOINCREMENT, texto TEXT)"))
        s.execute(text(
            "INSERT INTO textos_guardados (texto) VALUES (:texto);"),
            params={"texto": texto}
        )
        s.commit()
    st.rerun()

def cargar_sql(conn)-> st.dataframe:
    df = conn.query('select * from textos_guardados')
    return df

def main():
    st.title("Testing SQL conections")

    # SQL con streamlit
    conn = st.experimental_connection(
    "local_db",
    type="sql",
    url="sqlite:///mydb.db",
    ttl=0.0
    #autocommit=True,
    )

    # SQLite (ejecutar solo una vez)
    #conn1 = sqlite3.connect(NOMBRE_DB_SQLITE)
    #c = conn1.cursor()
    #c.execute('''
    #CREATE TABLE IF NOT EXISTS textos_guardados (
    #    id INTEGER PRIMARY KEY AUTOINCREMENT,
    #    texto TEXT
    #)
    #''')
    #conn1.commit()
    #conn1.close()

    # Parte de SQL streamlit
    st.header(":blue[Gestión en SQL en streamlit]")
    contenedor_sql = st.container()
    with contenedor_sql:
        df = cargar_sql(conn)
        for id, texto in df.iterrows():
            st.text(texto["texto"])
        #st.dataframe(df, 
        #       use_container_width=True,
        #       hide_index=True,)
    
    with st.form("SQL Streamlit", clear_on_submit=True):
        texto_sql = st.text_input(
        "Escribe algo chachi",
        )

        escribir_sql = st.form_submit_button("Guardar SQL") 
        if escribir_sql and texto_sql:
            guardar_sql(conn, texto_sql)
            st.rerun()


    agregar_salto(3)

    # Parte de SQLite
    st.header(":green[Gestión en SQLite]")
    contenedor_sqlite = st.container()
    with contenedor_sqlite:
        results = cargar_sqlite()
        for item in results:
            st.text(item[0])
    
    with st.form("SQLite", clear_on_submit=True):
        texto_sqlite = st.text_input(
        "Escribe algo guay",
        )

        escribir_sqlite = st.form_submit_button("Guardar SQLite") 
        if escribir_sqlite and texto_sqlite:
            guardar_sqlite(texto_sqlite)
            st.rerun()
    
    agregar_salto(3)

    # Parte de archivo txt
    st.header(":violet[Gestión en txt]")
    contenedor_txt = st.container()
    with contenedor_txt:
        cargar_txt()

    with st.form("TXT", clear_on_submit=True):
        texto_txt = st.text_input(
            "Escribe algo chuli",
            )
        agregar_salto()
        escribir_txt = st.form_submit_button("Guardar txt")
        if escribir_txt and texto_txt:
            guardar_en_txt(texto_txt)




if __name__ == '__main__':
    main()