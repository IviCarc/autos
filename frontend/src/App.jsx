import React from "react";
import Busqueda from "./components/busqueda";
import Header from './components/header.jsx'

const App = () => {
    return (
        <div className="App">
            <Header></Header>
            <Busqueda></Busqueda>
        </div>
    )
}

export default App;