const https = require('https');
const WebSocket = require('ws');
const fs = require('fs');

process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

const server = https.createServer({
  cert: fs.readFileSync('server.crt'),
  key: fs.readFileSync('server.key'),
});

const wss = new WebSocket.Server({ server });

wss.on('connection', (ws) => {
  ws.on('message', (message) => console.log(`Received: ${message}`));
  ws.send('Connected over WSS');
});

server.listen(4003, () => console.log('Server running on wss://'));
