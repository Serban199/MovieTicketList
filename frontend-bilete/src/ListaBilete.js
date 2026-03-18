function ListaBilete({ bilete, onSterge, onEdit }) {
  return (
    <ul style={{ listStyle: 'none', padding: 0 }}>
      {bilete.map(bilet => (
        <li key={bilet.id} style={{ marginBottom: '20px', padding: '15px', border: '1px solid #ccc', borderRadius: '8px', textAlign: 'left', maxWidth: '600px', margin: '0 auto 20px' }}>
          
          <div style={{ marginBottom: '10px', fontSize: '18px' }}>
            film: {bilet.movie_title} | client: {bilet.customer_name} | pret: {bilet.price} lei          </div>
          
          <div style={{ marginBottom: '10px', color: '#444' }}>
            nota imdb: {bilet.scor_film ? bilet.scor_film : 'se incarca...'}
          </div>

          {}
          {bilet.stiri_film && bilet.stiri_film.length > 0 && (
            <div style={{ marginBottom: '15px', fontSize: '14px' }}>
              stiri recente:
              <ul style={{ paddingLeft: '20px', marginTop: '5px' }}>
                {bilet.stiri_film.map((stire, index) => (
                  <li key={index} style={{ marginBottom: '5px' }}>
                    <a href={stire.url} target="_blank" rel="noreferrer" style={{ color: '#0066cc', textDecoration: 'none' }}>
                      {stire.title}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          )}

          <div>
            <button 
              onClick={() => onEdit(bilet)} 
              style={{ color: 'blue', cursor: 'pointer' }}
            >
              editeaza
            </button>

            <button 
              onClick={() => onSterge(bilet.id)} 
              style={{ marginLeft: '10px', color: 'red', cursor: 'pointer' }}
            >
              sterge
            </button>
          </div>
          <div style={{ marginBottom: '10px', fontSize: '18px' }}>
            film: {bilet.movie_title} | client: {bilet.customer_name} | pret: {bilet.price} lei
          </div>
          
          <div style={{ marginBottom: '10px', color: '#444' }}>
            nota imdb: {bilet.scor_film ? bilet.scor_film : 'se incarca...'}
          </div>

          <div style={{ marginBottom: '10px', color: '#0066cc', fontSize: '14px' }}>
            locatie cinema: {bilet.adresa_cinema ? bilet.adresa_cinema : 'se incarca...'}
          </div>
        </li>
      ))}
    </ul>
  );
}

export default ListaBilete;