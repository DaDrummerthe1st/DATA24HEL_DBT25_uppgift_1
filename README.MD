# Skoluppgift DAT24HEL_DBT25_Uppgift_1
## Undervisningsmaterial
[GitHub-repo](https://github.com/schizoakustik/DATA24HEL_DBT25.git)
## Språk
- Kommentarer: engelska
- Hjälptext: svenska
- Svar på frågor: svenska
## Tidpunkt
Projektet startade 6 februari 2025
## Skapare av detta repo
Joakim Reuterborg

## I uppgiften har jag:
1. Besvarat frågorna från [läroboken](https://github.com/AntonioPrgomet/laer_dig_databaser_och_sql_1uppl)
2. Skapat, redogjort för och uppvisat resultatet av en kontakt med data mot Redis
3. Skapat, redogjort för och uppvisat resultatet av en kontakt med MongoDB
4. Skapat en Streamlit-app för att uppvisa resultatet av MongoDb-resultatet samt [deployat](https://dadrummerthe1st-data24hel-dbt25-uppgift-1-main-drvwk7.streamlit.app/) den till Streamlit Communuity server
5. Transponerat [movies.json](data/movies/movies.json) till [sex individuella filer](./csv_neo4j/). Jag valde att inte ta bort någon data / kolumn, istället är Null-celler ersatta med siffran 0. En reflektion är att jag skulle velat lägga ner ännu mer tid på denna punkt, även om jag tvingats iterera när jag, ofta av en slump, hittat fel.
   1. movies.csv - 4 919 st filmer
   2. actors.csv - 6 255 st skådespelare
   3. genres.csv - 26 st genrer
   4. actors_movies.csv - kopplingstabell (csv) mellan actors och movies
   5. genre_movies.csv - kopplingstabell (csv) mellan genrer och filmer
   6. directors.csv - håller endast regissörens namn, pekning sker från movies.csv.

## Min filstruktur
- [Huvudsakligt svarsdokument - Jupyter Notebook](./kunskapskontroll_1.ipynb)
- [Streamlit - appens källkod](./main.py)
- [Streamlit deployed version](https://dadrummerthe1st-data24hel-dbt25-uppgift-1-main-drvwk7.streamlit.app/)
- [requirements.txt - från pip freeze](./requirements.txt)
- mappstruktur
  - [data - rådata](./data/)
  - [csv-filer för Neo4j](./csv_neo4j/)
  - [svaren för Neo4j-frågorna, besvaras även samlat i Huvudsakligt svarsdokument](./neo4j_answers/)
- Lösenordsfilerna är inte inkluderade i repot

## Kvar att göra:
- Skriva klart denna README-fil
- Uppgift 3 Neo4j
- Uppgift 4 Neo4j
- Hårdkoda Dataframen till Streamlit-appen eftersom jag annars måste visa upp mina inloggningsdetaljer i repot