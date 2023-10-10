import streamlit as st
from sqlalchemy import text
from datetime import datetime, timedelta

st.set_page_config(
    page_icon="🏰",
    page_title="Testing SQL"
)

FILE_NAME = "fake_database.txt"

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

    conn = st.experimental_connection(
    "local_db",
    type="sql",
    url="sqlite:///mydb.db",
    ttl=0.0
    #autocommit=True,
)

    # Parte de SQL
    st.header(":blue[Gestión en SQL]")
    contenedor_sql = st.container()
    with contenedor_sql:
        df = cargar_sql(conn)
        for id, texto in df.iterrows():
            st.text(texto["texto"])
        #st.dataframe(df, 
        #       use_container_width=True,
        #       hide_index=True,)
        
    col1, col2 = st.columns(2)
    with col1:
        texto_sql = st.text_input(
            "texto_sql",
            label_visibility="hidden",
            placeholder="Escribe tu texto",
            )
    with col2:
        agregar_salto()
        agregar_sql = st.button("Guardar sql")
        if agregar_sql and texto_sql:
            guardar_sql(conn, texto_sql)
            st.rerun()


    agregar_salto(3)


    # Parte de archivo txt
    st.header(":blue[Gestión en txt]")
    contenedor_txt = st.container()
    with contenedor_txt:
        cargar_txt()
    col1, col2 = st.columns(2)
    with col1:
        texto_txt = st.text_input(
            "texto_txt",
            label_visibility="hidden",
            placeholder="Escribe tu texto",
            )
    with col2:
        agregar_salto()
        agregar_txt = st.button("Guardar txt")
        if agregar_txt and texto_txt:
            guardar_en_txt(texto_txt)




if __name__ == '__main__':
    main()