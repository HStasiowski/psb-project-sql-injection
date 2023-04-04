import streamlit as st

import sqlite3

from psb_project.SQL_Injection import init_connection


def db_restart():
    error_text = "Katastrofalny błąd 1"
    return False, error_text


def main():
    if "user_id" not in st.session_state:
        conn = sqlite3.connect('connections.db')
        cursor = conn.cursor()
        outcome = cursor.execute("insert into user default values returning id;")
        st.session_state.user_id = outcome.fetchone()[0] 
        conn.commit()
        conn.close()
    st.title("Wyszukiwanie filmów: ")
    title = st.text_input("Wprowadź tytuł lub aktora filmu: ")

    table, is_error, query_message = st.session_state['db'].get_products(title)

    if st.button("❔ Wskazówka SQL Injection", key="wskazowka_sql_injection"):
        st.write(
            "Wpisanie kodu w tym przypadku może odbyć się poprzez ucieczkę z warunków LIKE. Możemy następnie "
            "wykorzystać nowe zapytanie, zawierające np. prośbę o wyświetlenie tabeli klientów.")
        st.code("')); SELECT * FROM customers; --", language="sql")

    if is_error:
        st.error(query_message)
    else:
        st.table(table.head(100))

    if len(table) > 100:
        st.text("* Wynik został ograniczony do 100 wierszy.")

    st.sidebar.subheader("Przywracanie bazy do stanu początkowego")
    if st.sidebar.button("Przywróć bazę"):
        st.session_state['db'].drop_tables()
        is_not_error, result = st.session_state['db'].fill_db()
        if is_not_error:
            st.sidebar.success(result)
        else:
            st.sidebar.error(result)


if __name__ == "__main__":
    st.session_state['db'] = init_connection()
    main()
