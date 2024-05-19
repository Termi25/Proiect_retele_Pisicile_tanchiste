# Server si client pentru Executia paralela la distanta (tema 19):

## Comunicare broadcast:
1. Acesti clienti notifica la randul lor clientii lor cu privire la intrare unui nou client in cluster;

2. Server-ul la care se conecteaza un client notifica restul clientilor conectati cu privire la adresa si portul unde poate fi contactat clientul acceptat;

3. Server-ul lanseaza in exeutie metoda pe numarul de fire de executie solicitat de client si cu argumentele primite de la acesta;

4. Server-ul notifica toti clientii conectati la el pentru actualizarea gradului de incarcare cu procesarile primite sa le execute, 
precum si server-ul la care e el conectat, care atunci cand primeste notificarea in cauza, notifica la randul sau toti clientii care sunt conectati la el in acest sens;

5. Cand server-ul a obtinut rezultatul in urma executiei unui fir, il trimite clientului si notifica toti clientii conectati la el pentru actualizarea gradului sau de incarcare, 
acestia notificand la randul lor clientii conectati la ei;

## Procesare/comunicare client-server propriu-zisa:

1. Cand un client se deconecteaza, server-ul la care e conectat notifica toti clientii conectati la el, care la randul lor isi notifica si ei clientii conectati la ei.

2. Clientii incearca sa se conecteze pe rand la o lista de server-e, oprindu-se dupa ce reusesc sa se conecteze la primul;

3. Clientul este la randul sau server, iar cand se conectaza la un server, ii trimite portul pe care asculta la randul sau sa primeasca procesari;

4. Un client poate solicita serverului cu cel mai mic grad de incarcare sa execute pe un numar de fire de executie in paralele o metoda a unei clase care intoarce un anumit rezultat;

5. In cazul in care clasa respectiva nu se gaseste pe server-ul destinatie, clientul trimite continutul binar al clasei server-ului;
