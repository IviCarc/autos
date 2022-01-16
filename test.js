const spawn = require('child_process').spawn;

const ls = spawn('python3', ['test.py'])

ls.stdout.on('data', data => {
    jsonData = JSON.parse((data.toString()))
    console.log(jsonData)
})
