Nume: Florian Silviu-Gabriel
Grupă: 333CC

# Tema <1> 

## Organizare
1. Explicație pentru soluția aleasă:

Pentru managementul produselor, coșurilor de cumpărături și al producerilor am
folosit următoarele dicționare:
* [product_pool]
  - stochează toate produsele, o intrare din dicționar are cheia numele
  produsului(deoarece acesta este unic pentru fiecare produs) iar că valoare
  am folosit un tuplu cu obiectul produs în sine că primul element, și o lista
  cu id-urile producerilor că al doilea
* [producer_queue_size]
  - dicționar care stochează lungimea queue-ului fiecărui producer în parte,
  cheia este id-ul producerului iar valoarea este lungimea cozii de produse
* [cart_list]
  - stochează toate coșurile de cumpărături, cheia este id-ul coșului iar
  valoarea este alt dicționar care reprezintă lista de produse din coș
  - fiecare lista de produse este în sine un dicționar, care are aceeași
  logica că product_pool, dicționar cu nume produs și tuplu cu obiectul produs
  și o lista cu id-urile producerilor

Producer:
* producer-ul are un loop infinit în care adaugă produse cât timp aplicația
  este activă
* în init voi retine un id obținut apelând funcția [register_producer]
* în acest loop trece prin fiecare element din lista de produse primită
* pentru fiecare produs din lista, apelează [publish] de atâtea ori cât
  numărul de la quantity
* după fiecare apelare de [publish], se face un sleep, cu un anumit timp
  pentru atunci când nu poate adăuga un produs sau timpul de așteptare pentru
  publicarea celuilalt produs

Consumer:
* în consumer pentru fiecare cart am generat un id folosind funcția [new_cart]
* am trecut prin fiecare operație din cart am apelat [add_to_cart] sau 
  [remove_from_cart] în funcție de tipul operației
* am făcut asta de n ori în funcție de field-ul quantity din operație
* atunci când [add_to_cart] întoarce False(când nu se găsește produsul), se
  face un sleep și se resetează iterația pentru a reincerca adăugarea în cart
* după ce am obținut toate produsele, se apelează [place_order] pentru a obține
  toate elementele cartului, acestea se afișează corespunzător

Sincronizare:
* pentru a sincroniza thread-urile, am folosit câte un mutex pentru
  modificarea variabilelor de queue_size ale producerilor și altul
  pentru printarea rezultatelor din consumer
* operațiile de adăugare și scoatere din liste și dicționare sunt thread-safe
  deci nu am folosit mecanisme de sincronizare pentru acestea

Unit testing:
* am implementat modulul de unit testing pentru toate funcțiile din marketplace

Logging:
* am implementat logging pentru toate funcțiile din marketplace

## Referine:

[product_pool]: {nume_produs : (produs, [id_producer])}

[producer_queue_size]: {id_producer : nr_produse}

[cart_list]: {cos_id : {nume_produs : (produs, [id_producer])}}

[uuid]: https://docs.python.org/3/library/uuid.html

[publish]:
'''python
    def publish(self, producer_id, product):
        if self.producer_queue_size[producer_id] >= self.queue_size_per_producer:
            return False
        if product.name not în self.product_pool:
            self.product_pool[product.name] =(product, [producer_id])
        else:
            self.product_pool[product.name][1].append(producer_id)
        with self.lock_modify_sizes[producer_id]:
            self.producer_queue_size[producer_id] += 1
        return True
'''

[register_producer]:
'''python
    def register_producer(self):
        producer_id = str(uuid.uuid4())
        self.producer_queue_size[producer_id] = 0
        self.lock_modify_sizes[producer_id] = threading.Lock()
        return producer_id
'''

[new_cart]:
'''python
    def new_cart(self):
        cart_id = int(uuid.uuid4())
        self.cart_list[cart_id] = {}
        return cart_id
'''

[add_to_cart]:
'''python
    def add_to_cart(self, cart_id, product):
        if product.name not în self.product_pool or len(self.product_pool[product.name][1]) == 0:
            return False

        producer_id = self.product_pool[product.name][1].pop()
        with self.lock_modify_sizes[producer_id]:
            self.producer_queue_size[producer_id] -= 1

        if product.name not în self.cart_list[cart_id]:
            self.cart_list[cart_id][product.name] = (product, [producer_id])
        else:
            self.cart_list[cart_id][product.name][1].append(producer_id)
      
        return True
'''

[remove_from_cart]:
'''python
    def remove_from_cart(self, cart_id, product):
        producer_id = self.cart_list[cart_id][product.name][1].pop()
        with self.lock_modify_sizes[producer_id]:
            self.producer_queue_size[producer_id] += 1
        self.product_pool[product.name][1].append(producer_id)
'''

[place_order]:
'''python
    def place_order(self, cart_id):
        cart_products = []
        for (_,(product_cart, producer_id_list)) în self.cart_list[cart_id].items():
            for _ în producer_id_list:
                cart_products.append(product_cart)
        return cart_products
'''

* Consideri că tema este utilă?
  Consider că tema m-a ajutat să învăț mai bine python

* Consideri implementarea naivă, eficientă, se putea mai bine?
  Consider implementarea destul de eficientă având în vedere că toate căutările
  sunt în dicționare și nu folosesc iterari prin liste, cu excepția preluării
  listei de cumpărături din funcția [place_order]

## Implementare
  * Am implementat întregul enunț al temei
  * Câteva edge-case uri nespecificate în enunț și netratate în teste:
    * Ce se întâmplă dacă un producer are spre exemplu un queue limit de 2
    adaugă 2 produse, acesta se umple, iar unul dintre consumatori va face
    [remove_from_cart]? Size-ul queue-ul producerului crește? Se adaugă tot 
    în lista lui? Nu se lasă să se dea remove? Eu am considerat că se poate
    adaugă în lista lui, iar queue-ul se va incrementa peste limită
    * E posibil că un consumer să dea remove la un produs care nu există în
    coș? Am considerat că nu se va ajunge la acest caz

  * Dificultăți întâmpinate
    * Am stat câteva ore să îmi dau seama că producerii vor genera în continuu
      produse, și nu doar o singura data produsele din lista sa cu cantitățile
      lor, nu cred că a fost destul de explicit enunțul în legătură cu asta.
    * Chiar daca se înțelege, sugerez ca în enunț să fie specificat că fiecare
      consumer are coșurile sale, care nu se împart între consumeri
    * Mi-a luat ceva timp să printez și să îmi dau seama care e input-ul primit
      la consumeri și produceri(lista de produse) deoarece în json e diferit,
      de exemplu în json există un id al produsului care nu există la input
    * *Nu iau punctaj maxim pe linting din cauza unei erori ale unui import
      care e pus bine*
  * Lucruri interesante descoperite pe parcurs
    Am aflat cum funcționează funcția print în python, are un buffer și nu
    face printarea pe loc, am avut un bug cu un loop infinit în care nu funcționa
    printarea, doar cu opțiunea flush=True

## Resurse utilizate
https://docs.python.org
https://ocw.cs.pub.ro/courses/asc/laboratoare/03
https://stackoverflow.com
https://www.geeksforgeeks.org
https://ocw.cs.pub.ro/courses/asc/teme/tema1
https://curs.upb.ro/2022/mod/forum/view.php?id=144437
https://gitlab.cs.pub.ro/asc/asc-public

## Git
https://github.com/Silviuf19/producer-consumer