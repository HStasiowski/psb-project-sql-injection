import streamlit as st
from psb_project.SQL_Injection import init_connection

def db_restart():
    error_text = "Katastrofalny błąd 1"
    return False, error_text


def main():
    st.title("Wyszukiwanie filmów: ")
    title = st.text_input("Wprowadź tytuł lub aktora filmu: ")
    
    table, is_error, querry_message = st.session_state['db'].get_products(title)

    if is_error:
        st.error(querry_message)
    else:
        st.table(table.head(100))
    
    if len(table) > 100: st.text("* Wynik został ograniczony do 100 wierszy.")

    st.sidebar.subheader("Przywracanie bazy do stanu początkowego")
    if st.sidebar.button("Przywróc bazę"):
        st.session_state['db'].drop_tables()
        is_not_error, result = st.session_state['db'].fill_db()
        if is_not_error:
            st.sidebar.success(result)
        else:
            st.sidebar.error(result)

if __name__ == "__main__":
    st.session_state['db'] = init_connection()
    main()