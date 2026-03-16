function FormularBilet({ titlu, setTitlu, pret, setPret, client, setClient, onSave, esteEditare }) {
    return (
        <form onSubmit={onSave} style={{ marginBottom: '30px' }}>
            <input 
                type="text" 
                placeholder="nume film" 
                value={titlu} // folosim numele din antet
                onChange={(e) => setTitlu(e.target.value)}
                required 
                style={{ marginRight: '10px' }}
            />
            <input 
                type="text" 
                placeholder="nume client" 
                value={client} // folosim numele din antet
                onChange={(e) => setClient(e.target.value)}
                required 
                style={{ marginRight: '10px' }}
            />
            <input 
                type="number" 
                placeholder="pret" 
                value={pret} // folosim numele din antet
                onChange={(e) => setPret(e.target.value)}
                required 
                style={{ marginRight: '10px' }}
            />
            <button type="submit">
                {esteEditare ? 'salveaza modificarea' : 'adauga bilet'}
            </button>
        </form>
    );
}

export default FormularBilet;