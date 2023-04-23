Nume: Florian Silviu-Gabriel
Grupă: 333CC

# Tema <1> 

Organizare
1. Explicație pentru soluția aleasă:

Pentru managementul produselor, coșurilor de cumpărături și al producerilor am
folosit următoarele dicționare:
* product_pool: {nume_produs : (produs, [id_producer])}
  - stochează toate produsele, o intrare din dicționar are cheia numele
  produsului(deoarece acesta este unic pentru fiecare produs) iar că valoare
  am folosit un tuplu cu obiectul produs în sine că primul element, și o lista
  cu id-urile producerilor că al doilea
* producer_queue_size: {id_producer : nr_produse}
  - dicționar care stochează lungimea queue-ului fiecărui producer în parte,
  cheia este id-ul producerului iar valoarea este lungimea cozii de produse
* cart_list: {cos_id : {nume_produs : (produs, [id_producer])}}
  - stochează toate coșurile de cumpărături, cheia este id-ul cosului iar
  valoarea este alt dictionar care reprezinta lista de produse din cos
  - fiecare lista de produse este in sine un dictionar, care are aceeasi
  logica ca product_pool, dictionar cu nume produs si tuplu cu obiectul produs
  si o lista cu id-urile producerilor

Producer:
* producer-ul are un loop infinit in care adauga produse cat timp aplicatia
  este activa
* in acest loop trece prin fiecar element din lista de produse primita
* pentru fiecare produs din lista, apeleaza publish[1] de atatea ori cat
  numarul de la quantity
* dupa fiecare apelare de publish[1], se face un sleep, cu un anumit timp
  


***Obligatoriu:*** 


* De făcut referință la abordarea generală menționată în paragraful de mai sus. Aici se pot băga bucăți de cod/funcții - etc.
* Consideri că tema este utilă?
da
* Consideri implementarea naivă, eficientă, se putea mai bine?

***Opțional:***


* De menționat cazuri speciale, nespecificate în enunț și cum au fost tratate.


Implementare
-

* De specificat dacă întregul enunț al temei e implementat
* Dacă există funcționalități extra, pe lângă cele din enunț - descriere succintă + motivarea lor
* De specificat funcționalitățile lipsă din enunț (dacă există) și menționat dacă testele reflectă sau nu acest lucru
* Dificultăți întâmpinate
* Lucruri interesante descoperite pe parcurs


Resurse utilizate
-

* Resurse utilizate - toate resursele publice de pe internet/cărți/code snippets, chiar dacă sunt laboratoare de ASC

Git
-
1. Link către repo-ul de git

Ce să **NU**
-
* Detalii de implementare despre fiecare funcție/fișier în parte
* Fraze lungi care să ocolească subiectul în cauză
* Răspunsuri și idei neargumentate
* Comentarii (din cod) și *TODO*-uri

Acest model de README a fost adaptat după [exemplul de README de la SO](https://github.com/systems-cs-pub-ro/so/blob/master/assignments/README.example.md).