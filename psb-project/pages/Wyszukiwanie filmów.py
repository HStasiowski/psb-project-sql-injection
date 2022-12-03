import streamlit as st
import pandas as pd
import numpy as np
#from psb_project import db

def db_restart():
    error_text = "Katastrofalny błąd 1"
    return False, error_text

def get_movies_table(title):
    table = pd.DataFrame(
    np.random.randn(10, 5),
    columns=('col %d' % i for i in range(5)))

    is_error = False
    querry_message = "test"
    return table, is_error, querry_message

def main():
    st.title("Wyszukiwanie filmów: ")
    title = st.text_input("Wprowadź tytuł lub aktora filmu: ")
    
    movies_table, is_error, querry_message = get_movies_table(title)

    if is_error:
        st.error(querry_message)
    else:
        st.table(movies_table.head(100))
    
    if len(movies_table) > 100: st.text("* Wynik został ograniczony do 100 wierszy.")
    st.sidebar.subheader("Przywracanie bazy do stanu początkowego")
    if st.sidebar.button("Przywróc bazę"):
        result, error_text = db_restart()
        if result:
            st.sidebar.success("Poprawnie przywrócono bazę")
        else:
            st.sidebar.error("Nie udało się przywrócić bazy")
            st.sidebar.text(error_text)

if __name__ == "__main__":
    main()