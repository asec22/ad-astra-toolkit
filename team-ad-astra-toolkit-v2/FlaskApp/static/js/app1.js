$(document).ready(function () {
  const ctx1 = document.getElementById("potChart").getContext("2d");
  
  const data2 = [];

  const potChart = new Chart(ctx1, {
    type: "line",
    data: {
      datasets: [{ label: "Servo Angle", borderColor: "rgba(39,43,245,0.8)",} ,],
    },
  });
  
  function addData(label, data) {
    potChart.data.labels.push(label);
    potChart.data.datasets[0].data.push(data);
    const data1 = {time: label, angle: data};
    data2.push(data1);
    potChart.update();  
  }

  function removeFirstData() {
    potChart.data.labels.splice(0, 1);
    potChart.data.datasets[0].data.shift();
    data2.shift(); // Also remove the first data point from data2
    potChart.update();
  }

  function generateTable(data) {
    const table = document.createElement("table");
    const headerRow = document.createElement("tr");
  
    // Create header cells
    const headerCells = ["Time", "Angle"];
    headerCells.forEach((cell) => {
      const headerCell = document.createElement("th");
      headerCell.textContent = cell;
      headerRow.appendChild(headerCell);
    });
  
    table.appendChild(headerRow);
  
    // Create data rows
    data.forEach((item) => {
      const dataRow = document.createElement("tr");
  
      // Create data cells
      const dataCells = [item.time, item.angle]; // Use item.angle instead of item.level
      dataCells.forEach((cell) => {
        const dataCell = document.createElement("td");
        dataCell.textContent = cell;
        dataRow.appendChild(dataCell);
      });
  
      table.appendChild(dataRow);
    });
  
    return table;
  }

  function clearTable() {
    const tableContainer = document.getElementById("tableServo");
    tableContainer.innerHTML = ""; // Clear existing content
  }

  function createTable(data){
    const table = generateTable(data);
    document.getElementById("tableServo").appendChild(table);
  }  

  const MAX_DATA_COUNT = 10;
  //connect to the socket server.
  //var socket = io.connect("http://" + document.domain + ":" + location.port);
  var socket = io.connect();


  //receive details from server
  socket.on("updateSensorData1", function (msg1) {
    console.log("Received sensorData :: " + msg1.date + " :: " + msg1.value1);

      // Show only MAX_DATA_COUNT data
    if (potChart.data.labels.length > MAX_DATA_COUNT) {
      removeFirstData();
    }
    addData(msg1.date, msg1.value1);
    clearTable();
    createTable(data2); // Update the table with the latest data
  });
});