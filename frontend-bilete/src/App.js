import { useState, useEffect } from 'react';
import './App.css';
import FormularBilet from './FormularBilet';
import ListaBilete from './ListaBilete';

function App() {
  // variabila care pastreaza biletele
  const [bilete, setBilete] = useState([]);
  
  // variabile de memorie pentru formular
  const [titluFilm, setTitluFilm] = useState('');
  const [numeClient, setNumeClient] = useState('');
  const [pret, setPret] = useState('');
  const [idBiletModificat, setIdBiletModificat] = useState(null);//variabila pt id ul biletelor mod

  // am mutat cererea get intr-o functie separata ca sa o putem refolosi
  const incarcaBilete = () => {
    fetch('http://localhost:8081/tickets')
      .then(raspuns => raspuns.json())
      .then(date => setBilete(date))
      .catch(eroare => console.log('eroare la conectare:', eroare));
  };

  const stergeBilet = (id) => {
    // am schimbat ghilimelele aici in backticks
    fetch(`http://localhost:8081/tickets/${id}`, {
      method: 'DELETE'
    })
      .then(raspuns => {
        if(raspuns.ok) {
          incarcaBilete(); // reincarca lista de bilete dupa stergere
        } else {
          console.log('eroare la stergerea biletului:', raspuns.statusText);
        }})
      
  };

  // se apeleaza automat o singura data cand deschizi pagina
  useEffect(() => {
    incarcaBilete();
  }, []);

  // functia care trimite datele noi la python cand apesi butonul
  const adaugaBilet = (eveniment) => {
    eveniment.preventDefault(); // opreste browserul din a da refresh la pagina

    // construim pachetul cu date exact cum il asteapta python
    const biletNou = {
      movie_title: titluFilm,
      customer_name: numeClient,
      price: pret
    };

    // trimitem pachetul cu post
    fetch('http://localhost:8081/tickets', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(biletNou)
    })
    .then(raspuns => {
      if (raspuns.ok) {
        // curatam casutele formularului dupa succes
        setTitluFilm('');
        setNumeClient('');
        setPret('');
        // cerem iar lista de bilete de la server ca sa apara biletul nou
        incarcaBilete();
      }
    })
    .catch(eroare => console.log('eroare la adaugare:', eroare));
  }; // aici am pus acolada care inchide corect functia de adaugare

  // acum functia de modificare este libera si complet separata
  const modificaBilet = (eveniment) => {
    eveniment.preventDefault();

    const biletActualizat = {
      movie_title: titluFilm,
      customer_name: numeClient,
      price: pret
    };

    fetch(`http://localhost:8081/tickets/${idBiletModificat}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(biletActualizat)
    })
    .then(raspuns => {
      if (raspuns.ok) {
        incarcaBilete(); // reincarca lista de bilete dupa stergere
        
        setTitluFilm('');
        setNumeClient('');
        setPret('');
        setIdBiletModificat(null);
      } else {
        console.log('eroare la modificare:', raspuns.statusText);
      }
    })
    .catch(eroare => console.log('eroare:', eroare));
  };
  
  const pregatesteEditare = (bilet) => {
    setTitluFilm(bilet.movie_title);
    setNumeClient(bilet.customer_name);
    setPret(bilet.price);
    setIdBiletModificat(bilet.id);
  };

  // aici este partea vizuala care iti lipsea si care leaga totul
  return (
    <div className="App" style={{ padding: '20px' }}>
      <h1>sistem de gestiune bilete</h1>

      <FormularBilet 
        titlu={titluFilm} 
        setTitlu={setTitluFilm}
        client={numeClient} 
        setClient={setNumeClient}
        pret={pret} 
        setPret={setPret}
        onSave={idBiletModificat ? modificaBilet : adaugaBilet}
        esteEditare={!!idBiletModificat}
      />

      <hr />

      <ListaBilete 
        bilete={bilete} 
        onSterge={stergeBilet} 
        onEdit={pregatesteEditare} 
      />
    </div>
  );
}

export default App;