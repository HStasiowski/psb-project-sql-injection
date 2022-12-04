## Atacks
1. Login without user password - attempt 1
	User: bob, Password: ' OR 1=1; #
	nie da się ponieważ pole $password jest haszowane
2. Login without user password -  attempt 2
	User: bob'; #

`SELECT * FROM users where username='bob' and password='5f4dcc3b5aa765d61d8327deb882cf99';` 
`bob'; #`
`SELECT * FROM products WHERE product_name LIKE ''; DROP DATABASE if exists sqlitraining -- // ';`


## Jak ulepszyć kod tak, aby nie był już podatny na ataki? 
Łączenie się z bazą danych PostgreSQL i uruchomienie wszystkich kwerend w Pythonie wykonuje się w następujący sposób: 
```python
import psycopg2  
  
connection = psycopg2.connect(  
    host="127.0.0.1",  
    database="dellstore2",  
    user="sqlinjection",  
    password="3FS-DI"  
)  
with connection.cursor() as cursor:  
    cursor.execute("SELECT username, password FROM customers;")  
    print(cursor.fetchone())

# ('user1', '15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225')
```
Jedyne miejsce podatne na ataki SQL Injection w tym kodzie znajduje się w linijce dziesiątej: 
```python
	cursor.execute("SELECT username, password FROM customers;")  
```
Jeżeli nasz zapytanie przyjmuje jakieś dane od użytkownika, to nie mogą one być po prostu wklejone bez żadnej weryfikacji. Poniżej jest podany **BŁĘDNY** sposób przyjmowania argumenów użytkownika: 
```python
username = "user1"  
  
with connection.cursor() as cursor:  
    cursor.execute(f"SELECT firstname, lastname "  
                   f"FROM customers WHERE username='{username}';")  
    print(cursor.fetchone())
```
Czemu? A co się stanie, jeżeli zamiast `"user1"` użytkownik poda `"user1'; SELECT * FROM customers; --"`?  Wykona się następne polecenie SQL: 
```SQL
SELECT firstname, lastname FROM customers WHERE username='user1'; 
SELECT * FROM customers; 
--*"`
```
W takim przypadku użytkownik może dostać dowolne dane z bazy danych. Poprawnym zabezpieczeniem przed atakiem SQL Injection jest wykorzystanie specjalnych filtrów, które sprawdzają wartości otrzymane od użytkownika. W przypadku PostgreSQL i Pythona najprostszym rozwiązaniem jest użycie domyślnie dostępnej funkcji przekazywania parametrów: 
```python
username = "user1'; SELECT * FROM customers; --"

with connection.cursor() as cursor:  
    cursor.execute("SELECT firstname, lastname "  
                   "FROM customers WHERE username=%(checked_username)s;",  
                   {"checked_username": username})  
    print(cursor.fetchone())

# None
```
Jak widzimy, filtr skutecznie zablokował możliwość wyłowania takiego polecenia i zwróciło ono wartość `None`. 


## Config
### Postgres users
```
username: sqlinjection
password: 3FS-DI
```
### Tablespace
```
name: dbspace
location: /var/lib/postgresql/data
```
### Database
```
name: dellstore2
```



## Instructions
```
git clone https://github.com/FrightenedFox/psb-project-sql-injection
cd psb-project-sql-injection
pip install -e .
streamlit run psb_project/SQL_Injection.py
```
Aby uruchomić aplikacje i zamnąć konsolę (instrukcja [stąd](https://linuxize.com/post/how-to-run-linux-commands-in-background/)): 
```
streamlit run psb_project/SQL_Injection.py &
disown %1
```
gdzie `1`  oznacza numer procesu w tle, można otrzymać wpisując `jobs -l`.



## Sources
1. [SQL injection examples for practice](https://thehackerish.com/sql-injection-examples-for-practice/)  - OWASP training 
2. [SQL Injection Exercise](https://research.cs.wisc.edu/mist/SoftwareSecurityCourse/Exercises/3.8.1_SQL_Injection_Exercise.html) - VirtualBox Image (not working: kernel panic)
3. [Lab - SQL Injection ](http://sweet.ua.pt/jpbarraca/course/sio-2122/lab-sql-injection/) - Docker image (on linux)



## TODO
- [ ] ~~Poprawić relacje w bazie danych~~
- [x] Podmienić hasła
- [x] Automatycznie wyczyszczenie na panelu logowania (zmiana logowanie/rejestreacja)
- [x] Inna nazwa przycisku załóż konto
- [x] Zmienić "niepoprawna nazwa" na "taki użytkownik już istnieje"
- [x] Pozwolić początek pracy z dowolnej strony
- [ ] Podać w Streamlit/dokumentacji pierwsze 10 wierszy z pliku `psb_project/dellstore2/database_readable_passwords.csv`, żeby można było testować hasła rzeczywistych już istniejących użytkowników. Można również powiedzieć, że hasła zostały przydzielone użytkownikom w kolejności zmniejszenia się ich popularności (user1 - najbardziej popularne, user20000 - najmniej popularne); jednak nie są to najpopularjniejsze hasła (po prostu losowo wybrane ze zbioru danych najpopularnieszych). 
- [x] Opisać co trzeba zmienić w kodzie, aby nie był podatny na ataki SQL Injection.
- [ ] *(jako pomysł, jeżeli będzie mało tego, co zrobiliśmy)* Dodać przełącznik na tryb zabezpieczony, w którym kod już jest dobrze napisany i nie da się zaatakować przez SQL Inection.
- [ ] Na zakładce "Wyszukiwarka filmów" raczej dobrze by było podnieść tą wskazówke SQL Inection do góry, bo na dole tam nikt jej nie znajdzie.
- [ ] Wskazówka na stronie logowania nie działa, bo używamy funkcji haszującej. 
- [ ] 

