var updatetime = new Array();
var unum = new Array();
var myChart = echarts.init(document.getElementById('main'));

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
            tooltip: {},
            legend: {
                data:['帖子数量']
            },
            xAxis: {
                data: updatetime
            },
            yAxis: {},
            series: [{
                name: '帖数',
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
var charts = [];//定义一个全局变量

charts.push(myChart);//将每个图表的实例存到全局变量中。

window.onresize = function(){//在所有图表之后
    for(var i = 0; i < charts.length; i++){
        charts[i].resize();
    }
};
