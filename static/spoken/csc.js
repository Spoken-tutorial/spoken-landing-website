const colorList = ['rgb(216, 133, 163)','rgb(253, 187, 47)','rgb(230, 246, 157)','rgb(170, 222, 167)','rgb(100, 194, 166)','rgb(45, 135, 187)','rgb(155, 191, 224)','rgb(232, 160, 154)','rgb(251, 226, 159)','rgb(198, 214, 143)','rgb(255, 170, 165)','rgb(203, 226, 176)','rgb(220, 214, 247)','rgb(234, 144, 133)','rgb(164, 212, 174)','rgb(213, 151, 206)',
'rgb(72, 76, 127)','rgb(237, 154, 115)','rgb(222, 212, 115)','rgb(120, 176, 160)','rgb(92, 120, 147)','rgb(203, 155, 66)','rgb(215, 172, 212)','rgb(234, 138, 138)','rgb(66, 121, 150)','rgb(135, 142, 205)','rgb(42, 82, 138)','rgb(139, 79, 128)']
console.log('a',colorList.length)
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
  console.log('printing d................')
  console.log(d)
  const labels = [];
  const data_points = []
  for (const course in d) {
    console.log(`${course}: ${d[course]}`);
    labels.push(course);
    data_points.push(d[course]);
  }
  console.log(labels)
    backgroundColors = [];
    for (const i in colorList) {
      backgroundColors.push(colorList[i]);
    }
    const data = {
        labels: labels,
        datasets: [{
          label: 'Programme Type',
          backgroundColor:backgroundColors,
          borderColor: '#fff',
          data: data_points,
        }]
      };
    var config = {
        type: 'bar',
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
    

    course_count_result = {}
    $.ajax({
        url : url,
        type: "GET",
        success: function(data, textStatus, jqXHR)
        {       
            upcoming_tests = data['upcoming_tests']
            course_type_offered = data['course_type_offered']
           
            course_count_result= data['course_count_result']

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
            draw_prg_type_stats(data['course_count_result']);
            // draw_course_enroll_stats(dca_students,'dca','dca_course');
            // draw_course_enroll_stats(individual_students,'individual','individual_course');            
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