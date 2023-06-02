import hashlib

import streamlit as st

from psb_project.SQL_Injection import init_dellstore2_connection, init_user_and_containers, WARN_TEXT


def make_hash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


st.title("Logowanie")

st. info("""
Celem danego zadania jest zalogowanie się do systemu nie znając ani loginu, ani hasła żadnego z użytkowników. 

Po skutecznym zalogowaniu wyświetlony zostanie klucz poprawnie wykonanego zadania. Przy błędnym zalogowaniu zwrócony zostanie odpowiedni komunikat. Liczba prób logowania jest nieograniczona.
""")

if "postgres_port" not in st.session_state:
    st.warning(WARN_TEXT, icon="🚨")
    st.header("Inicjalizacja środowiska pracy")
    container_progress = st.progress(0, text="Tworzenie prywatnego środowiska...")
    init_user_and_containers(container_progress)
elif "user_id" not in st.session_state:
    init_user_and_containers()


st.session_state['db'] = init_dellstore2_connection()

username = st.text_input("Nazwa użytkownika")
password = st.text_input("Hasło", type='password')
if st.button("✅ Zaloguj się"):
    hashed_password = make_hash(password)
    result, is_error, text = st.session_state['db'].get_user(username, hashed_password)

    if result:
        st.success("""
        Poprawnie zalogowano!

        ```
        KITS{SQL_USER}
        ```
        """)
        st.balloons()
    else:
        if is_error:
            st.error("Błąd logowania")
            st.text(text)
        else:
            st.warning("Nie poprawne hasło/nazwa użytkownika!")


st.sidebar.subheader("Przywracanie bazy do stanu początkowego")
if st.sidebar.button("Przywróć bazę (3-5 sekund)", key="reset_db_login_tab"):
    st.session_state['db'].drop_tables()
    is_not_error, result = st.session_state['db'].fill_db()
    if is_not_error:
        st.sidebar.success(result)
    else:
        st.sidebar.error(result)
