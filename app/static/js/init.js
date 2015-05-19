$(document).ready(function() {

     $.getJSON("/api/get", function (result) {

         var labels = [],data=[];
         for(var item in result.json_list){
              labels.push(result.json_list[item].modified_at);
              data.push(result.json_list[item].rand);
          }

    var tempData = {
        labels : labels,
        datasets : [{
            fillColor : "rgba(172,194,132,0.4)",
            strokeColor : "#ACC26D",
            pointColor : "#fff",
            pointStrokeColor : "#9DB86D",
            data : data
        }]
    };
    Chart.defaults.global.responsive = true;
    var temp = document.getElementById('myChart').getContext('2d');
    var lineChart = new Chart(temp).Line(tempData);

     });
 });