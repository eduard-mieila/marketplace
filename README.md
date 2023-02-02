# Marketplace

## Descriere generală
Pe acest repo găsim o implementare de Marketplace prin intermediul căruia mai mulți producători își vor oferi produsele spre vânzare, iar mai mulți cumpărători vor achiziționa produsele puse la dispoziție. Aplicația rezolvă o problemă clasică: Multi-Producer Multi-Consumer.

## How to run
Pentru demonstrație se pot folosi fișierele din folderul checker. Pentru a efectua o serie de teste, se va foosi scriptul run_tests.sh.

## Informații suplimentare despre implementare

### Marketplace
Marketplace va folosi:
- prod - un dicționar ce va conține cozile de producție ale fiecărui producător
- prod_lock - lock pentru prod
- prod_id - un contor pentru id-ul producatorilor
- prod_id_lock - lock pentru prod_id
- cons_id - un contor pentru id-ul consumatorilor
- cons_id_lock - lock pentru cons_id
- carts - un dicționar cu liste de tupluri [id_producător, produs]
- carts_lock - lock pentru carts
- carts_max_cap - capacitatea maximă a unei cozi de producție

register_producer și new_cart vor fi metode ce vor incrementa variabile în mod sigur pentru rularea paralelă.

Metoda publish va căuta producătorul, va verifica dacă acesta are coada de producție plină, iar dacă nu o are, va adăuga produsul. Metoda va bloca resursa prod pentru a nu suferi modificari din alt thread.

Metoda add_to_cart va căuta primul producător care are în coada de producție produsul dorit, nu înainte de a bloca lock-ul pentru prod. Imediat ce a găsit produsul, va bloca și resursa carts și va adăuga produsul în coșul dorit, după care va elimina produsul din coada de producție. La final se vor elibera cele 2 lock-uri. Dacă produsul nu este găsit, se va returna false.

Metoda remove_from_cart va căuta produsul în coș, nu înainte de a bloca resursa carts, o va elimina din coș, va bloca resursa prod și va adăuga înapoi produsul în coada de producție. La final, eliberează lock-urile.

Metoda place_order returnează toate produsele dintr-un coș sub formă de listă.

### Producer
Producer va folosi toate datele ca parametru în constructor.

Metoda sa run va rula în buclă infintă, producând elementele specifice unui producător la timpii dați ca parametru. Dacă nu se poate adăuga un element, se așteaptă.

### Consumer
Consumer va folosi toate datele ca parametru în constructor.

Metoda sa run va lua câte un coș de cumpărături pe rând, va rula toate comenzile primite, așteptând acolo unde este cazul. La final, va plasa comanda prin place_order din marketplace și va afișa mesajele necesare.
