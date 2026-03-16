
function ListaBilete({ bilete, onSterge, onEdit }) {
  return (
    <ul>
      {bilete.map(bilet => (
        <li key={bilet.id} style={{ marginBottom: '10px' }}>
          film: {bilet.movie_title} | client: {bilet.customer_name} | pret: {bilet.price} lei
          
          <button 
            onClick={() => onEdit(bilet)} 
            style={{ marginLeft: '15px', color: 'blue' }}
          >
            editeaza
          </button>

          <button 
            onClick={() => onSterge(bilet.id)} 
            style={{ marginLeft: '10px', color: 'red' }}
          >
            sterge
          </button>
        </li>
      ))}
    </ul>
  );
}

export default ListaBilete;