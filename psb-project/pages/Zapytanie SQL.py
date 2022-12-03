import streamlit as st
import pandas as pd
import numpy as np

def get_movies_table(title):
    table = pd.DataFrame(
    np.random.randn(10, 5),
    columns=('col %d' % i for i in range(5)))

    is_error = False
    querry_message = "test"
    return table, is_error, querry_message

def main():
    st.subheader("Wyszukiwanie filmów: ")
    title = st.text_input("Wprowadź tytuł filmu: ")
    
    movies_table, is_error, querry_message = get_movies_table(title)

    if is_error:
        st.error(querry_message)
    else:
        st.table(movies_table)

if __name__ == "__main__":
    main()