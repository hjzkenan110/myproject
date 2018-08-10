window.onload=function(){ 
    //假设这里每个五分钟执行一次test函数 
    get_all(); 
    //get_serise();     
} 
function process(data){
    var updatetime = new Array();
    var tpostnum = new Array();
    var myChart = echarts.init(document.getElementById('main'));
    // var timestamp3 = new Date().getTime();
    for ( var i = 1; i < data.length; i++){
        updatetime.push(data[i]["updatetime"]),
        tpostnum.push(Number(data[i]["tpostnum"]));
        // console.log(unum);
        var option = {
            tooltip: {},
            legend: {
                data:['帖子数量']
            },
            xAxis: {
                data: updatetime
            },
            yAxis: {
                boundaryGap: [0, '50%'],
            },
            series: [{
                symbol: 'none',
                stack: 'a',
                areaStyle: {
                    normal: {}
                },
                //smooth:true,
                name: '帖数',
                type: 'line',
                data: tpostnum
            }],
            dataZoom: [
                {   // 这个dataZoom组件，默认控制x轴。
                    type: 'slider', // 这个 dataZoom 组件是 slider 型 dataZoom 组件
                    start: 90,      // 左边在 10% 的位置。
                    end: 100         // 右边在 60% 的位置。
                },
                {   // 这个dataZoom组件，也控制x轴。
                    type: 'inside', // 这个 dataZoom 组件是 inside 型 dataZoom 组件
                    start: 10,      // 左边在 10% 的位置。
                    end: 60         // 右边在 60% 的位置。    
                }    
            ],
        };
    }
    myChart.setOption(option);
    window.onresize = function(){
        myChart.resize();
    }
}
function get_all(){ 
    setTimeout(get_all,1000*60*5);
    $.ajax({
        type: "get",
        url: "/increase-timelion?",
        //data : {"year":year},
        cache : false,	//禁用缓存
        dataType: "json",
        success: function(result) {
            // alert(result.data[0])
            var j = result.data
            process(j)
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            alert("查询失败");
        }
    });

function subForm() {
    $.ajax({
        url: '/tpostnum_rank', //请求的url
        type: 'get', //请求的方式
        cache : false,	//禁用缓存
        dataType: "json",
        error:function (data) {
            alert('请求失败');
        },
        success:function (data) {
            var str1 = "";
            //清空table中的html
            $("#table table-bordered table-hover table-striped").html("");
            $("#table table-bordered table-hover table-striped").append("<thead><tr><th>板块名</th><th>链接</th><th>更新时间</th><th>帖数</th></tr></thead>");
            for(var i = 0;i<data.data.length;i++){
                str1 = "<tr>" + 
                    "<th>"+data.data[i].fname + "</td>" +
                    "<th>"+data.data[i].url + "</td>" +
                    "<th>"+data.data[i].tpostnum + "</td>" +
                    "<th>"+data.data[i].updatetime + "</td>" +
                    "</tr>";
                $("#table table-bordered table-hover table-striped").append(str1);
            }
            $("#table table-bordered table-hover table-striped").append("</th>")
        }
    });
    
} 




// function get_serise(){ 
//     setTimeout(publicBusi,1000*60*3);//这里的1000表示1秒有1000毫秒,1分钟有60秒,5表示总共5分钟 
//     $.ajax({
//         type: "get",
//         url: "/increase_timelion?" + "time=" + checkText,
//         //data : {"year":year},
//         cache : false,	//禁用缓存
//         dataType: "json",
//         success: function(result) {
//             // alert(result.data[0])
//             var j = result.data
//             for ( var i = 1; i < j.length; i++){
//                 updatetime.push(j[i]["updatetime"]),
//                 unum.push(Number(j[i]["unum"]));
//                 // console.log(unum);
//             }
//             var option = {
//                 tooltip: {},
//                 legend: {
//                     data:['帖子数量']
//                 },
//                 xAxis: {
//                     data: updatetime
//                 },
//                 yAxis: {},
//                 series: [{
//                     name: '帖数',
//                     type: 'line',
//                     data: unum
//                 }]
//             };
    
//             // 使用刚指定的配置项和数据显示图表。
//             myChart.setOption(option);
//         },
//         error: function(XMLHttpRequest, textStatus, errorThrown) {
//             alert("查询失败");
//         }
//     });
//     var charts = [];//定义一个全局变量
    
//     charts.push(myChart);//将每个图表的实例存到全局变量中。
    
// } 
    


