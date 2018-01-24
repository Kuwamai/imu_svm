var ros = new ROSLIB.Ros({ url : 'ws://' + location.hostname + ':9000' });

ros.on('connection', function() {console.log('websocket: connected');});
ros.on('error', function(error) {console.log('websocket error: ', error); });
ros.on('close', function() {console.log('websocket: closed');});

var data = [{
	y: [],
	type: 'lines',
	line: {color: '#80CAF6'},
	name: 'forward'
},{
	y: [],
	type: 'lines',
	line: {color: '#DF56F1'},
	name: 'crash'
},{
	y: [],
	type: 'lines',
	line: {color: '#ff0050'},
	name: 'turn_l'
},{
	y: [],
	type: 'lines',
	line: {color: '#00ff19'},
	name: 'turn_r'
},{
	y: [],
	type: 'lines',
	line: {color: '#ffaa00'},
	name: 'stop'
}];

var options = {
	title: 'State probability'
};

Plotly.newPlot('graph', data, options);

var ls = new ROSLIB.Topic({
	ros : ros,
	name : '/state_proba',
	messageType : 'imu_svm/state_proba'
});

var array = [];
array[0] = [];
array[1] = [];
array[2] = [];
array[3] = [];
array[4] = [];

ls.subscribe(function(message) {
	var arr = [message.forward, message.crash, message.turn_l, message.turn_r, message.stop];

	str = JSON.stringify(arr.indexOf(Math.max.apply(null,arr) ));
	document.getElementById("state_proba").innerHTML = str;
	console.log(Math.max(message.forward, message.crash, message.turn_l, message.turn_r, message.stop));

	array[0].push(message.forward);
	array[1].push(message.crash);
	array[2].push(message.turn_l);
	array[3].push(message.turn_r);
	array[4].push(message.stop);
});

var interval = setInterval(function() {
	Plotly.extendTraces('graph', {
		y: [array[0], array[1], array[2], array[3], array[4]]
		}, [0,1,2,3,4])
	array[0] = [];
	array[1] = [];
	array[2] = [];
	array[3] = [];
	array[4] = [];
}, 100);
