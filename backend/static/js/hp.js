var updatetime = new Array();
var unum = new Array();
var myChart = echarts.init(document.getElementById('morris-area-chart'));

$.ajax({
    type: "get",
    url: "/timelion",
    //data : {"year":year},
    cache : false,	//禁用缓存
    dataType: "json",
    success: function(result) {
        // alert(result.data[0])
        var j = result.data
        for ( var i = 1; i < j.length; i++){
            updatetime.push(j[i]["updatetime"]),
            unum.push(Number(j[i]["unum"]));
            // console.log(unum);
        }
        var option = {
            title: {
                text: '虎扑板各块帖量'
            },
            tooltip: {},
            legend: {
                data:['帖子数量']
            },
            xAxis: {
                data: updatetime
            },
            yAxis: {},
            series: [{
                name: '销量',
                type: 'line',
                data: unum
            }]
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
    },
    error: function(XMLHttpRequest, textStatus, errorThrown) {
        alert("查询失败");
    }
});
// window.setInterval(function(){$.ajax()},100000);
