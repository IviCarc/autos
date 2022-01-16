const mapFunc = (data) => {
    return data.map((obj, i) => {
        return (
            <ul key={i} className='datos-ul'>
                <li className='datos-li'>{obj.cliente}</li>
                <li className='datos-li'>{obj.modelo}</li>
                <li className='datos-li'id='trabajo'>{obj.trabajo}</li>
                <li className='datos-li'>{obj.km}</li>
                <li className='datos-li'>{obj.fecha}</li>
                <li className='datos-li'>{obj.patente}</li>
            </ul>
        )
    })
}

export default mapFunc;