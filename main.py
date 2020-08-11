# mchtr-shop 0.45
# LICENSE: MIT

from fpdf import FPDF
from sys import platform
import sys

if platform == "linux" or platform == "linux2":
    system = 'linux'
elif platform == "win32":
    system = 'windows'

euro = 4.2693
forbidden_cpv_codes = ('302', '380', '385', '386', '438')
tender_threshold_euro = 30000 * euro

pdf = FPDF()
pdf.add_page()
if system == 'linux':
    pdf.add_font('DejaVu', '', '/usr/share/fonts/TTF/DejaVuSans.ttf', uni=True)
    pdf.set_font("DejaVu", size=10)
else:
    pdf.add_font('Tahoma', '', 'C:/WINDOWS/Fonts/Tahoma.ttf', uni=True)
    pdf.set_font('Tahoma', size=10)

i = True
while i:
    try:
        cpv = input("Podaj trzy pierwsze cyfry kodu CPV zamawianego towaru/usługi: ")
        cpv = int(cpv)
        i = False
    except ValueError:
        print("Błędny kod CPV. Spróbuj ponownie")

if str(cpv)[0:3] in forbidden_cpv_codes:
    tender_cpv = True
else:
    tender_cpv = False

i = True
while i:
    research = input("Czy zakup realizowany będzie ze środków projektu badawczego? (tak/nie) ").lower()
    if research not in ('tak', 'nie'):
        print("Błędna odpowiedź. Tylko 'tak' i 'nie' są akceptowane. ")
    else:
        i = False

i = True
while i:
    eu_funds = input("Czy zakup realizowany będzie ze środków pochodzących z Unii Europejskiej? (tak/nie) ").lower()
    if eu_funds not in ('tak', 'nie'):
        print("Błędna odpowiedź. Tylko 'tak' i 'nie' są akceptowane. ")
    else:
        i = False

i = True
while i:
    try:
        price = input("Podaj szacowaną kwotę netto zakupu (PLN): ")
        price = float(price)
        i = False
    except ValueError:
        print("Błędna kwota. Spróbuj ponownie")

num = 1


# Sekcja 1 - wypisanie wniosku (naukowy, nienaukowy, split-payment)
pdf.multi_cell(180, 7, txt="PRZYGOTOWANIE WNIOSKU", align="C")
if research == 'tak':
    pdf.multi_cell(180, 7, txt=str(num) + ". Wypełnij wniosek zgodnie z plikiem wniosek-badawczy.odt. Pamiętaj o "
                                          "uzupełnieniu informacji o projekcie badawczym, z którego środków realizowany"
                                          " jest zakup oraz o ew. zmianie/usunięciu loga w dolnej części wniosku.")
    num += 1
else:
    pdf.multi_cell(180, 7, txt=str(num) + ". Wypełnij wniosek zgodnie z plikiem wniosek-standard.odt")
    num += 1

if eu_funds == 'tak':
    pdf.multi_cell(180, 7, txt=str(num) + ". Zaznacz, że informacja o postępowaniu powinna być zamieszczona w Bazie Konkurencyjności. ")
    num += 1
else:
    pdf.multi_cell(180, 7, txt=str(num) + ". Zaznacz, że informacja o postępowaniu nie powinna być zamieszczona w Bazie Konkurencyjności. ")
    num += 1

pdf.multi_cell(180, 7, txt=str(num) + ". Podpisz wniosek jako 'osoba wnioskująca'. Zdobądź podpis dysponenta środków "
                                      "jako 'kierownika projektu'. ")
num += 1

pdf.multi_cell(180, 7, txt=str(num) + ". Złóż wniosek do działu administracyjnego (p. 627). ")
num += 1

if (not tender_cpv and price < 1000) or (tender_cpv and research == 'tak' and price < 1000):
    rule = 'nie podlega ustawie Prawo zamówień publicznych.'
    rule_num = 0
elif research == 'tak' and price < tender_threshold_euro:
    rule = 'podlega Zarządzeniu Dziekana nr 05/2020.'
    rule_num = 1
elif (not tender_cpv) and (price < tender_threshold_euro):
    rule = 'podlega Zarządzeniu Dziekana nr 04/2020.'
    rule_num = 1
else:
    rule = 'podlega pod przetarg nieograniczony.'
    rule_num = 2
pdf.multi_cell(180, 7, txt=str(num) + ". Po 1-2 dniach wniosek jest uzupełniony. Sprawdź wg jakich zapisów "
                                       "należy realizować zakup. Zgodnie z Twoimi odpowiedziami, "
                                       "twój zakup  " + rule)
num += 1

if rule_num == 2:
    pdf.multi_cell(180, 7, txt=str(num) + ". Przygotuj opis przedmiotu zamówienia w którym opiszesz pożądaną specyfikację zamawianego towaru."
                                          " Przykładowy opis znajdziesz w pliku opis-przedmiotu-zamowienia.odt.")
    num += 1
    pdf.multi_cell(180, 7, txt=str(num) + ". Opis przedmiotu zamówienia razem z podpisanym wnioskiem zanieś do p. Marii Lepy (1. piętro), która"
                                          " przejmie realizację przetargu.")
    pdf.output("plan-realizacji-zakupu.pdf")
    sys.exit()


# Sekcja 2 - zebranie ofert
if rule_num == 1:
    pdf.multi_cell(180, 7, txt="ZEBRANIE OFERT", align="C")
    if price <= 10000:
        pdf.multi_cell(180, 7, txt=str(num) + ". Zbierz 3 konkurencyjne oferty przedmiotu zakupu. W przypadku usług"
                                              " specjalistycznych, gdy ciężko o znalezienie 3 ofert można zebrać tylko 1"
                                              " ofertę pod warunkiem, że wrzucisz zaproszenie do składania ofert na stronę"
                                              " www wydziału na 7 dni. Ofertą może być zrzut ekranu ze strony www"
                                              " wykonawcy, notatka z przeprowadzonej rozmowy telefonicznej z wykonawcą"
                                              " lub pisemna oferta złożona przez wykonawcę.")
        num += 1
    elif price <= tender_threshold_euro:
        pdf.multi_cell(180, 7, txt=str(num) + ". Wypełnij zaproszenie do składania ofert (zaproszenie-umowa.odt) oraz opis"
                                              " przedmiotu zamówienia (opis-przedmiotu-zamowienia.odt). Załącz"
                                              " wzór propozycji cenowej (wzor-propozycji-cenowej.odt) i taki"
                                              " komplet dokumentów przekaż Dyrektorowi (pozostaw w p. 627).")
        num += 1
        pdf.multi_cell(180, 7, txt=str(num) + ". Dyrektor podpisze zaproszenie. Odbierz dokumenty.")
        num += 1
        pdf.multi_cell(180, 7, txt=str(num) + ". Zeskanuj podpisane zaproszenie. Skan zaproszenia, skan opisu"
                                              " przedmiotu zamówienia, elektroniczną, edytowalną wersję wzoru"
                                              " propozycji cenowej oraz wzór umowy wyślij mailem do co najmniej 3 firm. W przypadku"
                                              " usług/towarów specjalistycznych, dla których ciężko o 3 firmy mogące"
                                              " zrealizować dostawę/usługę istnieje możliwość wysłania zaproszenia"
                                              " tylko do 1 firmy pod warunkiem, że wrzucisz zaproszenie do składania"
                                              " ofert na stronę www wydziału na 7 dni.")
        num += 1
        pdf.multi_cell(180, 7, txt=str(num) + ". Zbierz oferty przesłane przez firmy.")
        num += 1
    elif research == 'tak' and price > tender_threshold_euro:
        pdf.multi_cell(180, 7, txt=str(num) + ". Wypełnij zaproszenie do składania ofert (zaproszenie-umowa.odt) oraz opis"
                                              " przedmiotu zamówienia (opis-przedmiotu-zamowienia.odt). Załącz"
                                              " wzór propozycji cenowej (wzor-propozycji-cenowej.odt) i taki"
                                              " komplet dokumentów przekaż Pełnomocnikowi Dziekana ds. zamówień"
                                              " publicznych oraz Dziekanowi (pozostaw w p. 627).")
        num += 1
        pdf.multi_cell(180, 7, txt=str(num) + ". Dziekan podpisze zaproszenie. Odbierz dokumenty.")
        num += 1
        pdf.multi_cell(180, 7, txt=str(num) + ". Ogłoszenie o udzielanym zamówieniu zamieść w Biuletynie Informacji"
                                              " Publicznej PW w zakładce 'bez stosowania ustawy'. Ogłoszenie powinno"
                                              " zawierać: nazwę i adres zamawiającego, adres do korespondencji,"
                                              " osobę do kontaktu, opis przedmiotu zamówienia, termin wykonania"
                                              " zamówienia, opis sposobu złożenia ofert, opis sposobu obliczania ceny,"
                                              " miejsce i termin składania ofert, kryteria oceny ofert i ich znaczenie,"
                                              " warunki jakie muszą spełniać podmioty zainteresowane wykonaniem"
                                              " zamówienia.")
        num += 1
        pdf.multi_cell(180, 7, txt=str(num) + ". Zeskanuj podpisane zaproszenie. Skan zaproszenia, skan opisu"
                                              " przedmiotu zamówienia, elektroniczną, edytowalną wersję wzoru"
                                              " propozycji cenowej oraz wzór umowy wyślij mailem do co najmniej 3 firm.")
        num += 1
        pdf.multi_cell(180, 7, txt=str(num) + ". Zbierz oferty przesłane przez firmy.")
        num += 1


# Sekcja 3 - raport wykonanych czynności
if rule_num == 1:
    if price <= 10000:
        pdf.multi_cell(180, 7, txt="NOTATKA SŁUŻBOWA", align="C")
        pdf.multi_cell(180, 7, txt=str(num) + ". Na podstawie wykonanego przeglądu ofert uzupełnij notatkę służbową"
                                              " (notatka-sluzbowa.odt). Wydrukuj i podpisz.")
        num += 1
    elif price <= tender_threshold_euro:
        pdf.multi_cell(180, 7, txt="RAPORT WYKONANYCH CZYNNOŚCI", align="C")
        pdf.multi_cell(180, 7, txt=str(num) + ". Na podstawie wykonanego przeglądu ofert uzupełnij raport wykonanych"
                                              " czynności (protokol-wykonanych-czynnosci.odt). Nie zmieniaj kursu euro"
                                              " w raporcie. Wydrukuj i podpisz. W punkcie 7 raportu należy zebrać"
                                              " podpisy 3 pracowników Instytutu. ")
        num += 1
    elif research == 'tak' and price > tender_threshold_euro:
        pdf.multi_cell(180, 7, txt=str(num) + ". Na podstawie wykonanego przeglądu ofert uzupełnij raport wykonanych"
                                          " czynności (protokol-wykonanych-czynnosci.odt). Nie zmieniaj kursu euro"
                                          " w raporcie. Wydrukuj i podpisz. W punkcie 7 raportu należy zebrać"
                                          " podpisy 3 pracowników Instytutu. ")
        num += 1
        pdf.multi_cell(180, 7, txt=str(num) + ". Przekaż raport do zatwierdzenia przez Dziekana. ")
        num += 1


# Sekcja 4 - podpisanie zamówienia, umowy
if rule_num == 1:
    if price <= 10000:
        pdf.multi_cell(180, 7, txt="PODPISANIE ZAMÓWIENIA", align="C")
        pdf.multi_cell(180, 7, txt=str(num) + ". Wypełnij zamówienie (zamowienie.odt).")
        num += 1
        pdf.multi_cell(180, 7, txt=str(num) + ". Złóż dwie kopie zamówienia, jedną kopię notatki służbowej i wydrukowane oferty do Dyrektora.")
        num += 1
        pdf.multi_cell(180, 7, txt=str(num) + ". Odbierz podpisane kopie zamówienia.")
        num += 1
        if research == 'tak':
            pdf.multi_cell(180, 7, txt=str(num) + ". Oryginał lub skan zamówienia wyślij firmie"
                                                  " realizującej dostawę/usługę razem z dokumentem RODO (RODO-badawczy.odt). Firma powinna podpisać dokumenty i"
                                                  " odesłać jedną kopię zamówienia i dokument RODO przed realizacją dostawy/usługi.")
            num += 1
        else:
            pdf.multi_cell(180, 7, txt=str(num) + ". Oryginał lub skan zamówienia wyślij firmie"
                                                  " realizującej dostawę/usługę razem z dokumentem RODO (RODO.odt). Firma powinna podpisać dokumenty i"
                                                  " odesłać jedną kopię zamówienia i dokument RODO przed realizacją dostawy/usługi.")
            num += 1
    else:
        pdf.multi_cell(180, 7, txt="PODPISANIE UMOWY", align="C")
        if research == 'tak':
            pdf.multi_cell(180, 7, txt=str(num) + ". Wypełnij umowę (umowa-badawczy.odt).")
            num += 1
            if price <= tender_threshold_euro:
                pdf.multi_cell(180, 7, txt=str(num) + ". Złóż dwie kopie umowy, jedną kopię raportu wykonanych czynności i wydrukowane oferty do Dyrektora.")
                num += 1
            else:
                pdf.multi_cell(180, 7, txt=str(num) + ". Złóż dwie kopie umowy, jedną kopię raportu wykonanych czynności i wydrukowane oferty do Dziekana.")
                num += 1
            pdf.multi_cell(180, 7, txt=str(num) + ". Odbierz podpisane kopie umowy.")
            num += 1
            pdf.multi_cell(180, 7, txt=str(num) + ". Wyślij obie papierowe kopie firmie realizującej dostawę/usługę"
                                                  " razem z dokumentem RODO (RODO-badawczy.odt), kopią oferty złożonej"
                                                  " przez wykonawcę, wzorem protokołu odbioru (protokol-odbioru.odt) i opisem przedmiotu"
                                                  " zamówienia. Firma powinna podpisać dokumenty i odesłać jedną kopię"
                                                  " umowy i dokument RODO przed realizacją dostawy/usługi.")
        else:
            pdf.multi_cell(180, 7, txt=str(num) + ". Wypełnij umowę (umowa.odt).")
            num += 1
            pdf.multi_cell(180, 7, txt=str(num) + ". Złóż dwie kopie umowy, jedną kopię raportu wykonanych czynności i wydrukowane oferty do Dyrektora.")
            num += 1
            pdf.multi_cell(180, 7, txt=str(num) + ". Odbierz podpisane kopie umowy.")
            num += 1
            pdf.multi_cell(180, 7, txt=str(num) + ". Wyślij obie papierowe kopie firmie realizującej dostawę/usługę"
                                                  " razem z dokumentem RODO (RODO.odt), kopią oferty złożonej"
                                                  " przez wykonawcę, wzorem protokołu odbioru (protokol-odbioru.odt) i opisem przedmiotu"
                                                  " zamówienia. Firma powinna podpisać dokumenty i odesłać jedną kopię"
                                                  " umowy i dokument RODO przed realizacją dostawy/usługi.")
        num += 1

# Sekcja 5 - zakup - faktura przelew lub zwykła
pdf.multi_cell(180, 7, txt="ZAKUP", align="C")
if rule_num == 0:
    pdf.multi_cell(180, 7, txt=str(num) + ". Znajdź interesujący Cię przedmiot i dokonaj zakupu. Możesz zapłacić"
               " własnymi pieniędzmi (po realizacji zakupu dostaniesz zwrot) lub poprosić firmę o fakturę przelewową"
               " płatną w terminie 14 dni od dnia dostarczenia towaru (faktura zostanie opłacona przez księgowość).")
    num += 1
elif rule_num == 1 and price <= 10000:
    pdf.multi_cell(180, 7, txt=str(num) + ". Po podpisaniu zamówienia przez firmę, firma może zrealizować dostawę/usługę. Możesz zapłacić"
               " własnymi pieniędzmi (po realizacji zakupu dostaniesz zwrot) lub poprosić firmę o fakturę przelewową"
               " płatną w terminie 14 dni od dnia dostarczenia towaru (faktura zostanie opłacona przez księgowość).")
    num += 1
elif rule_num == 1 and price > 10000:
    pdf.multi_cell(180, 7, txt=str(
        num) + ". Po podpisaniu umowy przez firmę, firma może zrealizować dostawę/usługę. Firma powinna wystawić fakturę przelewową"
               " płatną w terminie 14 dni od dnia dostarczenia towaru (faktura zostanie opłacona przez księgowość)."
               " Upewnij się, że faktura wystawiona będzie na poprawne dane.")
    num += 1

pdf.multi_cell(180, 7, txt="", align="C")
pdf.multi_cell(180, 7, txt="Dane do faktury:", align="C")
pdf.multi_cell(180, 7, txt="Politechnika Warszawska", align="C")
pdf.multi_cell(180, 7, txt="Plac Politechniki 1", align="C")
pdf.multi_cell(180, 7, txt="00-661 Warszawa", align="C")
pdf.multi_cell(180, 7, txt="NIP: 525-000-58-34", align="C")
pdf.multi_cell(180, 7, txt="", align="C")

# Sekcja 6 - opisanie faktury
pdf.multi_cell(180, 7, txt="OPISANIE FAKTURY", align="C")
pdf.multi_cell(180, 7, txt=str(
        num) + ". Po otrzymaniu towaru i faktury, opisz fakturę na odwrocie w prawym górnym rogu. Jeśli fakturę"
               " masz w formie papierowej, napisz: otrzymałem/am dnia ........ Jeśli fakturę masz w formie"
               " elektronicznej, wydrukuj ją + wydrukuj maila do którego faktura była załączona. Następnie krótko"
               " opisz co było przedmiotem wniosku. ")
num += 1
if research == 'tak':
    pdf.multi_cell(180, 7, txt="Ponieważ realizujesz zakup ze środków grantu badawczego, opis powinien jasno "
                               "wskazywać, że przedmiot zakupu będzie służył do realizacji badań.")
pdf.multi_cell(180, 7, txt=str(num) + ". Podpisz opis faktury.")
num += 1
if rule_num == 1 and price > 10000:
    pdf.multi_cell(180, 7, txt=str(num) + ". Odbierając towar wypełnij i podpisz protokół odbioru w dwóch kopiach - jedna dla wykonawcy, druga dla ciebie. Obie kopie powinny być podpisane przez przedstawiciela wykonawcy.")
    num += 1
# Sekcja 7 - złożenie faktury do działu administracyjnego
pdf.multi_cell(180, 7, txt=str(num) + ". Przekaż wszystkie dokumenty do działu księgowego (p. 627).")
num += 1

if research == 'tak' and price > tender_threshold_euro:
    pdf.multi_cell(180, 7, txt=str(num) + ". Umieść na stronie Biuletynu Informacji Publicznej PW ogłoszenie o"
                                          " udzieleniu zamówienia podając nazwę firmy, z którą zawarto umowę lub"
                                          " informację o nieudzieleniu zamówienia.")
    num += 1

print('Plan realizacji zakupu wygenerowany do pliku PDF.')

pdf.output("plan-realizacji-zakupu.pdf")
