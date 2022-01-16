import React from "react";
import { useEffect, useState } from "react";
import axios from 'axios';
import './busqueda.scss';
import Nuevo from './nuevo.jsx'
import mapFunc from "./functions/funcs";

const Busqueda = () => {
    const [cliente, setCliente] = useState("");
    const [patente, setPatente] = useState("");
    const [data, setData] = useState(false);
    const [error, setError] = useState(false);
    const [errMsg, setErrMsg] = useState("");
    const [autocmpDataClients, setAutocmpDataClients] = useState(false)
    const [autocmpDataPatentes, setAutocmpDataPatentes] = useState(false)

    const getAll = async () => {
        try {
            const res = await (await axios.get(`http://localhost:5000/lista/clientes`)).data;
            setAutocmpDataClients(res)
        } catch (e) {
            setAutocmpDataClients(false)
            console.log(e)
        }
        try {
            const res = await (await axios.get(`http://localhost:5000/lista/patentes`)).data
            setAutocmpDataPatentes(res)
        } catch (e) {
            setAutocmpDataPatentes(false)
            console.log(e)
        }    
    }

    useEffect(getAll, [])

    const onChangeCliente = (e) => {
        setCliente(e.target.value);
    }
    const onChangePatente = (e) => {
        setPatente(e.target.value);
    }

    const send = async (e, valueSending) => {
        e.preventDefault();
        let url;
        if (valueSending === 1){
            url = `http://localhost:5000/cliente/${cliente}`
            setErrMsg(`El cliente '${cliente} no existe'`);
        } else {
            url = `http://localhost:5000/patente/${patente}`
            setErrMsg(`La patente '${patente}' no existe`);
        }
        let res
        try {
            res = await (await axios.get(url)).data;
            
        }catch(e) {
            setData(false)
            setError(e.response.status);
            return
        }
        setData(res);
        setError(false)
    }

    
    return (
        <div className='cliente'>
            <div className='forms-container'>
            <form action="">
                <label htmlFor="cliente">Nombre del cliente:</label>
                <input autoComplete='off' list='clientes-datalist' onChange={onChangeCliente} type="text" name='cliente'/>
                <datalist id='clientes-datalist'>
                    {autocmpDataClients && (
                        autocmpDataClients.map((obj, i) => <option key={i}>{obj.Cliente}</option>)
                    )}
                </datalist>
                <button onClick={(e) => send(e, 1)}>Buscar</button>
            </form>
            <form action="">
                <label htmlFor="cliente">Patente:</label>
                <input onChange={onChangePatente} autoComplete='off' list='patentes-datalist' type="text" name='cliente'/>
                <datalist id='patentes-datalist'>
                    {autocmpDataPatentes && (
                        autocmpDataPatentes.map((obj, i) => <option key={i}>{obj.patente}</option>)
                    )}
                </datalist>
                <button onClick={(e) => send(e,0)}>Buscar</button>
            </form>
            </div>
            <div className='datos-container'>
                <ul className='datos-ul titulos'>
                    <li className='datos-li titulo'>Cliente</li>
                    <li className='datos-li titulo'>Auto</li>
                    <li className='datos-li titulo'id='trabajo'>Trabajo</li>
                    <li className='datos-li titulo'>Km</li>
                    <li className='datos-li titulo'>Fecha</li>
                    <li className='datos-li titulo'>Patente</li>
                </ul>
                <Nuevo></Nuevo>

                {
                    data  && mapFunc(data)
                }
            </div>
            
            {error === 400 && (
                <h2 style={{color:"red", textAlign:'center'}}>{errMsg}</h2>
            )}
        </div>
    )
}

export default Busqueda;