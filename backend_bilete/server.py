from fastapi import fastapi, httpexception
from fastapi.middleware.cors import corsmiddleware
import json
import os

app = fastapi()

# permitem frontend-ului sa comunice cu backend-ul fara erori de cors
app.add_middleware(
    corsmiddleware,
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
        return json.load(f)

def salveaza_bilete(bilete):
    with open(fisier_db, "w") as f:
        json.dump(bilete, f, indent=4)

@app.get("/tickets")
def get_bilete():
    return citeste_bilete()

@app.post("/tickets", status_code=201)#modificam codul pt succes 201 craeted
def adauga_bilet(bilet_nou: dict):
   
    bilete = citeste_bilete()
    
    # gasim cel mai mare id si adaugam 1
    max_id = 0
    for bilet in bilete:
        if(bilet.get("id")>max_id):
           max_id=bilet.get("id")
    bilet_nou["id"] = max_id + 1
    
    bilete.append(bilet_nou)
    salveaza_bilete(bilete)
    
   
    return bilet_nou

@app.put("/tickets/{id_bilet}")
def modifica_bilet( bilet_actualizat: dict):
    id_bilet = bilet_actualizat.get("id")   
    bilete = citeste_bilete()
    for index, bilet in enumerate(bilete):
        if bilet.get("id") == id_bilet:
            bilet_actualizat["id"] = id_bilet
            bilete[index] = bilet_actualizat
            salveaza_bilete(bilete)
            return bilet_actualizat
            
    raise httpexception(status_code=404, detail="biletul nu a fost gasit")

@app.delete("/tickets/{id_bilet}")
def sterge_bilet(id_bilet: int):
    bilete = citeste_bilete()
    bilete_ramase = []
    for b in bilete:
        if b.get("id")!=id_bilet:
            bilete_ramase.append(b)
    if len(bilete) == len(bilete_ramase):
        raise httpexception(status_code=404, detail="biletul nu a fost gasit")
        
    salveaza_bilete(bilete_ramase)
    return {"mesaj": "bilet sters cu succes"}