      // Appel à la route Flask pour récupérer les données
      fetch("/get_data")
          .then(response => response.json())
          .then(data => {
              // Extraction des valeurs du temps, température, humidité et pression
              const xValues = data.temps;
              const yTemperature = data.temperature;
              const yHumidity = data.humidity;
              const yPressure = data.pressure;
  
              // Création du graphique Plotly
              const plotDataTemp = [
                  {
                      x: xValues,
                      y: yTemperature,
                      type: "scatter",
                      mode: "lines",
                      name: "Température",
                      marker: { color: 'red' }
                  }
                ];
                const plotDataHum = [
                      {
                          x: xValues,
                          y: yHumidity,
                          type: "scatter",
                          mode: "lines",
                          name: "Humidité",
                          marker: { color: 'blue' }
                      }
                ];
                const plotDataPress = [
                       {
                            x: xValues,
                            y: yPressure,
                            type: "scatter",
                            mode: "lines",
                            name: "Pression",
                            marker: { color: 'green' }
                        }
                ];
                  
             const plotLayoutTemp = {
                  title: "Graphique Température en fonction du temps",
                  xaxis: { title: "Temps" },
                  yaxis: { title: "°C" }
              };
              const plotLayoutHum = {
                  title: "Graphique Humidité en fonction du temps",
                  xaxis: { title: "Temps" },
                  yaxis: { title: "%" }
              };
              const plotLayoutPress = {
                  title: "Graphique Pression en fonction du temps",
                  xaxis: { title: "Temps" },
                  yaxis: { title: "hPa" }
              };
              Plotly.newPlot("myPlotTemp", plotDataTemp, plotLayoutTemp);
              Plotly.newPlot("myPlotHum", plotDataHum, plotLayoutHum);
              Plotly.newPlot("myPlotPress", plotDataPress, plotLayoutPress);
          })
          .catch(error => console.error('Erreur lors de la récupération des données:', error));


// script pour changer le theme
function toggleIcons() {
    var moonIcon = document.getElementById("moon-icon");
    var sunIcon = document.getElementById("sun-icon");
    var bodyElement = document.body;
    var iconClicked = ""

    if (moonIcon.style.display === "block") {
      moonIcon.style.display = "none";
      sunIcon.style.display = "block";
      bodyElement.style.backgroundImage = "url('static/nightbg.png')";
      iconClicked = "moon";
      
    } else {
        moonIcon.style.display = "block";
        sunIcon.style.display = "none";
        bodyElement.style.backgroundImage = "url('static/lightbg.png')";
        iconClicked = "sun";
    }
    // console.log(iconClicked);
    return iconClicked;
  }
