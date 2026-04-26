# Restorano valdymo sistema

## Objektinio programavimo kursinio darbo ataskaita

---

## 1. Įvadas

Šio kursinio darbo tikslas – sukurti programinę sistemą, kuri praktiškai pritaiko objektinio programavimo (OOP) principus, dizaino šablonus, kompozicijos ir agregacijos principus, duomenų saugojimą bei testavimą. Šio darbo metu buvo siekiama ne tik sukurti veikiančią programą, bet ir aiškiai suprasti, kaip skirtingos sistemos dalys tarpusavyje sąveikauja.

Pasirinkta tema – restorano valdymo sistema. Ši tema yra tinkama objektiniam programavimui, nes realiame restorane egzistuoja daug tarpusavyje susijusių objektų: meniu elementai, stalai, užsakymai ir pats restoranas. Kiekvienas iš šių objektų turi savo duomenis ir funkcijas, todėl juos patogu modeliuoti naudojant klases.

Sukurta programa leidžia vartotojui:
- peržiūrėti meniu;
- pridėti ir pašalinti meniu elementus;
- peržiūrėti stalus;
- rezervuoti ir atlaisvinti stalus;
- sukurti naują užsakymą;
- peržiūrėti užsakymus;
- uždaryti užsakymą;
- apskaičiuoti bendras pajamas;
- išsaugoti ir įkelti duomenis iš JSON failo.

Programa parašyta Python programavimo kalba ir veikia per tekstinę vartotojo sąsają (komandinėje eilutėje).

### Programos paleidimas

```bash
python restaurant_system.py
```

### Testų paleidimas

```bash
python -m unittest
```

---

## 2. Sistemos analizė ir struktūra

Sistema sudaryta iš kelių pagrindinių klasių, kurios kiekviena atlieka konkrečią funkciją:

- `MenuItem` – abstrakti bazinė klasė, apibrėžianti bendrą meniu elemento struktūrą;
- `FoodItem` – maisto klasė;
- `DrinkItem` – gėrimų klasė;
- `OrderItem` – klasė, aprašanti vieną užsakymo elementą;
- `Order` – klasė, aprašanti visą užsakymą;
- `OrderBuilder` – klasė, naudojama užsakymo kūrimui;
- `Table` – klasė, aprašanti restorano stalą;
- `Restaurant` – pagrindinė klasė, valdanti visą sistemą.

Tokios struktūros pasirinkimas leidžia aiškiai atskirti atsakomybes. Pavyzdžiui, `MenuItem` klasė atsakinga tik už meniu elementus, `Order` – už užsakymo logiką, o `Restaurant` – už bendrą sistemos veikimą.

`Restaurant` klasė saugo visus sistemos duomenis:

```python
self.menu = []
self.orders = []
self.tables = []
```

Tai reiškia, kad visa sistemos būsena yra valdoma vienoje vietoje.

---

## 3. Objektinio programavimo principai

Šiame projekte panaudoti visi keturi pagrindiniai objektinio programavimo principai:

- inkapsuliacija;
- paveldėjimas;
- abstrakcija;
- polimorfizmas.

---

### 3.1 Enkapsuliacija

Enkapsuliacija reiškia, kad duomenys ir jų valdymas yra laikomi vienoje klasėje, o prieiga prie jų ribojama per metodus.

Šiame projekte inkapsuliacija naudojama keliose vietose. Pavyzdžiui, `Order` klasėje negalima keisti užsakymo, jei jis jau yra uždarytas:

```python
def add_item(self, menu_item, quantity):
    if self.status == "Closed":
        raise ValueError("Cannot modify closed order.")
    self.items.append(OrderItem(menu_item, quantity))
```

Šis metodas ne tik prideda elementą į užsakymą, bet ir patikrina, ar užsakymas dar yra atidarytas. Tai apsaugo sistemą nuo neteisingų veiksmų.

Kitas svarbus pavyzdys yra duomenų validacija konstruktoriuose:

```python
if price < 0:
    raise ValueError("Price cannot be negative.")
```

Tokiu būdu užtikrinama, kad objektai visada turės teisingus duomenis.

---

### 3.2 Paveldėjimas

Paveldėjimas leidžia kurti bendrą bazinę klasę ir iš jos išvesti konkretesnes klases.

Šiame projekte paveldėjimas naudojamas meniu elementams:

```python
class FoodItem(MenuItem):
    def final_price(self):
        return self.price

class DrinkItem(MenuItem):
    def final_price(self):
        if self.size_ml > 500:
            return self.price + 0.50
        return self.price
```

Abi klasės paveldi bendrus atributus iš `MenuItem`, tokius kaip pavadinimas, ID ir kaina. Tai leidžia išvengti kodo dubliavimo.

Paveldėjimas taip pat leidžia lengvai išplėsti sistemą. Pavyzdžiui, galima pridėti naują klasę `DessertItem`, kuri paveldėtų iš `MenuItem`.

---

### 3.3 Abstrakcija

Abstrakcija reiškia, kad apibrėžiama bendra struktūra, tačiau paslepiamos detalės.

Šiame projekte abstrakcija realizuota naudojant abstrakčią klasę `MenuItem`:

```python
class MenuItem(ABC):
    @abstractmethod
    def final_price(self):
        raise NotImplementedError
```

Tai reiškia, kad kiekvienas meniu elementas privalo turėti `final_price()` metodą. Tai užtikrina vienodą sąsają visoje sistemoje.

---

### 3.4 Polimorfizmas

Polimorfizmas leidžia skirtingiems objektams turėti tą patį metodą, tačiau skirtingą elgesį.

Šiame projekte visi meniu elementai turi metodą `final_price()`, tačiau jo veikimas priklauso nuo objekto tipo:

```python
item.final_price()
```

Maisto objektas grąžins paprastą kainą, o gėrimas gali pridėti papildomą mokestį priklausomai nuo dydžio.

Tai leidžia vienodai apdoroti skirtingus objektus.

---

## 4. Dizaino šablonas

Šiame projekte naudojamas **Builder dizaino šablonas**, kuris realizuotas `OrderBuilder` klasėje.

```python
builder = OrderBuilder()
order = (
    builder.set_order_id(1)
           .set_customer("Jonas")
           .set_table(2)
           .add_item(pizza, 2)
           .build()
)
```

Šis šablonas leidžia kurti sudėtingus objektus etapais. Tai yra naudinga, nes užsakymas turi daug parametrų.

Builder šablono privalumai:
- aiškesnis kodas;
- mažesnė klaidų tikimybė;
- lengvesnis objektų kūrimas.

---

## 5. Kompozicija ir agregacija

Kompozicija reiškia, kad vienas objektas yra sudarytas iš kitų objektų.

Šiame projekte `Order` klasė turi `OrderItem` objektus:

```python
self.items.append(OrderItem(menu_item, quantity))
```

Agregacija reiškia, kad objektai gali egzistuoti nepriklausomai.

`Restaurant` klasė saugo kitus objektus:

```python
self.menu.append(item)
self.orders.append(order)
self.tables.append(table)
```

---

## 6. Darbas su failais

Programa naudoja JSON failus duomenų saugojimui.

Duomenų išsaugojimas:

```python
with open(filename, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4)
```

Duomenų įkėlimas:

```python
with open(filename, "r", encoding="utf-8") as file:
    data = json.load(file)
```

JSON formatas pasirinktas dėl paprastumo ir aiškumo.

---

## 7. Testavimas

Testavimas atliekamas naudojant `unittest` modulį.

Testai tikrina:
- kainų skaičiavimą;
- užsakymo kūrimą;
- užsakymo būsenos keitimą;
- pajamų skaičiavimą;
- stalų rezervavimą.

Pavyzdys:

```python
item = FoodItem(1, "Pizza", 8.5, False)
self.assertEqual(item.final_price(), 8.5)
```

Testavimas yra svarbus, nes leidžia užtikrinti, kad sistema veikia teisingai.

---

## 8. Klaidų valdymas ir validacija

Programa turi daug validacijos mechanizmų:

```python
if item_id <= 0:
    raise ValueError("Item ID must be positive.")
```

```python
if quantity <= 0:
    raise ValueError("Quantity must be greater than zero.")
```

```python
if table is None:
    raise ValueError("Table not found.")
```

Validacija yra svarbi, nes apsaugo sistemą nuo neteisingų duomenų ir loginių klaidų.

---

## 9. Pajamų skaičiavimas

Pajamos skaičiuojamos tik iš uždarytų užsakymų:

```python
return sum(order.calculate_total() for order in self.orders if order.status == "Closed")
```

---

## 10. Rezultatai

Šio darbo metu buvo sukurta pilnai veikianti restorano valdymo sistema, kuri leidžia atlikti pagrindinius restorano administravimo veiksmus. Programa sėkmingai įgyvendina visus numatytus funkcinius reikalavimus ir demonstruoja objektinio programavimo principų taikymą praktikoje.

Pasiekti rezultatai:

- sukurta sistema, leidžianti valdyti meniu, stalus ir užsakymus;
- realizuotas užsakymų kūrimas naudojant Builder šabloną;
- įgyvendintas korektiškas pajamų skaičiavimas, kuris apima tik užbaigtus užsakymus;
- realizuotas duomenų išsaugojimas ir įkėlimas iš JSON failo;
- įgyvendintas klaidų valdymas ir duomenų validacija, užtikrinanti sistemos stabilumą;
- parašyti vienetiniai testai, kurie patikrina pagrindinę programos logiką.

Svarbu pabrėžti, kad sistema veikia nuosekliai ir logiškai – vartotojas negali atlikti neteisingų veiksmų, pavyzdžiui:
- uždaryti tuščio užsakymo;
- pridėti elementų į jau uždarytą užsakymą;
- rezervuoti neegzistuojantį stalą.

Didžiausias iššūkis buvo sukurti aiškią klasių tarpusavio sąveiką. Reikėjo užtikrinti, kad kiekviena klasė turėtų aiškią atsakomybę, o sistema nebūtų per daug sudėtinga.

---

## 11. Išvados

Šio kursinio darbo metu buvo sukurta paprasta, bet funkcionali sistema, kuri aiškiai parodo objektinio programavimo principų taikymą praktikoje.

Darbo metu paaiškėjo, kad tinkamas klasių suskirstymas yra labai svarbus. Kai kiekviena klasė turi aiškią atsakomybę, programa tampa lengviau suprantama, lengviau testuojama ir lengviau plečiama.

Inkapsuliacija leido apsaugoti duomenis ir užtikrinti, kad objektai visada būtų teisingos būsenos. Paveldėjimas sumažino kodo dubliavimą ir leido patogiai kurti naujus meniu elementų tipus. Abstrakcija užtikrino, kad visi objektai turėtų bendrą sąsają, o polimorfizmas leido vienodai apdoroti skirtingus objektus.

Builder dizaino šablonas pasirodė labai naudingas kuriant užsakymus, nes leido išvengti sudėtingų konstruktorių ir padarė kodą aiškesnį.

Taip pat svarbi dalis buvo testavimas ir validacija. Jie užtikrino, kad programa veiktų stabiliai ir kad vartotojas negalėtų įvesti neteisingų duomenų ar atlikti logiškai neteisingų veiksmų.

Apibendrinant galima teigti, kad sukurtas sprendimas yra:
- funkcionalus;
- logiškai suprojektuotas;
- lengvai plečiamas ateityje.

---

## 12. Ateities plėtra


Tolimesnis sistemos vystymas galėtų apimti šiuos patobulinimus:

- Meniu sistemos išplėtimas, leidžiant ne tik pridėti ar pašalinti elementus, bet ir redaguoti jų duomenis, pavyzdžiui, keisti kainą, pavadinimą ar papildomą informaciją apie patiekalą.

- Paieškos funkcionalumo įdiegimas, kuris leistų greitai rasti meniu elementus pagal pavadinimą ar kitus kriterijus, taip pagerinant sistemos naudojimo patogumą.

- Užsakymų valdymo patobulinimas, suteikiant galimybę redaguoti užsakymą tol, kol jis dar nėra uždarytas, pavyzdžiui, keisti kiekius ar pridėti naujus elementus.

- Papildomos informacijos apie užsakymus saugojimas, tokios kaip užsakymo sukūrimo laikas, klientas ar užsakymo istorija, kas leistų geriau analizuoti duomenis.

- Grafinės vartotojo sąsajos (GUI) sukūrimas, naudojant tokias bibliotekas kaip Tkinter, siekiant padaryti sistemą patogesnę naudoti ir vizualiai aiškesnę.

- Duomenų saugojimo sistemos tobulinimas, pakeičiant JSON failus į duomenų bazę (pvz., SQLite), kas leistų efektyviau valdyti didesnius duomenų kiekius.

- Testavimo išplėtimas, įtraukiant daugiau testų kraštiniams atvejams, siekiant dar labiau padidinti sistemos patikimumą.

- Sistemos funkcionalumo išplėtimas, pridedant galimybę generuoti ataskaitas, pavyzdžiui, apie populiariausius patiekalus ar bendras pajamas per tam tikrą laikotarpį.

- Sistemos pritaikymas internetinei aplinkai, sukuriant web aplikaciją, kuri leistų naudotis sistema per naršyklę.
