const spawn = require('child_process').spawn;

const controller = {}

controller.getByClient = (req, res) => {
    const {name} = req.params;
    ls = spawn('python3', ['python/autos.py', '-c', name, 'true']); 

    ls.stdout.on('data', data => {
        data = data.toString()

        console.log(data)

        if (data[0] === "0"){
            console.log("a")
            // Agregar status?
            // res.send('El cliente ingresado no existe')
            res.sendStatus(400)
            return
        }

        jsonData = JSON.parse(data)
        console.log(jsonData)
        res.send(jsonData);
    })
    
    ls.stderr.on('data', (data) => {
        console.log(`stderr: ${data}`);
    });
    
    ls.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
    });
}

controller.getPatentsList = (req, res) => {
    ls = spawn('python3', ['python/autos.py', '-lp','true']);

    ls.stdout.on('data', data => {
        data = data.toString()
        jsonData = JSON.parse(data)
        console.log(jsonData)
        res.send(jsonData);
    })

    ls.stderr.on('data', (data) => {
        console.log(`stderr: ${data}`);
    });

    ls.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
    });
}

controller.getClientsList = (req, res) => {
    ls = spawn('python3', ['python/autos.py', '-lc','true']);

    // console.log(ls)

    ls.stdout.on('data', data => {
        
        data = data.toString()
        console.log(data)

        jsonData = JSON.parse(data)
        console.log(jsonData)
        res.send(jsonData);
    })

    ls.stderr.on('data', (data) => {
        console.log(`stderr: ${data}`);
    });

    ls.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
    });
}

controller.getByPatent = (req, res) => {
    const {patente} = req.params;
    ls = spawn('python3', ['python/autos.py', '-p', patente, 'true']); 

    ls.stdout.on('data', data => {
        data = data.toString();

        if (data[0] === '0'){
            // res.send('La patente ingresada no existe');
            res.sendStatus(400);
            return;
        }

        jsonData = JSON.parse(data.toString());
        // console.log(jsonData)
        res.send(jsonData);
    })
    
    ls.stderr.on('data', (data) => {
    console.log(`stderr: ${data}`);
    });
    
    ls.on('close', (code) => {
    console.log(`child process exited with code ${code}`);
    });
}

controller.getByRegex = (req, res) => {
    const {regex} = req.params;
    ls = spawn('python3', ['python/autos.py', '-b', regex, 'true']); 

    ls.stdout.on('data', data => {
        data = data.toString();

        if (data[0] === '0') {
            res.send('El patrón ingresado no coincide con ningún cliente')
        }

        jsonData = JSON.parse(data.toString())
        res.send(jsonData);
    })
    
    ls.stderr.on('data', (data) => {
    console.log(`stderr: ${data}`);
    });
    
    ls.on('close', (code) => {
    console.log(`child process exited with code ${code}`);
    });
}

controller.newRecord = (req, res) => {

    // !!!! COMPLETAR !!!! //

    const {cliente, auto, trabajo, km, fecha, patente} = req.body;

    console.log("KILOMETRAJE JS" ,req.body)

    ls = spawn('python3', ['python/autos.py', '-n', cliente, auto, trabajo, km, fecha, patente,'true']); 

    ls.stdout.on('data', data => {
        data = data.toString();

        if (data[0] === '0') {
            res.sendStatus(200)
        } else {
            res.sendStatus(400)  
        }

    })
    
    ls.stderr.on('data', (data) => {
    console.log(`stderr: ${data}`);
    });
    
    ls.on('close', (code) => {
    console.log(`child process exited with code ${code}`);
    });
}

module.exports = controller