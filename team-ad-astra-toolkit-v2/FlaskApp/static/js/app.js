$(document).ready(function () {
  const ctx1 = document.getElementById("potChart").getContext("2d");

  const potChart = new Chart(ctx1, {
    type: "line",
    data: {
      datasets: [{ label: "Potentiometer", borderColor: "rgba(39,43,245,0.8)",} ,],
    },
  });

  const ctx2 = document.getElementById("photChart").getContext("2d");
  
  const photChart = new Chart(ctx2, {
    type: "line",
    data: {
      datasets: [{ label: "Photoresistor", borderColor: "rgba(39,43,245,0.8)",} ,],
    },
  });
  
  function addDataPot(label, data) {
    potChart.data.labels.push(label);
    potChart.data.datasets[0].data.push(data);
    potChart.update();  
  }

  function addDataPhot(label, data) {
    photChart.data.labels.push(label);
    photChart.data.datasets[0].data.push(data);
    photChart.update();
  }
  
  function removeFirstDataPot() {
    potChart.data.lables.splice(0,1);
    potChart.data.datasets[0].data.shift();
  }

  function removeFirstDataPhot() {
    photChart.data.lables.splice(0,1);
    photChart.data.datasets[0].data.shift();
  }

  //connect to the socket server.
  //var socket = io.connect("http://" + document.domain + ":" + location.port);
  var socket = io.connect();

  //receive details from server
  socket.on("updateSensorData1", function (msg1) {
    console.log("Received sensorData :: " + msg1.date + " :: " + msg1.value1);

      // Show only MAX_DATA_COUNT data
    if (potChart.data.labels.length > MAX_DATA_COUNT) {
      removeFirstDataPot();
    }
    addDataPot(msg1.date, msg1.value1);

  });

  socket.on("updateSensorData2", function (msg2) {
    console.log("Received sensorData :: " + msg2.date + " :: " + msg2.value2);

      // Show only MAX_DATA_COUNT data
    if (photChart.data.labels.length > MAX_DATA_COUNT) {
      removeFirstDataPhot();
    }
    addDataPhot(msg2.date, msg2.value1);

  });





});