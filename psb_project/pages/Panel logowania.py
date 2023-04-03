import hashlib

import sqlite3

import streamlit as st

from psb_project.SQL_Injection import init_connection


def make_hash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def main():
    if "user_id" not in st.session_state:
        conn = sqlite3.connect('connections.db')
        cursor = conn.cursor()
        outcome = cursor.execute("insert into user default values returning id;")
        st.session_state.user_id = outcome.fetchone()[0] 
        conn.commit()
        conn.close()

    st.title("Panel logowania")

    menu = ["Logowanie", "Rejestracja"]
    choice = st.selectbox("Wybór", menu)

    if choice == "Logowanie":
        st.subheader("Logowanie")
        username = st.text_input("Nazwa użytkownika")
        password = st.text_input("Hasło", type='password')
        if st.button("✅ Zaloguj się"):
            hashed_password = make_hash(password)
            result, is_error, text = st.session_state['db'].get_user(username, hashed_password)

            if result:
                st.success("Poprawnie zalogowano")
            else:
                if is_error:
                    st.error("Błąd logowania")
                    st.text(text)
                else:
                    st.warning("Nie poprawne hasło/nazwa użytkownika!")

    elif choice == "Rejestracja":
        st.subheader("Utwórz nowe konto")
        firstname = st.text_input("Imię")
        lastname = st.text_input("Nazwisko")
        st.subheader("Dane do logowania")
        register_username = st.text_input("Nazwa użytkownika")
        register_password = st.text_input("Hasło", type='password')
        username = register_username
        password = register_password
        if st.button("✅ Utwórz konto"):
            hashed_password = make_hash(register_password)
            result, text = st.session_state['db'].insert_user(register_username, hashed_password, firstname, lastname)

            if result:
                st.success("Poprawnie utworzono nowe konto")
            else:
                st.warning("Taki użytkownik już istnieje!")
                st.text(text)

    if st.button("❔ Wskazówka SQL Injection"):
        st.write(
            "Próbując wpisać kod w panelu logowania, możemy wykorzystać pole tekstowe nazwy użytkownika. Używając "
            "metody "
            "wstawiającej nowy warunek do zapytania.")
        st.code("' OR 1=1;--", language="sql")

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
