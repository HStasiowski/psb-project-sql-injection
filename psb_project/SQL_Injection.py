import configparser

import streamlit as st

import pandas as pd

from psb_project import db


@st.experimental_singleton
def init_connection():
    config = configparser.ConfigParser()
    config.read('./psb_project/config.ini')
    database = db.DellStoreDB()
    database.connect(**config["postgresql-dellstore2"])
    return database


def main():
    st.title("SQL Injection")
    st.write(
        "Często wykorzystywaną metodą ataku na aplikacje jest SQL Injection. Polega ona na wstrzyknięciu "
        "odpowiedniego polecenia w niezabezpieczone pole tekstowe.")

    st.header("Panel logowania")
    st.write("Jednym z najczęściej wykorzystywanych miejsc do wstrzyknięcia złośliwego kodu jest formularz logowania.")

    st.write(
        "Niezabezpieczone pole tekstowe w aplikacji przeważnie będzie składało się z zapytania do bazy podobnego do "
        "tego poniżej. Jest to najprostsze, a zarazem najbardziej niebezpieczne rozwiązanie, ponieważ zostawia lukę "
        "na wstrzyknięcie złośliwego kodu.")
    st.code("SELECT customerid FROM customers WHERE username = '$nazwa_uzytkownika' AND password = '$haslo';",
            language="sql")

    st.subheader("Wykonanie złośliwego polecenia")
    st.write(
        "Podstawiając odpowiednią sekwencję w pole nazwy użytkownika, można wymusić na bazie zrealizowanie innego "
        "polecenia.")
    st.code("$nazwa_uzytkownika = \"'; DROP TABLE customers; --\"", language="sql")
    st.write("SELECT po wstawieniu złośliwego kodu będzie wyglądał następująco:")
    st.code("SELECT customerid FROM customers WHERE username = ''; DROP TABLE customers; --' AND password = '$haslo';",
            language="sql")
    st.write(
        "Średnik (;) odpowiada za zakończenie poprzedniego zapytania do bazy. Kod po takim znaku przejdzie do "
        "wykonania polecenia DROP TABLE customers, które usunie tabelę klientów. Korzystając z podwójnego znaku pauzy "
        "(--) sprawimy, że pozostały kod zostanie oznaczony jako komentarz i nie wykona się.")

    st.subheader("Ominięcie hasła")
    st.write(
        "Osoba atakująca próbująca uzyskać dostęp do naszej aplikacji, może chcieć ominąć hasło. Można to uzyskać "
        "wpisując odpowiedni kod do pola hasła. Zapytanie do bazy sprawdza, czy podana nazwa użytkownika oraz "
        "hasło, zgadzają się z tymi zapisanymi w systemie. Wprowadzając zmiany do zapytania, możemy sprawić, że mimo "
        "złego hasła system nadal zaakceptuje logowanie.")
    st.code("$haslo = \"' OR 1=1;--\"", language="sql")
    st.write("SELECT po wstawieniu złośliwego kodu:")
    st.code("SELECT customerid FROM customers WHERE username = '$nazwa_uzytkownika' AND password = '' OR 1=1;--'",
            language="sql")
    st.write(
        "Znak apostrofu (') sprawi, że zapytanie przyjmie pusty ciąg znaków jako hasło oraz przejdzie do sprawdzania "
        "drugiego warunku (1=1 - jest zawsze prawdą). W tym przypadku mimo, że weryfikacja hasła zwróci FAŁSZ, "
        "to drugi warunek sprawi, że zapytanie zostanie wykonane i atakujący będzie mógł przejść dalej.")

    st.header("Schemat bazy danych")
    st.write(
        "Wykorzystany schemat bazy, to symulacja sklepu z filmami DELL Store 2, a aplikacja do ćwiczenia ataków jest "
        "oparta na bazie PostgreSQL. Panel logowania weryfikuje użytkowników na podstawie tabeli customers (username, "
        "password).")
    st.code("https://linux.dell.com/dvdstore/", language="uri")
    st.image("./schema_dark.png")

    st.header("Tabela użytkowników")
    st.write(
        "W bazie jest zarejestrowanych domyślnie 20 000 użytkowników. Przydzielone do nich hasła zostały wylosowane "
        "z listy najczęściej używanych oraz przydzielone użytkownikom w taki sposób, że pierwszy posiada "
        "najpopularniejsze, a ostatni najrzadsze.")
    st.subheader("Top 3 najczęściej przydzielone hasła do użytkowników.")
    col1, col2, col3 = st.columns(3)
    col1.metric("user1", "12345678")
    col2.metric("user2", "qwerty")
    col3.metric("user3", "111111")

    try:
        readable_passwords = pd.read_csv("./psb_project/dellstore2/database_readable_passwords.csv",
                                         delimiter=';', nrows=10)
    except Exception:
        st.error("Wystąpił błąd podczas wczytywania tabeli.")
    else:
        st.table(readable_passwords)

    st.header("Resetowanie bazy")
    st.write(
        "Po wykonaniu ćwiczeń, może się okazać, że aplikacja nie będzie funkcjonować tak jak powinna (np. po usunięciu "
        "tabeli). W celu przywrócenia poprawnego działania, trzeba skorzystać z funkcji przywracania bazy do stanu "
        "początkowego, znajdującego się w menu strony.")

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
