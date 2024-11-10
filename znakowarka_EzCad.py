
import os
import re
import datetime
import subprocess
import time
import pyautogui
import pygetwindow as gw

#Definicje:
katalog=os.getcwd()
full_path_txt=str(katalog) + "\\" +'wynik.txt'
full_path_ezd=str(katalog) + "\\" +'laser.ezd'
klawisz=''
domyslna_aplikacja = r"C:\EZCAD_LITE_2.14.16(20210519)\EzCad2.exe"



#===================================================================================================================================
def zapisz_do_pliku(nazwa_pliku, dane):
    with open(nazwa_pliku, 'w') as plik:
        plik.write(dane)
        print('Zapisano dane do pliku: '+str(nazwa_pliku))



#===================================================================================================================================
def czy_plik_istnieje_i_aktualny(nazwa_pliku, czas_max_minuty=1):
    if os.path.exists(nazwa_pliku):
        mtime = os.path.getmtime(nazwa_pliku)
        mtime_dt = datetime.datetime.fromtimestamp(mtime)
        czas_teraz = datetime.datetime.now()
        roznica_czasu = czas_teraz - mtime_dt
        if roznica_czasu.total_seconds() / 60 <= czas_max_minuty:
            return True
    return False



#===================================================================================================================================
def multi_input():
    try:
        etykieta =''  
        lista = []
        licz = 1
        last = ''

        print("Wprowadź kod QR:")
        
        while True:
            wrd = input()
            #print(wrd)
            #print("-$$$$$$-")
            if licz > 4 and len(wrd) < 1: break
            else:
                if len(wrd) > 3:
                    lista.append(str(wrd))
                    licz = licz + 1
                else:
                    if  wrd.isdigit() and len(wrd) > 3:
                        #print(wrd)
                        #print("-- !! --")
                        lista.append(str(wrd))
                        licz = licz + 1
                    else:
                        re1 = re.match("^PK ",last)
                        re2 = re.match("^PKA ",last)
                        if re1 or re2:
                            wymiar = re.findall("[0-9]{2,3}\*[0-9]{2,3}\*[0-9]{2,3}",last)
                            gatunek = re.findall("/(.*)/",last)
                            lista.append(wymiar[0].replace("*", "x"))
                            lista.append(str(gatunek[0]))
                            licz = licz + 1
                        else:
                            licz = licz + 1
            last = wrd
            #print(lista)
            #print("- ####### -")

    #What if ther user press the interruption shortcut? 
    except KeyboardInterrupt:
        print("program został zakończony przez użytkownika.")
        return

    if(len(lista)>0):
        #etykieta = '\n'.join(lista)
        etykieta = '\n'.join(lista)
        if len(etykieta) < 40:
            #raise Exception("cause of the problem")
            return ("99#9")
        else:
                #PN = lista[len(lista)-1]
                #PN = PN[4:]
                #print(len(etykieta))
                #print('Wprowadziłeś etykietę:')
                #print(etykieta)
            print('\n')
            return   (etykieta)
    else:
        return ("99#9")





#===================================================================================================================================
def uruchom_aplikacje_i_nacisnij_klawisze(nazwa_pliku,domyslna_aplikacja):

    # Uruchamia plik przy użyciu domyślnej aplikacji
    subprocess.Popen([domyslna_aplikacja, nazwa_pliku])

    # Czekaj na uruchomienie aplikacji i przydzielenie jej czasu na aktywację
    time.sleep(2)

    # Pobierz listę okien
    okna = gw.getWindowsWithTitle("EzCad2")
    print(okna)

    # Sprawdź, czy okno Notatnika jest aktywne
    for okno in okna:
        if "laser.ezd" in okno.title:
            # Ustaw focus na oknie aplikacji
            okno.activate()



            pyautogui.click(900,508)
            pyautogui.doubleClick(85,720)
            pyautogui.doubleClick(900,508)          

            #symuluj wklejenie tekstu etykiety
            pyautogui.typewrite(etykieta_global)

            pyautogui.hotkey('alt', 'o')


            try:
                while True:
                    # Symuluj naciśnięcie klawisza
                    pyautogui.press(klawisz)
                    print('zaznaczenie obszaru wypalania na płycie wpisz 1, wypalenie Laserem wpisz 2, koniec wpisz 3')
                    klawisz=jaki_klawisz()
                    if klawisz=="99#9":
                        print('błędny wybór')
                    if klawisz=='1':
                        pyautogui.press('f1')
                        time.sleep(10)
                        pyautogui.press('enter')
                        time.sleep(2)
                        zamknij_okna()
                    if klawisz=='2':
                        print('Jeżeli wszystko jest gotowe do wypalenia, wpisz "y"')
                        try:
                            check = input()
                            if len(check) > 0 and (check == 'y' or check.lower() == 'y'):
                                pyautogui.press('f2')
                                time.sleep(10)
                                zamknij_okna()
                                break
                        #What if ther user press the interruption shortcut? 
                        except KeyboardInterrupt:
                            print("program został zakończony przez użytkownika.")

                    if klawisz=='3':
                        zamknij_okna()
                        break
                #What if ther user press the interruption shortcut? 
            except (ValueError, RuntimeError, TypeError, EOFError, KeyboardInterrupt):
                print("program został zakończony.")        
            return


#===================================================================================================================================
def zamknij_okna():
    okna = gw.getWindowsWithTitle("EzCad2")
    for okno in okna:
        if 'laser.ezd' in okno.title:
            okno.close()



#===================================================================================================================================
def jaki_klawisz():
    #wynik=''
    #print("Podaj klawisz")
    try:

        while True:
            wrd = input()
            if len(wrd) > 0 and str(wrd).isdigit:
                return (wrd)
            else:
                return ("99#9")

    #What if ther user press the interruption shortcut? 
    except KeyboardInterrupt:
        print("program został zakończony przez użytkownika.")
        return




#MAIN
#===================================================================================================================================
try:
    while True:            
        stop=0
        etykieta_global = multi_input()
        #print(etykieta_global)

        if etykieta_global == "99#9":
            stop=1


        if stop==0:
            stop2=0
            zapisz_do_pliku(full_path_txt, str(etykieta_global))
            czy_plik=czy_plik_istnieje_i_aktualny(full_path_txt, 1)
            if czy_plik:
                print('plik istnieje i jest aktualny')
            else:
                stop2=1

            if stop2==0:
                zamknij_okna()
                try:
                    while True:

                        """print('zaznaczenie obszaru wypalania na płycie wpisz 1, wypalenie Laserem wpisz 2, koniec wpisz 3')
                        klawisz=jaki_klawisz()
                        if klawisz=="99#9":
                            print('błędny wybór')
                        if klawisz=='1':"""
                        uruchom_aplikacje_i_nacisnij_klawisze(full_path_ezd,domyslna_aplikacja)
                        """ time.sleep(10)
                            pyautogui.press('enter')
                            time.sleep(2)
                            zamknij_okna()
                        if klawisz=='2':"""
                        """print('Jeżeli wszystko jest gotowe do wypalenia, wpisz "y"')
                            try:
                                check = input()
                                if len(check) > 0 and (check == 'y' or check.lower() == 'y'):
                                    uruchom_aplikacje_i_nacisnij_klawisze(full_path_ezd,domyslna_aplikacja,'f2')
                                    time.sleep(10)
                                    zamknij_okna()
                                    break
                            #What if ther user press the interruption shortcut? 
                            except KeyboardInterrupt:
                                print("program został zakończony przez użytkownika.")"""
                        """if klawisz=='3':
                            zamknij_okna()
                            break"""
                        
                #What if ther user press the interruption shortcut? 
                except (ValueError, RuntimeError, TypeError, EOFError, KeyboardInterrupt):
                    print("program został zakończony.")
        
            else:
                print('wczytaj ponownie etykiete, wystąpil problem z zapisem do pliku')
        

 






#What if ther user press the interruption shortcut? 
except (ValueError, RuntimeError, TypeError, EOFError, KeyboardInterrupt):
        print("program został zakończony.")

@copyright Artur Szymkiewicz