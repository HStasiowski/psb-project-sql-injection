import streamlit as st

def db_restart():
    error_text = "Katastrofalny błąd 1"
    return False, error_text

def main():
    st.set_page_config(
        page_title="SQL Injection"
    )
    st.title("SQL Injection")
    st.write("Często wykorzystywaną metodą ataku na aplikacje jest SQL Injection. Polega ona na wstrzyknięciu odpowiedniego polecenia, w niezabezpieczone pole tekstowe.")
    st.subheader("Schemat bazy danych")

    st.subheader("Resetowanie bazy")
    st.write("Po wykonaniu ćwiczeń, może się okazać że aplikcja nie będzie funkcjonować tak jak powinna (np. po usunięciu tabeli). W celu przywrócenia poprawnego działania trzeba skorzystać z funkcji przywracania bazy do stanu początkowego.")
    if st.button("Przywróc bazę"):
        result, error_text = db_restart()
        if result:
            st.success("Poprawnie przywrócono bazę")
        else:
            st.error("Nie udało się przywrócić bazy")
            st.text(error_text)
if __name__ == "__main__":
    main()