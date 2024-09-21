const express = require('express');
const { exec } = require('child_process');
const cors = require('cors');
const path = require('path');


const app = express();
app.use(cors());

const port = 3000;

app.get('/shoot/assess', (req, res) => {

    exec('python3 shoot_assess.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            return res.status(500).json({ status: 'error', message: error.message });
        }

	let output = stderr + stdout;
	
        console.log(`Result: ${stdout}`);
        res.json({ status: 'success', output: output });
    });
});

app.get('/shoot/show', (req, res) => {

    let imgPath = path.join(__dirname, 'testimg.jpg');
    res.sendFile(imgPath, (err) => {
	if(err) res.status(500).send('Error sending image!');
    });
});

app.listen(port, '0.0.0.0', () => {
    console.log(`Server running on http://0.0.0.0:${port}`);
});

