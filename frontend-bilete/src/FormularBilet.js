function FormularBilet({ titlu, setTitlu, pret, setPret, client, setClient, onSave, esteEditare, onCancel }) {
    return (
        <form onSubmit={onSave} style={{ marginBottom: '30px' }}>
            <input 
                type="text" 
                placeholder="nume film" 
                value={titlu} 
                onChange={(e) => setTitlu(e.target.value)}
                required 
                style={{ marginRight: '10px' }}
            />
            <input 
                type="text" 
                placeholder="nume client" 
                value={client} 
                onChange={(e) => setClient(e.target.value)}
                required 
                style={{ marginRight: '10px' }}
            />
            <input 
                type="number" 
                placeholder="pret" 
                value={pret} 
                onChange={(e) => setPret(e.target.value)}
                required 
                style={{ marginRight: '10px' }}
            />
            <button type="submit">
                {esteEditare ? 'salveaza modificarea' : 'adauga bilet'}
            </button>
            
            {}
            {esteEditare && (
                <button type="button" onClick={onCancel} style={{ marginLeft: '10px' }}>
                    anuleaza
                </button>
            )}
        </form>
    );
}

export default FormularBilet;