from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import requests
import uvicorn

url_baza_omdb = "http://www.omdbapi.com/?apikey=f7f7b53&t="
url_baza_news = "https://newsapi.org/v2/everything?apiKey=a280d9a720cf41f899cd40221544623d&q="

app = FastAPI()

# permitem frontend-ului sa comunice cu backend-ul fara erori de cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fisier_db = "db.json"

def citeste_bilete():
    if not os.path.exists(fisier_db):
        return []
    with open(fisier_db, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def salveaza_bilete(bilete):
    with open(fisier_db, "w") as f:
        json.dump(bilete, f, indent=4)

@app.get("/tickets")
def get_bilete():
    bilete = citeste_bilete()
    
    for b in bilete:
        nume_film = b.get("movie_title")        
        if nume_film:
            nume_curat = nume_film.strip()
            
            try:
                scor_url = url_baza_omdb + nume_curat
                raspuns_omdb = requests.get(scor_url, timeout=5)
                date_omdb = raspuns_omdb.json()
                if date_omdb.get("Response") == "True":
                    b["scor_film"] = date_omdb.get("imdbRating")
                else:
                    b["scor_film"] = "n/a"
            except:
                b["scor_film"] = "n/a"

            try:
                stiri_url = url_baza_news + nume_film
                raspuns_news = requests.get(stiri_url, timeout=5)
                date_news = raspuns_news.json()
                b["stiri_film"] = date_news.get("articles", [])[:2]
            except:
                b["stiri_film"] = []

            try:
                url_harti = "https://nominatim.openstreetmap.org/search?format=json&q=cinema+city+iasi"
                headere = {'user-agent': 'proiect_facultate_bilete'}
                raspuns_harti = requests.get(url_harti, headers=headere, timeout=5)
                date_harti = raspuns_harti.json()
                if len(date_harti) > 0:
                    b["adresa_cinema"] = date_harti[0].get("display_name")
                else:
                    b["adresa_cinema"] = "n/a"
            except:
                b["adresa_cinema"] = "n/a"
                
    return bilete

@app.post("/tickets", status_code=201)#modificam codul pt succes 201 craeted
def adauga_bilet(bilet_nou: dict):
    bilete = citeste_bilete()
    
    # gasim cel mai mare id si adaugam 1
    max_id = 0
    for bilet in bilete:
        if bilet.get("id", 0) > max_id:
            max_id = bilet.get("id")
    
    bilet_nou["id"] = max_id + 1
    
    bilete.append(bilet_nou)
    salveaza_bilete(bilete)
    return bilet_nou

@app.put("/tickets/{id_bilet}")
def modifica_bilet(id_bilet: int, bilet_actualizat: dict):
    bilete = citeste_bilete()
    
    for index, bilet in enumerate(bilete):
        if bilet.get("id") == id_bilet:
            bilet_actualizat["id"] = id_bilet
            bilete[index] = bilet_actualizat
            salveaza_bilete(bilete)
            return bilet_actualizat
            
    raise HTTPException(status_code=404, detail="biletul nu a fost gasit")

@app.delete("/tickets/{id_bilet}")
def sterge_bilet(id_bilet: int):
    bilete = citeste_bilete()
    bilete_initiale = len(bilete)
    
    bilete_ramase = [b for b in bilete if b.get("id") != id_bilet]
    
    if len(bilete_ramase) == bilete_initiale:
        raise HTTPException(status_code=404, detail="biletul nu a fost gasit")
        
    salveaza_bilete(bilete_ramase)
    return {"mesaj": "bilet sters cu succes"}

# pornire automata daca rulezi fisierul direct din vscode
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8081)