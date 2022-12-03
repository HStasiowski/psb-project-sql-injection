import streamlit as st

def db_restart():
    error_text = "Katastrofalny błąd 1"
    return False, error_text

def main():
    st.set_page_config(
        page_title="SQL Injection",
    )
    st.title("SQL Injection")

    st.subheader("Schemat bazy danych")

    st.subheader("Resetowanie bazy")
    st.text("")
    if st.button("Przywróc bazę"):
        result, error_text = db_restart()
        if result:
            st.success("Poprawnie przywrócono bazę")
        else:
            st.error("Nie udało się przywrócić bazy")
            st.text(error_text)
if __name__ == "__main__":
    main()