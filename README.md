## Atacks
1. Login without user password - attempt 1
	User: bob, Password: ' OR 1=1; #
	nie da się ponieważ pole $password jest haszowane
2. Login without user password -  attempt 2
	User: bob'; #

`SELECT * FROM users where username='bob' and password='5f4dcc3b5aa765d61d8327deb882cf99';` 
`bob'; #`
`SELECT * FROM products WHERE product_name LIKE ''; DROP DATABASE if exists sqlitraining -- // ';`



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
