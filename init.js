const fs = require('fs');
const WebSocket = require('ws');
const { exec } = require('child_process');
const path = require('path');
const gpsd = require('node-gpsd');
const https = require('https');

const port = 3003;
let wsESP32;  
let wsClient;  

let autoProcess = false;

const gpsClient = new gpsd.Listener({
	hostname: 'localhost',
	port: 2947,
	logger: {
		log: function (msg) { console.log(msg); },
		error : function (msg) { console.error(msg); }
	}
});

gpsClient.connect(() => {
	gpsClient.watch();
})

const wss = new WebSocket.Server({ port });

wss.on('connection', (ws, req) => {
    ws.on('message', (message) => {
        let parsedMessage = JSON.parse(message);

        switch(parsedMessage.action) {
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
		break;
            case 'turn_right':
                exec('python3 camera/movement/turning.py 2', (error, stdout, stderr) => {
                    if (error) {
                        console.error(`Error: ${error.message}`);
                        ws.send(JSON.stringify({ status: 'error', message: error.message }));
                    } else {
                        let output = stderr + stdout;
                        console.log(`Result: ${stdout}`);
                        ws.send(JSON.stringify({ status: 'success', output: output }));
                    }
                })
		break;
            case 'turn_left':
                exec('python3 camera/movement/turning.py -2', (error, stdout, stderr) => {
                    if (error) {
                        console.error(`Error: ${error.message}`);
                        ws.send(JSON.stringify({ status: 'error', message: error.message }));
                    } else {
                        let output = stderr + stdout;
                        console.log(`Result: ${stdout}`);
                        ws.send(JSON.stringify({ status: 'success', output: output }));
                    }
                })
		break;
            case 'stop_rotate':
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
		break;
            case 'level_higher':
                exec('python3 camera/movement/elevating.py 7.2 1', (error, stdout, stderr) => {
                    if (error) {
                        console.error(`Error: ${error.message}`);
                        ws.send(JSON.stringify({ status: 'error', message: error.message }));
                    } else {
                        let output = stderr + stdout;
                        console.log(`Result: ${stdout}`);
                        ws.send(JSON.stringify({ status: 'success', output: output }));
                    }
                })
		break;
            case 'level_lower':
                exec('python3 camera/movement/elevating.py 7.8 1', (error, stdout, stderr) => {
                    if (error) {
                        console.error(`Error: ${error.message}`);
                        ws.send(JSON.stringify({ status: 'error', message: error.message }));
                    } else {
                        let output = stderr + stdout;
                        console.log(`Result: ${stdout}`);
                        ws.send(JSON.stringify({ status: 'success', output: output }));
                    }
                })
		break;
            case 'stop_elevate':
                //fs.writeFileSync('stop_signal.txt', '1');
                exec('python3 camera/movement/elevating.py 7.5 1', (error, stdout, stderr) => {
                    if (error) {
                        console.error(`Error: ${error.message}`);
                        ws.send(JSON.stringify({ status: 'error', message: error.message }));
                    } else {
                        let output = stderr + stdout;
                        console.log(`Result: ${stdout}`);
                        ws.send(JSON.stringify({ status: 'success', output: output }));
                    }
                })
		break;
	    case 'gps':
                exec('gpspipe -w -n 10', (error, stdout, stderr) => {
                    if (error) {
                        console.error(`Error: ${error.message}`);
                        ws.send(JSON.stringify({ status: 'error', message: error.message }));
                    } else {

			console.log(stdout);
			let iLat = stdout.indexOf('lat')+5;
			let iLon = stdout.indexOf('lon')+5;
			let iAlt = stdout.indexOf('alt')+8;

                            ws.send(JSON.stringify({
                                status: 'success',
                                latitude: stdout.substr(iLat, 12),
                                longitude: stdout.substr(iLon, 12),
                                altitude: stdout.substr(iAlt, 8) 
                            }));

                    }
                });
                break;
            default:
                ws.send(JSON.stringify({ status: 'error', message: 'Invalid command' }));
        }
    });
});
