import streamlit as st

from psb_project.SQL_Injection import init_dellstore2_connection, init_user_and_containers, WARN_TEXT

st.title("Wyszukiwanie filmów: ")

st. info("""
W prawidłowym trybie działania wyszukiwarka wyświetla filmy z tabeli `products`. Twoim zadaniem jest wyświetlenie użytkowników strony (z tabeli `customers`). 

Klucz do poprawnie wykonanego zadania znajdziesz w kolumnie `lastname` użytkownika o `customerid = 3`. 
""")

if "postgres_port" not in st.session_state:
    st.warning(WARN_TEXT, icon="🚨")
    st.header("Inicjalizacja środowiska pracy")
    container_progress = st.progress(0, text="Tworzenie prywatnego środowiska...")
    init_user_and_containers(container_progress)
elif "user_id" not in st.session_state:
    init_user_and_containers()
st.session_state['db'] = init_dellstore2_connection()

title = st.text_input("Wprowadź tytuł lub aktora filmu: ")

table, is_error, query_message = st.session_state['db'].get_products(title)

if is_error:
    st.error(query_message)
else:
    st.table(table.head(100))

if len(table) > 100:
    st.text("* Wynik został ograniczony do pierwszych 100 wierszy.")

st.sidebar.subheader("Przywracanie bazy do stanu początkowego")
if st.sidebar.button("Przywróć bazę (3-5 sekund)", key="reset_db_films_tab"):
    st.session_state['db'].drop_tables()
    is_not_error, result = st.session_state['db'].fill_db()
    if is_not_error:
        st.sidebar.success(result)
    else:
        st.sidebar.error(result)
