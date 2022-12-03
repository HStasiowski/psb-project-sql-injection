import hashlib
import streamlit as st

def db_restart():
    error_text = "Katastrofalny błąd 1"
    return False, error_text

def make_hash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def login(username, password):
    #should return TRUE, FALSE
    querry_message = "test"
    return False, querry_message

def register(username, password, firstname, lastname):
    #Password and name validation
    #should return TRUE, FALSE
    querry_message = "test"
    return True , querry_message

def main():
    st.title("Panel użytkownika")

    menu = ["Logowanie", "Rejestracja"]
    choice = st.selectbox("Wybór", menu)

    if choice == "Logowanie":
        st.subheader("Logowanie")
        username = st.text_input("Nazwa użytkownika")
        password = st.text_input("Hasło",type='password')
        if st.button("✅ Utwórz konto"):
            hashed_password = make_hash(password)
            result, text = login(username, hashed_password)

            if result:
                st.success("Poprawnie zalogowano")
            else:
                st.warning("Nie poprawne hasło/nazwa użytkownika")
                st.text(text)
                
    elif choice == "Rejestracja":
        st.subheader("Utwórz nowe konto")
        firstname = st.text_input("Imię")
        lastname = st.text_input("Nazwisko")
        st.subheader("Dane do logowania")
        username = st.text_input("Nazwa użytkownika")
        password = st.text_input("Hasło",type='password')
        if st.button("✅ Utwórz konto"):
            hashed_password = make_hash(password)
            result, text = register(username, hashed_password, firstname, lastname)

            if result:
                st.success("Poprawnie utworzono nowe konto")
            else:
                st.warning("Nie poprawne hasło/nazwa użytkownika")
                st.text(text)

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