import tkinter
from tkinter import Tk, Label
import urllib.request
import re
re.dotall = True

## Strona z której zaczytuje dane to mybank.pl, muszę zdekodować ją w standardzie utf-8
strona = urllib.request.urlopen('https://mybank.pl/kursy-walut/').read()
strona = strona.decode("utf-8")
## Strona zawierę tabelę z kursami. Tworzę listę, która zawiera wszystkie kursy
kursy = re.findall(r"<td>\d+,\d+</td>", strona)
## Tworzę ręcznie listę walut
waluty = ('Dolar amerykański USD', 'Euro EUR', 'Frank szwajcarski CHF', 'Funt szterling GBP', 'Bat tajlandzki THB',
          'Dolar australijski AUD', 'Dolar hongkoński HKD', 'Dolar kanadyjski CAD', 'Dolar nowozelandzki NZD',
          'Dolar singapurski SGD', 'Forint węgierski 100 HUF', 'Hrywna ukraińska UAH', 'Jen japoński 100 JPY',
          'Juan chiński CNY', 'Korona czeska CZK', 'Korona duńska DKK', 'Korona islandzka 100 ISK',
          'Korona norweska NOK', 'Korona szwedzka SEK', 'Lej rumuński RON', 'Lew bułgarski BŁG', 'Lita turecka TRY',
          'Peso chilijskie 100 CLP', 'Peso filipińskie PHP', 'Peso meksykańskie MXN', 'Rand (RPA) ZAR',
          'Real brazylijski BRL', 'Ringgit malezyjski MYR', 'Rupia indonezysjka 10000 IDR', 'Rupia indyjska 100 INR',
          'Szekel izraelski ISL', 'Won południowokoreański 100 KRW', 'Międzynarodowa SDR', 'Polski złoty PLN')

## Tworzę podstawę interfejsu graficznego
root = Tk()
root.title("Przelicznik walut")
root.geometry("300x400")
label = Label(fg="black", bg="white", width=50, text="Wprowadź kwotę:")
label.pack()
## Tworzę pole do wprowadzania kwoty
entry = tkinter.Entry(fg="black", bg="white", width=50)
entry.pack()
label1 = Label(fg="black", bg="white", width=50, text="Wybierz walutę z której chcesz przeliczyć:")
label1.pack()
var1 = tkinter.Variable(value=waluty)
var2 = tkinter.Variable(value=waluty)

## Tworzę pierwsze z okien gdzie umieszczę pierwszą listę i suwak
frame = tkinter.Frame(root)
frame.pack(fill='both')
## Tworzę suwak do pierwszej listy
scrollbar = tkinter.Scrollbar(frame)
scrollbar.pack(side="right", fill="y")
## Tworzę pierwszą listę wyboru
listbox = tkinter.Listbox(frame, height=5, exportselection=False, listvariable=var1, selectmode=tkinter.BROWSE)
listbox.config(yscrollcommand=scrollbar.set)
listbox.pack(fill="both")
scrollbar.config(command=listbox.yview)

label2 = Label(fg="black", bg="white", width=50, text="Wybierz walutę na którą chcesz przeliczyć:")
label2.pack()

## Tworzę drugie z okien gdzie umieszcze listę i suwak
frame2 = tkinter.Frame(root)
frame2.pack(fill="both")
## Tworzę drugą listę wyboru
listbox2 = tkinter.Listbox(frame2, height=5, exportselection=False, listvariable=var2, selectmode=tkinter.BROWSE)
## Tworzę drugi suwak
scrollbar2 = tkinter.Scrollbar(frame2)
scrollbar2.pack(side="right", fill="y")
listbox2.config(yscrollcommand=scrollbar2.set)
listbox2.pack(fill="both")
scrollbar2.config(command=listbox2.yview)
label3 = Label(fg="black", bg="white", width=50, text="Wynik:")
label3.pack()
## Tworzę pole gdzie wyświetlony będzie wynik
entry1 = tkinter.Entry(fg='black', bg='white', width=50)
entry1.pack()


def czyszczenie(event):
    """Funckja służy do czyszczenia wejścia gdy użytkownik najedzie na pole z którym w dalszej części kodu jest powiązana"""
    entry.delete(0, "end")


def funkcja():
    """
    Główna funckja programu
    Na początku czyszcze pole gdzie wyświetli się wynik.
    Zczytuje waluty wybrane przez użytkownika.
    Jeśli jedna z walut nie zostanie wybrana, program przerwie działanie i wyświetli komunikat o błędzie.
    Osobno rozpatruję przypadek gdy wybrane są złotówki których autor strony nie uwzględnił.
    W zapisie odpowiedniego kursu trzeba zamienić przecinek na kropkę.
    Następnie próbuje zamienić dane wprowadzone przez użytkownika na liczbę.
    Jeśli się nie uda, wyświetla odpowiedni komunikat i kończy działanie.
    Jeśli się uda, przelicza i wyświetla wynik.
    """
    entry1.delete(0, "end")
    waluta1 = listbox.curselection()
    waluta2 = listbox2.curselection()

    if len(waluta1) == 0 or len(waluta2) == 0:
        entry1.insert(0, "Wprowadź walutę!")
        return
    if waluta1[0] == 33:
        kurs1 = 1
    else:
        kurs1 = kursy[waluta1[0]]
        kurs1 = kurs1[4:-5]
        kurs1 = list(kurs1)
        kurs1[1] = "."
        kurs1 = "".join(kurs1)
        kurs1 = eval(kurs1)

    if waluta2[0] == 33:
        kurs2 = 1
    else:
        kurs2 = kursy[waluta2[0]]
        kurs2 = kurs2[4:-5]
        kurs2 = list(kurs2)
        kurs2[1] = "."
        kurs2 = "".join(kurs2)
        kurs2 = eval(kurs2)

    try:
        liczba = float(entry.get())
        wynik = round((kurs1 / kurs2 * liczba), 2)
        entry1.insert(0, wynik)
    except:
        entry.delete(0, "end")
        entry.insert(0, "Niepoprawne dane!")
        entry.bind("<FocusIn>", czyszczenie)


## Tworzę przycisk, którego naciśnięcie spowoduje wywołanie programu
button = tkinter.Button(text="Przelicz", command=funkcja)
button.pack()

root.mainloop()
