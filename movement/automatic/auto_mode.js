const WebSocket = require('ws');
const { execSync } = require('child_process');

const ESP32_WS_URL = 'ws://192.168.4.18:81/ws';
const ws = new WebSocket(ESP32_WS_URL);

const measureDistance = () => {
  const distances = execSync('python3 movement/automatic/measure.py').toString().trim();
  const [leftDistance, rightDistance] = distances.split(',').map(Number);
  return { leftDistance, rightDistance };
};

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

ws.on('open', () => {
  console.log('Connected to ESP32-C3');
  
  const autoMoveInterval = setInterval(async () => {
    const measuredDistances = measureDistance();

    if (measuredDistances.leftDistance < 50 || measuredDistances.rightDistance < 50) {
      console.log('Obstacle detected, sending turn_right command');
      ws.send(JSON.stringify({ action: 'turn_right' }));
    } else {
      console.log('No obstacles, sending move_forward command');
      ws.send(JSON.stringify({ action: 'move_forward' }));
      await sleep(250);
      ws.send(JSON.stringify({ action: 'stop'}));
      await sleep(250);
    }
  }, 1000);  

  ws.on('close', () => {
    clearInterval(autoMoveInterval);
    console.log('ESP32 connection closed, stopping auto movement');
  });
});

ws.on('error', (err) => {
  console.error('WebSocket error:', err);
});
