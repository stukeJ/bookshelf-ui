# Kirjateline • Lukuseuranta ja Lukupöytä UI

Puhdas, vaalea ja skandinaavisen minimalistinen lukupöytäsovellus rakennettuna [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) -kirjastolla. Suunniteltu toimimaan sekä PC:llä että Raspberry Pi -kosketusnäytöllä varustetussa puisessa kirjatelineessä.

---

## ✨ Ominaisuudet

- **Kaikki toiminnot samassa ikkunassa (ei erillisiä ponnahdusikkunoita)**:
  - Sovellus ei avaa erillisiä popup-ikkunoita, vaan päänäkymä vaihtuu sulavasti kosketusnäppäimistöön ja takaisin.
- **"Uusi kirja" (vasen yläkulma)**:
  - Painettaessa `Uusi kirja` näkymä vaihtuu suoraan puhtaaseen numpadiin, jolla syötetään uuden kirjan kokonaissivumäärä (ei esimerkkipainikkeita, vain selkeä kosketusnäppäimistö).
  - Vahvistettaessa ("Aloita kirja ✓") näkymä palaa päänäkymään ja päivittyy uuden kirjan sivumäärälle (`0 / X sivua`).
- **Sivun merkintä ("Päivitä sivu, jolla olet")**:
  - Vaihtuu samassa ikkunassa puhtaaseen numpadiin, josta voi merkitä nykyisen sivun.
- **15 sekunnin lepotila (Musta näyttö + iso Progress Bar)**:
  - Jos näyttöön ei kosketa 15 sekuntiin, näyttö pimenee kokonaan mustaksi.
  - Keskellä näkyy ainoastaan suuri esteettinen edistymispalkki ja sivumäärä/prosentit ilman mitään häiritseviä tekstejä.
  - Kosketus herättää näytön välittömästi takaisin.
- **Lukusuora / Streak**:
  - Oikeassa yläkulmassa siisti teksti- ja numerolaatta (`🔥 7 Päivän Putki`).

---

## 🚀 Käynnistys Windowsilla

```powershell
pip install -r requirements.txt
python main.py
```

---

## 🍓 Käynnistys Raspberry Pi:llä

```bash
# 1. Asenna Tkinter-kirjastot
sudo apt update
sudo apt install -y python3-tk python3-pil python3-pil.imagetk

# 2. Luo virtuaaliympäristö ja asenna riippuvuudet
cd ~/kirjateline
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Käynnistä
python3 main.py
```
*(Jos käytät vanhempaa Python 3.7.3 -versiota: `pip install "customtkinter<=5.1.3" "pillow<10.0.0"`)*
