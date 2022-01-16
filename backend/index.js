const express = require('express');
const app = express();
require('dotenv').config();
const cors = require('cors');
const spawn = require('child_process').spawn;
const { getByClient, getClientsList, getByPatent, getByRegex, newRecord, getPatentsList} = require('./controllers.js');

app.use(cors());

app.use(express.json());

URL = process.env.URL || 'http://localhost:5000';


// CUANDO HAY ERRORES AL EJECUTARSE LAS FUNC EL SERVIDOR CRASHEA //
// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! //

app.get("/lista/clientes", getClientsList);

app.get("/lista/patentes", getPatentsList)

app.get('/cliente/:name', getByClient);

app.get('/patente/:patente', getByPatent);

app.get('/buscar/:regex', getByRegex);

app.post('/nuevo', newRecord);


app.listen(process.env.PORT | 5000, () => {
    console.log('Server listening on port', process.env.PORT || 5000);
})