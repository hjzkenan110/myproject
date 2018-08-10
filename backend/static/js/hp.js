var checkText=$(".s1").find("option:selected").text();

window.onload=function(){ 
    //假设这里每个五分钟执行一次test函数 
    get_all(); 
    get_serise(); 
} 

function get_all(){ 
    var updatetime = new Array();
    var unum = new Array();
    var myChart = echarts.init(document.getElementById('main'));
    var timestamp3 = new Date().getTime();
    setTimeout(get_all,1000*60*5);
    $.ajax({
        type: "get",
        url: "/increase_timelion?" + "time=" + checkText,
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
    } 

function get_serise(){ 
setTimeout(publicBusi,1000*60*5);//这里的1000表示1秒有1000毫秒,1分钟有60秒,5表示总共5分钟 
$.post('${basePath}/approval/toCheckPersonBusi',function(data){ 
if(data.result !=0){ 
............ 
} 
}); 
} 
    

$.ajax({
    type: "get",
    url: "/increase_timelion?" + "time=" + checkText,
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





//在所有图表之后,自适应bootstrapt
window.onresize = function(){
    for(var i = 0; i < charts.length; i++){
        charts[i].resize();
    }
};
