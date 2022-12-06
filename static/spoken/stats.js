const COLOR_CODES = ['rgb(54, 162, 235)','rgb(255, 99, 132)','#9A1663','#E0144C','#DC5F00','#829460','#256D85','#628E90']
const DATA_NOT_AVAILABLE = 'Unknown'

function populate_data(label,val,graph_label=''){
  // alert('abc');
  data_val = []
  labels = []

  for (const x of val) { 
    if(x[label]==''){
      str1 = `${DATA_NOT_AVAILABLE} (${x['count']})`;
      labels.push(str1);
    }else{
      str1 = `${x[label]} (${x['count']})`;
      labels.push(str1);
    }
    data_val.push(x['count']);
  }
  const data = {
    labels: labels,
    datasets: [{
      data: data_val,
      backgroundColor: COLOR_CODES.slice(0,labels.length),
      hoverOffset: 4,
      label:graph_label
    }]
  };
  return data
}

function add_chart(id,config){
  const myChart = new Chart(document.getElementById(id),config);
}
// doughnut charts start
function gender_stats(val){
  const data = populate_data('gender',val);
  const config = {
    type: 'doughnut',
    data: data,
    options: {
      plugins: {
        title: {
          display: true,
          text: 'Gender based student distribution',
          font: {
            size: 16,
            family:'sans-serif'
        },
        },
        legend:{
          display: true,
          position:'right',
        }
      }
    }
  };
  add_chart('student_gender',config);
  
}

function student_category(val){
  const data = populate_data('category',val);
  const config = {
    type: 'doughnut',
    data: data,
    options: {
      plugins: {
        title: {
          display: true,
          text: 'Category based student distribution',
          font: {
            size: 16,
            family:'sans-serif'
        },
        },
        legend:{
          position:'right',
          align:'right'
        }
      }
    }
  };

  add_chart('student_category',config);
}

function student_occupation(val){
  const data = populate_data('occupation',val);
  const config = {
    type: 'doughnut',
    data: data,
    options: {
      plugins: {
        title: {
          display: true,
          text: 'Occupation based student distribution',
          font: {
            size: 16,
            family:'sans-serif'
        },
        },
        legend:{
          position:'right'
        }
      }
    }
  };
  add_chart('student_occupation',config);
  
}
// doughnut charts end

function course_stats(val){
  const data = populate_data('cert_category__code',val,'Student-Certificate Course Distribution');
  const config = {
    type: 'bar',
    data,
    // options: {
    //   // indexAxis: 'y',
    // }
};
add_chart('student_course',config);
}

function foss_stats(val,id,graph_title){
  data_val = []
  labels = [];
  console.log(val)
  for (const x of val) { 
    // labels.push(x['csc_foss__foss']);
    if(x['csc_foss__foss']==''){
      str1 = `${DATA_NOT_AVAILABLE} (${x['count']})`;
      labels.push(str1);
    }else{
      str1 = `${x['csc_foss__foss']} (${x['count']})`;
      labels.push(str1);
    }
    data_val.push(x['count']);
  }
const data = {
  labels: labels,
  datasets: [{
    axis: 'y',
    label: graph_title,
    data: data_val,
    fill: false,
    backgroundColor: [
      'rgba(255, 99, 132, 0.2)',
      'rgba(255, 159, 64, 0.2)',
      'rgba(255, 205, 86, 0.2)',
      'rgba(75, 192, 192, 0.2)',
      'rgba(54, 162, 235, 0.2)',
      'rgba(153, 102, 255, 0.2)',
      'rgba(201, 203, 207, 0.2)'
    ],
    borderColor: [
      'rgb(255, 99, 132)',
      'rgb(255, 159, 64)',
      'rgb(255, 205, 86)',
      'rgb(75, 192, 192)',
      'rgb(54, 162, 235)',
      'rgb(153, 102, 255)',
      'rgb(201, 203, 207)'
    ],
    borderWidth: 1
  }],
    options: {
      scales: {
        y: {
          max : 100,
        }
      }
    }
};

const config = {
  type: 'bar',
  data,
  options: {
    // indexAxis: 'y',
    scales: {
      y: {
        // max : 2000,
      }
    }
  }
};

const myChart = new Chart(
  document.getElementById(id),
  config
);

}

function csc_states(val){
  console.log(val)
  data_val = []
  labels = [];

  for (const x of val) { 
    // console.log(x); 
    
    if(x['state']==''){
      str1 = `${DATA_NOT_AVAILABLE} (${x['count']})`;
      labels.push(str1);
    }else{
      str1 = `${x['state']} (${x['count']})`;
      labels.push(str1);
    }
    data_val.push(x['count']);
  }
const data = {
  labels: labels,
  datasets: [{
    axis: 'y',
    label: 'CSC - State Distribution',
    data: data_val,
    fill: false,
    backgroundColor: [
      'rgba(255, 99, 132, 0.2)',
      'rgba(255, 159, 64, 0.2)',
      'rgba(255, 205, 86, 0.2)',
      'rgba(75, 192, 192, 0.2)',
      'rgba(54, 162, 235, 0.2)',
      'rgba(153, 102, 255, 0.2)',
      'rgba(201, 203, 207, 0.2)'
    ],
    borderColor: [
      'rgb(255, 99, 132)',
      'rgb(255, 159, 64)',
      'rgb(255, 205, 86)',
      'rgb(75, 192, 192)',
      'rgb(54, 162, 235)',
      'rgb(153, 102, 255)',
      'rgb(201, 203, 207)'
    ],
    borderWidth: 1
  }]
};

const config = {
  type: 'bar',
  data,
  options: {
    // indexAxis: 'y',
  }
};

const myChart = new Chart(
  document.getElementById('csc_state'),
  config
);

}







function student_indi_foss(val){
  data_val = []
  labels = [];

  for (const x of val) { 
    // console.log(x); 
    labels.push(x['csc_foss__foss']);
    data_val.push(x['count']);
  }
const data = {
  labels: labels,
  datasets: [{
    axis: 'y',
    label: 'Student-FOSS Distribution (Individual FOSS only)',
    data: data_val,
    fill: false,
    backgroundColor: [
      'rgba(255, 99, 132, 0.2)',
      'rgba(255, 159, 64, 0.2)',
      'rgba(255, 205, 86, 0.2)',
      'rgba(75, 192, 192, 0.2)',
      'rgba(54, 162, 235, 0.2)',
      'rgba(153, 102, 255, 0.2)',
      'rgba(201, 203, 207, 0.2)'
    ],
    borderColor: [
      'rgb(255, 99, 132)',
      'rgb(255, 159, 64)',
      'rgb(255, 205, 86)',
      'rgb(75, 192, 192)',
      'rgb(54, 162, 235)',
      'rgb(153, 102, 255)',
      'rgb(201, 203, 207)'
    ],
    borderWidth: 1
  }]
};

const config = {
  type: 'bar',
  data,
  options: {
    // indexAxis: 'y',
  }
};

const myChart = new Chart(
  document.getElementById('student_indi_foss'),
  config
);

}

function ajax_call(){

  url = '/csc/stats/ajax_stats/'
  $.ajax({
    url : url,
    type: "GET",
    // data : data,
    success: function(data, textStatus, jqXHR)
    {
      
        // console.log(data);
        // console.log(data['student_gender']);
        gender_stats(data['student_gender']);
        student_category(data['student_category']);
        student_occupation(data['student_occupation']);
        
        course_stats(data['student_course']);

        // foss_stats(data['student_foss_1'],'student_foss_1','Student-FOSS Distribution (Top 20% popular FOSS)');
        // foss_stats(data['student_foss_2'],'student_foss_2','Student-FOSS Distribution (20% - 40% in popularity)');
        // foss_stats(data['student_foss_3'],'student_foss_3','Student-FOSS Distribution (40% - 60% in popularity)');
        // foss_stats(data['student_foss_4'],'student_foss_4','Student-FOSS Distribution (60% - 80% in popularity)');
        // foss_stats(data['student_foss_5'],'student_foss_5','Least popular FOSS (Bottom 20%)');

        foss_stats(data['student_indi_foss'],'student_indi_foss','Student-Individual FOSS Distribution (Top 20% popular FOSS)');
        foss_stats(data['student_indi_foss_1'],'student_indi_foss_1','Student-Individual FOSS Distribution (Top 20% popular FOSS)');
        foss_stats(data['student_indi_foss_2'],'student_indi_foss_2','Student-Individual FOSS Distribution (20% - 40% in popularity)');
        foss_stats(data['student_indi_foss_3'],'student_indi_foss_3','Student-Individual FOSS Distribution (40% - 60% in popularity)');
        foss_stats(data['student_indi_foss_4'],'student_indi_foss_4','Student-Individual FOSS Distribution (60% - 80% in popularity)');
        foss_stats(data['student_indi_foss_5'],'student_indi_foss_5','Least popular Individual FOSS (Bottom 20%)');

        csc_states(data['csc_state']);
        
        
        student_indi_foss(data['student_indi_foss']);

        

        
        
    },
    error: function (jqXHR, textStatus, errorThrown)
    {
        alert('error')
    }
});

}

$( document ).ready(function() {
  
  ajax_call();
  
  // gender_stats();
});



function getColor(d) {
  return d > 1000 ? '#800026' :
         d > 500  ? '#BD0026' :
         d > 200  ? '#E31A1C' :
         d > 100  ? '#FC4E2A' :
         d > 50   ? '#FD8D3C' :
         d > 20   ? '#FEB24C' :
         d > 10   ? '#FED976' :
                    '#FFEDA0';
}
function style(feature) {
  return {
      // fillColor: getColor(feature.properties.density),
      fillColor: getColor(feature.properties.ID_0),
      weight: 2,
      opacity: 1,
      color: 'white',
      dashArray: '3',
      fillOpacity: 0.7
  };
}


function zoomToFeature(e) {
  map.fitBounds(e.target.getBounds());
}

function onEachFeature(feature, layer) {
  layer.on({
      mouseover: highlightFeature,
      mouseout: resetHighlight,
      click: zoomToFeature
  });
}




var map = L.map('map').setView([20.5937, 78.9629], 4);



geojson = L.geoJson(statesData, {
  style: style,
  onEachFeature: onEachFeature
}).addTo(map);

//For our control
var info = L.control();

info.onAdd = function (map) {
    this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
    this.update();
    return this._div;
};

// method that we will use to update the control based on feature properties passed
info.update = function (props) {
    this._div.innerHTML = '<h4>CSC Density</h4>' +  (props ?
        '<b>' + props.name + '</b><br />' + props.IT_0 + ' people / mi<sup>2</sup>'
        : 'Hover over a state');
};

info.addTo(map);

//Legends
var legend = L.control({position: 'bottomright'});

legend.onAdd = function (map) {

    var div = L.DomUtil.create('div', 'info legend'),
        grades = [0, 10, 20, 50, 100, 200, 500, 1000],
        labels = [];

    // loop through our density intervals and generate a label with a colored square for each interval
    for (var i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColor(grades[i] + 1) + '"></i> ' +
            grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
    }

    return div;
};

legend.addTo(map);


(function () {
  'use strict'

  // feather.replace({ 'aria-hidden': 'true' })

  // Graphs
  // var ctx = document.getElementById('myChart')
  // eslint-disable-next-line no-unused-vars
  // var   = new Chart(ctx, {
  //   type: 'line',
  //   data: {
  //     labels: [
  //       'Sunday',
  //       'Monday',
  //       'Tuesday',
  //       'Wednesday',
  //       'Thursday',
  //       'Friday',
  //       'Saturday'
  //     ],
  //     datasets: [{
  //       data: [
  //         15339,
  //         21345,
  //         18483,
  //         24003,
  //         23489,
  //         24092,
  //         12034
  //       ],
  //       lineTension: 0,
  //       backgroundColor: 'transparent',
  //       borderColor: '#007bff',
  //       borderWidth: 4,
  //       pointBackgroundColor: '#007bff'
  //     }]
  //   },
  //   options: {
  //     scales: {
  //       yAxes: [{
  //         ticks: {
  //           beginAtZero: false
  //         }
  //       }]
  //     },
  //     legend: {
  //       display: false
  //     }
  //   }
  // })
})()

function get_csc_state_count(){
  url = '/csc/stats/ajax_csc_state_count/'
  $.ajax({
    url : url,
    type: "GET",
    // data : data,
    success: function(data, textStatus, jqXHR)
    {
      // alert('success');
        // console.log(data);
    },
    error: function (jqXHR, textStatus, errorThrown)
    {
        alert('error')
    }
});
}

google.load('visualization', '1', {'packages': ['geochart']});
google.setOnLoadCallback(drawVisualization);

function drawVisualization() {
  // get_csc_state_count();
  
  url = '/csc/stats/ajax_csc_state_count/'
  var data_state = []
  $.ajax({
    url : url,
    type: "GET",
    // data : data,
    success: function(data, textStatus, jqXHR)
    {
      alert('success');
      // console.log(data);
      data_state.push(['State Code', 'State', 'Temperature']);
      
      for (const x of data['csc_state']) { 
        // console.log(x); 
        
        data_state.push([x['code'],x['state'],Number(x['count'])]);
      }

      var data = google.visualization.arrayToDataTable(data_state);
      var opts = {
        region: 'IN',
        domain:'IN',
        displayMode: 'regions',
        colorAxis: {colors: ['#e5ef88', '#d4b114', '#e85a03']},
        resolution: 'provinces',
        /*backgroundColor: '#81d4fa',*/
        /*datalessRegionColor: '#81d4fa',*/
        defaultColor: '#f5f5f5',
        width: 640, 
        height: 480
      };
      var geochart = new google.visualization.GeoChart(
        document.getElementById('visualization'));
    geochart.draw(data, opts);


    },
    error: function (jqXHR, textStatus, errorThrown)
    {
        alert('error')
    }
  });
  


    
    };

    
    function highlightFeature(e) {
      var layer = e.target;
    
      layer.setStyle({
          weight: 5,
          color: '#666',
          dashArray: '',
          fillOpacity: 0.7
      });
    
      if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
          layer.bringToFront();
      }
      info.update(layer.feature.properties);
    }


    function resetHighlight(e) {
      geojson.resetStyle(e.target);
      info.update();
    }
