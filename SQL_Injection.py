import configparser
import sqlite3
import subprocess
import random 

import pandas as pd
import streamlit as st

from psb_project import db


ERROR_TEXT = """
Niestety coś poszło nie tak! 
Spróbuj kliknąć przycisk `R`. Jeżeli problem nie zniknie, całkiem restartuj stronę (`F5`)...
"""
WARN_TEXT = """
**Zalecenia na temat użycia strony:**
 - pozostań na danej podstronie do końca inicjalizacji środowiska pracy (1-2 minuty), aby uniknąć późniejszych problemów;
 - nie odświeżaj strony, aby nie stracić swojej pracy (chyba, że strona się zacięła i nie ma innego wyjścia);
 - aby odświeżyć stronę w bezpieczny sposób kliknij przycisk `R` lub użyj odpowiedniej opcji w prawym górnym menu 🍔;
 - jeżeli zepsułeś bazę danych i chciałbyś ją przywrócić: użyj odpowiedniego przycisku po lewej stronie (pojawi się po zakończeniu inicjalizacji środowiska). 
"""


def make_sure_it_runs(command: list):
    counter = 0
    retcode = 2
    while retcode == 2:
        retcode = subprocess.run(command).returncode
        if retcode == 2:
            sleep_time = random.randint(3, 6)
            subprocess.run(["sleep", f"{sleep_time}"])
        counter += 1
        if counter > 10:
            st.error(ERROR_TEXT)
            break
        

def init_user_and_containers(progress_bar=None):
    if "user_id" not in st.session_state or "postgres_port" not in st.session_state:
        # Get user id from DB
        conn = sqlite3.connect("psb_project/connections-db/connections.db")
        cursor = conn.cursor()

        counter = 0
        err = True
        while err: 
            try:
                outcome = cursor.execute("INSERT INTO user DEFAULT VALUES RETURNING id;")
            except sqlite3.OperationalError:
                sleep_time = random.randint(3, 6)
                subprocess.run(["sleep", f"{sleep_time}"])
                err = True
                print("Database is closed...")
            else:
                err = False
                st.session_state.user_id = outcome.fetchone()[0]
            counter += 1
            if counter > 10:
                st.error(ERROR_TEXT)
                break
            
        conn.commit()
        conn.close()

    if "postgres_port" not in st.session_state:
        # Create Docker container for this user
        con_name = f"injection-user-{st.session_state.user_id:03d}"
        ret = subprocess.run(["docker", "run", "--name", con_name, "-e", "POSTGRES_PASSWORD=123456", "-d", "-p",
                        f"55{st.session_state.user_id:03d}:5432", "psb-injection"])
        print(ret)
        if progress_bar is not None:
            progress_bar.progress(30, "Łączenie się ze środowiskiem...")
        sleep_time = random.randint(7, 23)
        subprocess.run(["sleep", f"{sleep_time}"])
        if progress_bar is not None:
            progress_bar.progress(60, "Inicjalizacja bazy danych...")
        make_sure_it_runs(["docker", "exec", con_name, "psql", "-U", "postgres", "-d", "postgres", "-q", "-f",
                        "/usr/src/app/setup_dellstore2.sql"])
        if progress_bar is not None:
            progress_bar.progress(80, "Wypełnianie bazy danych...")
        make_sure_it_runs(["docker", "exec", con_name, "psql", "-U", "sqlinjection", "-d", "dellstore2", "-q", "-f",
                        "/usr/src/app/dellstore2-normal-1.0.sql"])
        if progress_bar is not None:
            progress_bar.progress(100, "System gotowy do pracy!")
        st.session_state.postgres_port = int(f"55{st.session_state.user_id:03d}")


def init_dellstore2_connection():
    config = configparser.ConfigParser()
    config.read("./psb_project/config.ini")
    database = db.DellStoreDB()
    database.connect(port=st.session_state.postgres_port, **config["postgresql-dellstore2"])
    return database


st.title("SQL Injection")
st.write(
    "Często wykorzystywaną metodą ataku na aplikacje jest SQL Injection. Polega ona na wstrzyknięciu "
    "odpowiedniego polecenia w niezabezpieczone pole tekstowe.")

st.warning(WARN_TEXT, icon="🚨")

container_progress = None
if "postgres_port" not in st.session_state:
    st.header("Inicjalizacja środowiska pracy")
    container_progress = st.progress(10, text="Tworzenie prywatnego środowiska...")

st.header("Wprowadzenie teoretyczne")
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
st.code("SELECT customerid FROM customers WHERE username = ''; DROP TABLE customers CASCADE; --' AND password = '$haslo';",
        language="sql")
st.write(
    "Średnik (;) odpowiada za zakończenie poprzedniego zapytania do bazy. Kod po takim znaku przejdzie do "
    "wykonania polecenia DROP TABLE customers, który usunie tabelę klientów. Korzystając z podwójnego znaku pauzy "
    "(--) sprawimy, że pozostały kod zostanie oznaczony jako komentarz i nie wykona się.")

st.header("Schemat bazy danych")
st.write(
    "Wykorzystany schemat bazy, to symulacja sklepu z filmami DELL Store 2, a aplikacja do ćwiczenia ataków jest "
    "oparta na bazie PostgreSQL. Panel logowania weryfikuje użytkowników na podstawie tabeli customers (username, "
    "password).")
st.code("https://linux.dell.com/dvdstore/", language="uri")
st.image("./psb_project/dellstore2/schema_dark.png")

st.header("Resetowanie bazy")
st.write(
    "Po wykonaniu ćwiczeń, może się okazać, że aplikacja nie będzie funkcjonować tak jak powinna (np. po usunięciu "
    "tabeli). W celu przywrócenia poprawnego działania, trzeba skorzystać z funkcji przywracania bazy do stanu "
    "początkowego, znajdującego się w menu strony.")

init_user_and_containers(container_progress)
st.session_state["db"] = init_dellstore2_connection()

st.sidebar.subheader("Przywracanie bazy do stanu początkowego")
if st.sidebar.button("Przywróć bazę (3-5 sekund)", key="reset_db_home_tab"):
    st.session_state["db"].drop_tables()
    is_not_error, result = st.session_state["db"].fill_db()
    if is_not_error:
        st.sidebar.success(result)
    else:
        st.sidebar.error(result)
