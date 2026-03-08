from gpiozero import LED, Button, Buzzer
from signal import pause
from time import sleep, time

# Hardware 
groen = LED(18)
rood = LED(23)
knop1 = Button(4, bounce_time=0.05)
knop2 = Button(17, bounce_time=0.05)
buzzer = Buzzer(24)

# Toestanden
toestand = "uit"   
PIN_CODE = [1, 2, 2, 1]
invoer = []
laatste_druk = 0
foute_pogingen = 0

# Beginstatus
groen.on()
rood.off()

def piep(aantal, duur=0.1):
    for _ in range(aantal):
        buzzer.on()
        sleep(duur)
        buzzer.off()
        sleep(0.1)

def start_alarm():
    global toestand
    toestand = "alarm"
    print("!!! ALARM GAAT AF !!!")
    rood.blink(on_time=0.2, off_time=0.2)
    buzzer.beep(on_time=0.2, off_time=0.2)

def stop_alarm():
    rood.off()
    buzzer.off()

def start_lockout():
    global toestand
    toestand = "lockout"
    print("!!! LOCKOUT — SYSTEEM GEBLOKKEERD !!!")
    rood.blink(on_time=0.1, off_time=0.1)
    buzzer.beep(on_time=0.1, off_time=0.1)

def controleer_pin():
    global invoer, toestand, foute_pogingen

    if invoer == PIN_CODE:
        print("PIN correct - Alarm uitgeschakeld")
        invoer = []
        foute_pogingen = 0
        toestand = "uit"

        stop_alarm()
        groen.on()
        rood.off()
        piep(2)
    else:
        foute_pogingen += 1
        print(f"FOUTE PIN – poging {foute_pogingen}/3")
        invoer = []
        piep(3)

        if foute_pogingen >= 3:
            start_lockout()
        elif toestand == "aan":
            start_alarm()

def registreer_druk(knop_nr):
    global toestand, invoer, laatste_druk

    nu = time()

    # LOCKOUT 
    if toestand == "lockout":
        print("Systeem is geblokkeerd. Herstart vereist.")
        return

    #TOESTAND: uit
    if toestand == "uit":
        if knop_nr == 1:
            toestand = "aan"
            groen.off()
            rood.on()
            print("Alarm is INGESCHAKELD")
            piep(1)
        return

    # TOESTANDEN: aan of alarm
    # Timeout check
    if invoer and (nu - laatste_druk) > 5:
        print("Timeout! Invoer gewist.")
        invoer = []

    laatste_druk = nu

    
    invoer.append(knop_nr)
    print(f"Invoer: {'*' * len(invoer)}")

    if len(invoer) == len(PIN_CODE):
        controleer_pin()


knop1.when_pressed = lambda: registreer_druk(1)
knop2.when_pressed = lambda: registreer_druk(2)

pause()