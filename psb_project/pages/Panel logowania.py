import hashlib
import streamlit as st

def make_hash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def main():
    st.title("Panel logowania")

    menu = ["Logowanie", "Rejestracja"]
    choice = st.selectbox("Wybór", menu)

    if choice == "Logowanie":
        st.subheader("Logowanie")
        username = st.text_input("Nazwa użytkownika")
        password = st.text_input("Hasło",type='password')
        if st.button("✅ Utwórz konto"):
            hashed_password = make_hash(password)
            result, is_error, text = st.session_state['db'].get_user(username, hashed_password)

            if result:
                st.success("Poprawnie zalogowano")
            else:
                if is_error:
                    st.error("Błąd logowania")
                    st.text(text)
                else:
                    st.warning("Nie poprawne hasło/nazwa użytkownika")
                
    elif choice == "Rejestracja":
        st.subheader("Utwórz nowe konto")
        firstname = st.text_input("Imię")
        lastname = st.text_input("Nazwisko")
        st.subheader("Dane do logowania")
        username = st.text_input("Nazwa użytkownika")
        password = st.text_input("Hasło",type='password')
        if st.button("✅ Utwórz konto"):
            hashed_password = make_hash(password)
            result, text = st.session_state['db'].insert_user(username, hashed_password, firstname, lastname)

            if result:
                st.success("Poprawnie utworzono nowe konto")
            else:
                st.warning("Nie poprawne hasło/nazwa użytkownika")
                st.text(text)

    if st.button("❔ Wskazówka SQL Injection"):
        st.write("Próbująć wstrzyknąć kod w panelu logowania, możemy wykorzystać pole tekstowe hasła. Wykorzystując metodę wstawiającą nowy warunek do zapytania.")
        st.code("' OR 1=1;--",language="sql")

    st.sidebar.subheader("Przywracanie bazy do stanu początkowego")
    if st.sidebar.button("Przywróc bazę"):
        st.session_state['db'].drop_tables()
        result = st.session_state['db'].fill_db()
        st.sidebar(result)

if __name__ == "__main__":
    main()