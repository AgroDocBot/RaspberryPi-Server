// all of the methods here are deprecated
// the control and movement functions have been transfered to the ESP32-C3
// (see the ESP32-C3 Firmware repository)

const express = require('express');
const { exec } = require('child_process');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const Gpio = require('onoff').Gpio;

const app = express();
app.use(cors());
const port = 3000;

const servoForward = new Gpio(17, 'out');
const servoBackward = new Gpio(18, 'out');

console.warn("Movement control through the Raspberry Pi is deprecated.");

app.get('/control/:direction', (req, res) => {
  const direction = req.params.direction;

  switch (direction) {
    case 'forward':
      servoForward.writeSync(1); 
      break;
    case 'backward':
      servoBackward.writeSync(1); 
      break;
  }

  setTimeout(() => {
    servoForward.writeSync(0);
    servoBackward.writeSync(0);

  }, 1000);

  res.send({ status: 'Moving', direction });
});

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
