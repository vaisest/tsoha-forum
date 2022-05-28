# Tsohit

## Yleistä

Tässä repositoriossa on [Tsoha-kurssin](https://hy-tsoha.github.io/materiaali/) projekti, jonka ideana on Reddit-tyylinen keskustelupalsta.  
Sovellus toteutetaan Flask:lla, PostgreSQL:lla ja se tulee olemaan saatavilla Herokussa.

## Sovelluksen käyttö

Sovellus vaatii jonkin verran konfiguraatiota ennen käyttöä. Käyttöön vaaditaan PostgreSQL palvelin, jonka osoite täytyy lisätä `.env` tiedostoon tai ympäristömuuttujaan `SQLALCHEMY_DATABASE_URI`. Samoin täytyy myös tehdä muuttujalle `SECRET_KEY`, joka täytyy asetta joksikin uniikiksi arvoksi.

Sovellus on Herokussa osoitteessa [tsohit.herokuapp.com](https://tsohit.herokuapp.com).

Sovellusta voidaan myös käyttää paikalliesti Linuxilla seuraavasti:

```bash
python -m venv venv # uusi virtuaaliympäristö
source venv/bin/activate # luodun ympäristön aktivointi

pip install -r requirements.txt # riippuvuuksien asennus
gunicorn wsgi:app # sovelluksen käynnistys

# Viimeiset kaksi komentoa kannattaa korvata näillä
# jos tavoitteena on kehittää sovellusta:
pip install -r requirements/dev.txt
FLASK_ENV=development flask run # debug versio
```

## Kehitys

Tiedostossa `requirements/dev.txt` on muutamia tämän sovelluksen kehittämiseen käytettyjä työkaluja. Kaikki projektin koodi on formatoitu Black-työkalulla, mitä voidaan käyttää komennolla `black --line-length 95 app`.  
Lisätarkastukseen voidaan käyttä Flake8-komentoa seuraavasti: `flake8 --max-line-length 95 app`.

## Sovelluksen toimintoja

- Käyttäjiä voi lisätä ja sovelluksessa on tavallinen kirjautumistoiminto. Ylläpitällä on oma käyttäjä, jolla on erikoisoikeuksia.

- Käyttäjä voi lisätä ja poistaa omia kommenttejansa.

- Käyttäjät voivat lisätä ja selata uusia keskustelualueita, jotka toimivat alisivuina. Ylläpitäjä voi poistaa alueita.

- Alueelle (ei pääsivulle) voi luoda uusia ketjuja, joissa on otsikko, leipäteksti ja kommentteja. Kommenteilla voi olla myös alikommentteja.

- Sekä kommentteja että ketjuja voi äänestää ylös tai alas.

- Käyttäjän sivulta voidaan nähdä kaikki käyttäjän kommentit ja ketjut eri alueilta.
