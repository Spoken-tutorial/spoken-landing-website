const colorList = ['rgb(216, 133, 163)','rgb(253, 187, 47)','rgb(230, 246, 157)','rgb(170, 222, 167)','rgb(100, 194, 166)','rgb(45, 135, 187)','rgb(155, 191, 224)','rgb(232, 160, 154)','rgb(251, 226, 159)','rgb(198, 214, 143)']

// function draw_course_enroll_stats(courses,type,id){
function draw_course_enroll_stats(courses,type,id){
    let labels = [];
    let data_points = [];
    for (var key in courses){
        console.log(key,courses[key]);
        labels.push(key);
        data_points.push(courses[key]);
    }    
    const data = {
        labels: labels,
        datasets: [{
          axis: 'y',
          label:'',
          backgroundColor: colorList.slice(labels.length),
          borderColor: '#fff',
          data: data_points,
          borderWidth: 1,
        //   fill: false,
        }]
      };
      console.log("data")
      console.log(data.datasets[0])
    var config = {
        type: 'bar',
        data: data, 
        options: {
            indexAxis: 'y',
          }             
    };
    const myChart = new Chart(document.getElementById(id),config);
}


function draw_prg_type_stats(d){
    const labels = [
        'DCA',
        'Individual',
       ];
    data_points = [d['dca'],d['individual']];
    const data = {
        labels: labels,
        datasets: [{
          label: 'Programme Type',
          backgroundColor: ['#ffecb5','#cff4fc'],
          borderColor: '#fff',
          data: data_points,
        }]
      };
    var config = {
        type: 'pie',
        data: data,              
    };
    const myChart = new Chart(document.getElementById('prg_type'),config);
}

function lockScroll() {
    document.body.classList.toggle('lock-scroll');
}
$(document).ready(function(){ 
    url = '/csc/get_stats/'
    var upcoming_tests = {}
    var course_type_offered = {}
    var dca_students = {}
    var individual_students = {}
    $.ajax({
        url : url,
        type: "GET",
        success: function(data, textStatus, jqXHR)
        {       
            upcoming_tests = data['upcoming_tests']
            course_type_offered = data['course_type_offered']
            dca_students = data['dca_students']
            individual_students = data['individual_students']
            for (var key in upcoming_tests){
                
                d = upcoming_tests[key];
                const labels = [
                    'Approved',
                    'Rejected',
                   ];
                data_points = [d['approved'],d['rejected']];
                const data = {
                    labels: labels,
                    datasets: [{
                      label: key,
                      backgroundColor: ['#94D0CC','#EEC4C4'],
                      borderColor: '#fff',
                      data: data_points,
                    }]
                  };
                var config = {
                    type: 'doughnut',
                    data: data,    
                    options: {
                        borderWidth:1,
                        caretPadding: 10,
                        weight:1,
                          legend: {
                            display: false
                          },
                          cutoutPercentage: 80,
                    }            
                };
                const myChart = new Chart(document.getElementById('test_'+String(d['id'])),config);    
            }
            draw_prg_type_stats(data['course_type_offered']);
            draw_course_enroll_stats(dca_students,'dca','dca_course');
            draw_course_enroll_stats(individual_students,'individual','individual_course');            
        },
        error: function (jqXHR, textStatus, errorThrown)
        {
            console.log("ERROR")
        }
    });
});

function toggle_sidebar(){
    $("#sidebar_div").toggle();
    var element = document.getElementById("main_div");
  element.classList.add("col-md-12");
  var element = document.getElementById("wrapper");
  element.classList.add("container");
  
}