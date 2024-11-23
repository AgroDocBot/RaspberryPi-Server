const fs = require('fs');
const WebSocket = require('ws');
const { exec } = require('child_process');
const path = require('path');

const port = 3003;
let wsESP32;  
let wsClient;  

let autoProcess = false;

const wss = new WebSocket.Server({ port });

wss.on('connection', (ws, req) => {
    ws.on('message', (message) => {
        let parsedMessage = JSON.parse(message);

        switch(parsedMessage.command) {
            case 'connect-esp32':
                wsESP32 = ws;
                console.log('ESP32 connected via WebSocket.');
                break;
            case 'connect-client':
                wsClient = ws;
                console.log('Client connected via WebSocket.');
                break;
            case 'shoot_assess':
                exec('python3 camera/shoot_assess.py', (error, stdout, stderr) => {
                    if (error) {
                        console.error(`Error: ${error.message}`);
                        ws.send(JSON.stringify({ status: 'error', message: error.message }));
                    } else {
                        let output = stderr + stdout;
                        console.log(`Result: ${stdout}`);
                        ws.send(JSON.stringify({ status: 'success', output: output }));
                    }
                });
                break;
            case 'shoot_show':
                // read and send testimg.jpg as binary
                let imgPath = path.join(__dirname, 'testimg.jpg');
                fs.readFile(imgPath, (err, data) => {
                    if (err) {
                        ws.send(JSON.stringify({ status: 'error', message: 'Error reading image' }));
                    } else {
                        ws.send(data);  // send binary image data
                    }
                });
                break;
            case 'auto_on':
                console.log('Auto mode activated');
                if (!autoProcess) {
                    autoProcess = exec('node auto_mode.js');
                    autoProcess.stdout.on('data', (data) => console.log(data));
                    autoProcess.stderr.on('data', (err) => console.error(err));
                    autoProcess = true;
                }
                break;
            case 'auto_off':
                console.log('Auto mode deactivated');
                if (autoProcess) {
                    autoProcess.kill();
                    autoProcess = false;
                }
            case 'turn_right':
                exec('python3 camera/movement/turning.py 1', (error, stdout, stderr) => {
                    if (error) {
                        console.error(`Error: ${error.message}`);
                        ws.send(JSON.stringify({ status: 'error', message: error.message }));
                    } else {
                        let output = stderr + stdout;
                        console.log(`Result: ${stdout}`);
                        ws.send(JSON.stringify({ status: 'success', output: output }));
                    }
                })
            case 'turn_left':
                exec('python3 camera/movement/turning.py -1', (error, stdout, stderr) => {
                    if (error) {
                        console.error(`Error: ${error.message}`);
                        ws.send(JSON.stringify({ status: 'error', message: error.message }));
                    } else {
                        let output = stderr + stdout;
                        console.log(`Result: ${stdout}`);
                        ws.send(JSON.stringify({ status: 'success', output: output }));
                    }
                })
            case 'stop':
                fs.writeFileSync('stop_signal.txt', '1');
                exec('python3 camera/movement/turning.py 0', (error, stdout, stderr) => {
                    if (error) {
                        console.error(`Error: ${error.message}`);
                        ws.send(JSON.stringify({ status: 'error', message: error.message }));
                    } else {
                        let output = stderr + stdout;
                        console.log(`Result: ${stdout}`);
                        ws.send(JSON.stringify({ status: 'success', output: output }));
                    }
                })
            default:
                ws.send(JSON.stringify({ status: 'error', message: 'Invalid command' }));
        }
    });
});

console.log(`WebSocket server running on ws://0.0.0.0:${port}`);
