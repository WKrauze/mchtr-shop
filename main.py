# mchtr-shop 0.3

from fpdf import FPDF
from sys import platform
import sys

if platform == "linux" or platform == "linux2":
    system = 'linux'
elif platform == "win32":
    system = 'windows'

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

forbidden_cpv_codes = ('302', '323', '386', '426', '429', '484')

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
    split_payment = input("Czy zamawiany produkt/usługa znajduje się na liście split-payment.pdf? (tak/nie) ").lower()
    if split_payment not in ('tak', 'nie'):
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
                                          " jest zakup.")
    num += 1
else:
    pdf.multi_cell(180, 7, txt=str(num) + ". Wypełnij wniosek zgodnie z plikiem wniosek-standard.odt")
    num += 1
pdf.multi_cell(180, 7, txt=str(num) + ". Podpisz wniosek jako 'osoba wnioskująca'. Zdobądź podpis dysponenta środków "
                                      "jako 'kierownika projektu'. ")
num += 1

if split_payment == 'tak':
    pdf.multi_cell(180, 7, txt=str(num) + ". W polu przedmiot wniosku dopisz: 'poz. ... zał. 15 ustawy o VAT' - numer pozycji weź z pliku split-payment.pdf. ")
    num += 1
else:
    pdf.multi_cell(180, 7, txt=str(num) + ". W polu przedmiot wniosku dopisz: 'przedmiot wniosku niewykazany "
                                               "w zał. 15 ustawy o VAT'.")
    num += 1

pdf.multi_cell(180, 7, txt=str(num) + ". Złóż wniosek do działu administracyjnego (p. 627). ")
num += 1

# TODO: sprawdzić jaki jest warunek kwotowy dla przetargu
if (not tender_cpv and price < 1000) or (tender_cpv and research == 'tak' and price < 1000):
    rule = 'nie podlega ustawie Prawo zamówień publicznych.'
    rule_num = 0
elif tender_cpv and research == 'tak':
    rule = 'podlega Zarządzeniu Dziekana nr 03/2016.'
    rule_num = 1
elif (not tender_cpv) and (price < 100000):
    rule = 'podlega Zarządzeniu Dziekana nr 8/2014.'
    rule_num = 1
elif tender_cpv:
    rule = 'podlega pod przetarg nieograniczony.'
    rule_num = 2
pdf.multi_cell(180, 7, txt=str(num) + ". Po 1-2 dniach wniosek jest uzupełniony. Sprawdź wg jakich zapisów "
                                       "powinnaś/powinieneś realizować zakup. Zgodnie z Twoimi odpowiedziami, "
                                       "twój zakup  " + rule)
num += 1

if rule_num == 2:
    pdf.output("plan-realizacji-zakupu.pdf")
    sys.exit('Zakup przetargowy nie jest jeszcze opracowany. Generowanie cząstkowego raportu.')


# Sekcja 2 - przegląd 3 ofert/zaproszenie do składania ofert/zakup z wolnej ręki
if rule_num != 0:
    pdf.multi_cell(180, 7, txt="ZEBRANIE OFERT", align="C")
    if price <= 10000:
        pdf.multi_cell(180, 7, txt=str(num) + ". Zbierz 3 konkurencyjne oferty przedmiotu zakupu. W przypadku usług"
                                              " specjalistycznych, gdy ciężko o znalezienie 3 ofert można zebrać tylko 1"
                                              " ofertę pod warunkiem, że wrzucisz zaproszenie do składania ofert na stronę"
                                              " www wydziału na 7 dni. Ofertą może być zrzut ekranu ze strony www"
                                              " wykonawcy, notatka z przeprowadzonej rozmowy telefonicznej z wykonawcą"
                                              " lub pisemna oferta złożona przez wykonawcę.")
        num += 1
    elif price<= 50000:
        pdf.multi_cell(180, 7, txt=str(num) + ". Wypełnij zaproszenie do składania ofert (zaproszenie.odt) oraz opis"
                                              " przedmiotu zamówienia (opis-przedmiotu-zamowienia.odt). Załącz"
                                              " wzór propozycji cenowej (wzor-propozycji-cenowej.odt) i taki"
                                              " komplet dokumentów przekaż Dyrektorowi (pozostaw w p. 627).")
        num += 1
        pdf.multi_cell(180, 7, txt=str(num) + ". Dyrektor podpisze zaproszenie. Odbierz dokumenty.")
        num += 1
        pdf.multi_cell(180, 7, txt=str(num) + ". Zeskanuj podpisane zaproszenie. Skan zaproszenia, skan opisu"
                                              " przedmiotu zamówienia oraz elektroniczną, edytowalną wersję wzoru"
                                              " propozycji cenowej wyślij mailem do co najmniej 3 firm. W przypadku"
                                              " usług/towarów specjalistycznych, dla których ciężko o 3 firmy mogące"
                                              " zrealizować dostawę/usługę istnieje możliwość wysłania zaproszenia"
                                              " tylko do 1 firmy pod warunkiem, że wrzucisz zaproszenie do składania"
                                              " ofert na stronę www wydziału na 7 dni.")
        num += 1
        pdf.multi_cell(180, 7, txt=str(num) + ". Zbierz oferty przesłane przez firmy.")
        num += 1


# Sekcja 3 - raport wykonanych czynności
if rule_num != 0 :
    if price <= 10000:
        pdf.multi_cell(180, 7, txt="NOTATKA SŁUŻBOWA", align="C")
        pdf.multi_cell(180, 7, txt=str(num) + ". Na podstawie wykonanego przeglądu ofert uzupełnij notatkę służbową"
                                              " (notatka-sluzbowa.odt). Wydrukuj i podpisz.")
        num += 1
    else:
        pdf.multi_cell(180, 7, txt="RAPORT WYKONANYCH CZYNNOŚCI", align="C")
        pdf.multi_cell(180, 7, txt=str(num) + ". Na podstawie wykonanego przeglądu ofert uzupełnij raport wykonanych"
                                              " czynności (protokol-wykonanych-czynnosci.odt). Nie zmieniaj kursu euro"
                                              " w raporcie. Wydrukuj i podpisz. W punkcie 9 raportu należy zebrać"
                                              " podpisy 3 pracowników ZiF. ")
        num += 1

# Sekcja 4 - podpisanie zamówienia, umowy
if rule_num != 0:
    if price <= 10000:
        pdf.multi_cell(180, 7, txt="PODPISANIE ZAMÓWIENIA", align="C")
        pdf.multi_cell(180, 7, txt=str(num) + ". Wypełnij zamówienie (zamowienie.odt). Złóż dwie kopie zamówienia,"
                                              " jedną kopię notatki służbowej i wydrukowane oferty do Dyrektora. Odbierz"
                                              " podpisane kopie zamówienia. Wyślij oryginał lub skan firmie"
                                              " realizującej dostawę/usługę. Firma powinna podpisać dokumenty i"
                                              " odesłać jedną kopię przed realizacją dostawy/usługi.")
        num += 1
    else:
        pdf.multi_cell(180, 7, txt="PODPISANIE UMOWY", align="C")
        if research == 'tak':
            pdf.multi_cell(180, 7, txt=str(num) + ". Wypełnij umowę (umowa.odt). Złóż dwie kopie umowy, jedną kopię"
                                                  " raportu wykonanych czynności i wydrukowane oferty do Dyrektora. Odbierz podpisane kopie umowy."
                                                  " Wyślij obie papierowe kopie firmie realizującej dostawę/usługę. Firma powinna"
                                                  " podpisać dokumenty i odesłać jedną kopię przed realizacją"
                                                  " dostawy/usługi.")
        else:
            pdf.multi_cell(180, 7, txt=str(num) + ". Wypełnij umowę (umowa-badawczy.odt). Złóż dwie kopie umowy, jedną kopię"
                                                  " raportu wykonanych czynności i wydrukowane oferty do Dyrektora. Odbierz podpisane kopie umowy."
                                                  " Wyślij obie papierowe kopie firmie realizującej dostawę/usługę. Firma powinna"
                                                  " podpisać dokumenty i odesłać jedną kopię przed realizacją"
                                                  " dostawy/usługi.")
        num += 1

# TODO: RODO jako dodatek do umowy? (zamówienia też?)

# Sekcja 5 - zakup - faktura przelew lub zwykła
pdf.multi_cell(180, 7, txt="ZAKUP", align="C")
if rule_num == 0:
    pdf.multi_cell(180, 7, txt=str(
        num) + ". Znajdź interesujący Cię przedmiot i dokonaj zakupu. Możesz zapłacić"
               " własnymi pieniędzmi (po realizacji zakupu dostaniesz zwrot) lub poprosić firmę o fakturę przelewową"
               " płatną w terminie 14 dni od dnia dostarczenia towaru (faktura zostanie opłacona przez księgowość)."
               " W obu przypadkach weź fakturę na Instytut!")
    num += 1
elif price <= 10000:
    pdf.multi_cell(180, 7, txt=str(
        num) + ". Po podpisaniu zamówienia przez firmę, firma może zrealizować dostawę/usługę. Możesz zapłacić"
               " własnymi pieniędzmi (po realizacji zakupu dostaniesz zwrot) lub poprosić firmę o fakturę przelewową"
               " płatną w terminie 14 dni od dnia dostarczenia towaru (faktura zostanie opłacona przez księgowość)."
               " W obu przypadkach upewnij się, że faktura wystawiona będzie na Instytut!")
    num += 1
else:
    pdf.multi_cell(180, 7, txt=str(
        num) + ". Po podpisaniu umowy przez firmę, firma może zrealizować dostawę/usługę. Firma powinna wystawić fakturę przelewową"
               " płatną w terminie 14 dni od dnia dostarczenia towaru (faktura zostanie opłacona przez księgowość)."
               " Upewnij się, że faktura wystawiona będzie na poprawne dane.")
    num += 1

pdf.multi_cell(180, 7, txt="", align="C")
pdf.multi_cell(180, 7, txt="Dane do faktury:", align="C")
pdf.multi_cell(180, 7, txt="Politechnika Warszawska", align="C")
pdf.multi_cell(180, 7, txt="Instytut Mikromechaniki i Fotoniki", align="C")
pdf.multi_cell(180, 7, txt="ul. Św. A. Boboli 8", align="C")
pdf.multi_cell(180, 7, txt="02-525 Warszawa", align="C")
pdf.multi_cell(180, 7, txt="NIP: 525-000-58-34", align="C")
pdf.multi_cell(180, 7, txt="", align="C")

pdf.multi_cell(180, 7, txt="Dopuszczalne też jest wystawienie faktury na: ")

pdf.multi_cell(180, 7, txt="", align="C")
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
pdf.multi_cell(180, 7, txt=str(
        num) + ". Podpisz opis faktury.")
num += 1

# Sekcja 7 - złożenie faktury do działu administracyjnego
pdf.multi_cell(180, 7, txt=str(
        num) + ". Przekaż wszystkie dokumenty do działu księgowego (p. 627).")
num += 1



print('Plan realizacji zakupu wygenerowany do pliku PDF.')

pdf.output("plan-realizacji-zakupu.pdf")
