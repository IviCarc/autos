import axios from "axios";
import React from "react";
import { useEffect, useState } from "react";
import mapFunc from "./functions/funcs";
import './nuevo.scss'

const Nuevo = () => {
    const [data, setData] = useState(false);
    const [error, setError] = useState(false)

    const [inputs, setInputs] = useState({
        cliente: {value:"", valid:null},
        auto: {value:"", valid:null},
        trabajo: {value:"", valid:null},
        km: {value:"", valid:null},
        fecha: {value:"", valid:null},
        patente: {value:"", valid:null}
    })

    const onChange = (e) => {
        const inputName = e.target.name;
        const inputValue = e.target.value;
        setInputs({
            ...inputs,
            [inputName] : {
                ...inputs[inputName],
                value: inputValue
            }
        })
    }

    const sendData = async (e) => {
        e.preventDefault();
        let data = {}
        for (const key in inputs) data[key] = inputs[key].value;
        console.log("DATA OBJECT",data)
        try {
            data = await axios.post('http://localhost:5000/nuevo', data);
        } catch (e) {
            console.log(e);
            return
        }

        console.log("AUTO AGREGADO")
    }

    return (
        <>
        <ul className='datos-ul'>
            <li className='datos-li'><input name='cliente' onChange={onChange} className='datos-input' type="text" /></li>
            <li className='datos-li'><input name='auto' onChange={onChange} className='datos-input' type="text" /></li>
            <li className='datos-li'><input name='trabajo' onChange={onChange} className='datos-input' type="text" /></li>
            <li className='datos-li'><input name='km' onChange={onChange} className='datos-input' type="text" /></li>
            <li className='datos-li'><input name='fecha' onChange={onChange} className='datos-input' type="text" /></li>
            <li className='datos-li'><input name='patente' onChange={onChange} className='datos-input' type="text" /></li>
        </ul>
        <button className='datos-btn send-btn' onClick={sendData}>Cargar</button>
        </>
    )

    // return (
    //     <div className='nuevo-container'>
    //         <form action="" className='form-container'>
    //             <div className="inputs-container">
    //                 <label htmlFor="">Cliente</label>
    //                 <input onChange={onChange} name='cliente' type="text" autoComplete='off'/>
    //             </div>
    //             <div className="inputs-container">
    //                 <label htmlFor="">Auto</label>
    //                 <input onChange={onChange} name='auto' type="text" autoComplete='off'/>
    //             </div>
    //             <div className="inputs-container">
    //                 <label htmlFor="">Trabajo</label>
    //                 <textarea onChange={onChange} name="trabajo" id="trabajo" ></textarea>
    //             </div>
    //             <div className="inputs-container">
    //                 <label htmlFor="">Km</label>
    //                 <input onChange={onChange} name='km' type="number" autoComplete='off'/>
    //             </div>
    //             <div className="inputs-container">
    //                 <label htmlFor="">Fecha</label>
    //                 <input onChange={onChange} name='fecha' type="date" autoComplete='off'/>
    //             </div>
    //             <div className="inputs-container">
    //                 <label htmlFor="">Patente</label>
    //                 <input onChange={onChange} name='patente' type="text" autoComplete='off'/>
    //             </div>
    //             <button className='send-btn' onClick={sendData}>Cargar</button>
    //         </form>
    //     </div>
    // )
}

export default Nuevo