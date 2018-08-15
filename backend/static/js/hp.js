window.onload=function(){ 
    //假设这里每个五分钟执行一次test函数 
    get_all(); 
    get_rank();
    get_pie();
    get_hour();
    get_serise();     
} 

function process_line(data){
    var updatetime = new Array();
    var tpostnum = new Array();
    var myChart = echarts.init(document.getElementById('main'));
    // var timestamp3 = new Date().getTime();
    for ( var i = 1; i < data.length; i++){
        updatetime.push(data[i]["updatetime"]),
        tpostnum.push(Number(data[i]["tpostnum"]));}
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
    
    myChart.setOption(option);
    window.onresize = myChart.resize;
}

// 渲染饼图
function process_pie(fname, tpostnum){
    var myChart = echarts.init(document.getElementById('pie'));
    pie_data = new Array()
    for(var i = 0; i < tpostnum.length;i++){
        pie_data.push({value:tpostnum[i], name:fname[i]})
    }

    var option = {
        title : {
            //text: '某站点用户访问来源',
            //subtext: '纯属虚构',
            x:'center'
        },
        tooltip : {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
            orient : 'vertical',
            x : 'left',
            data:fname
        },
        toolbox: {
            show : true,
            feature : {
                mark : {show: true},
                // dataView : {show: true, readOnly: true},
                magicType : {
                    show: true, 
                    type: ['pie'],
                    option: {
                        funnel: {
                            x: '100%',
                            width: '50%',
                            funnelAlign: 'left',
                            max: 1548
                        }
                    }
                },
                // restore : {show: true},
                // saveAsImage : {show: true}
            }
        },
        calculable : true,
        series : [
            {
                name:'访问来源',
                type:'pie',
                radius: '55%',
                center: ['50%', '60%'],
                data: pie_data
            }
        ]
    };
    
    myChart.setOption(option);
    window.onresize = myChart.resize;
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
            process_line(j)
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            alert("查询失败");
        }
    });
}

function get_rank() {
    $.ajax({
        url: '/tpostnum-rank?type=top8', //请求的url
        type: 'get', //请求的方式
        cache : false,	//禁用缓存
        dataType: "json",
        error:function (data) {
            alert('请求失败');
        },
        success:function (data) {
            var str1 = "";
            //清空table中的html
            $("#fuck").html("");
            $("#fuck").append("<thead><tr><th>板块名</th><th>链接</th><th>帖数</th></tr></thead><tbody>");
            for(var i = 0;i<data.data.length;i++){
                str1 = "<tr>" + 
                    "<th>"+data.data[i].fname + "</td>" +
                    "<th>"+data.data[i].url + "</td>" +
                    "<th>"+data.data[i].tpostnum + "</td>" +
                    //"<th>"+data.data[i].updatetime + "</td>" +
                    "</tr>";
                $("#fuck").append(str1);
            }
            $("#fuck").append("</tbody></th>")
        }
    });
} 

function get_pie(){
    var fname = new Array();
    var tpostnum = new Array();
    setTimeout(get_all,1000*60*5);
    $.ajax({
        url: '/tpostnum-rank?type=others', //请求的url
        type: 'get', //请求的方式
        cache : false,	//禁用缓存
        dataType: "json",
        error:function (data) {
            alert('请求失败');
        },
        success:function (data) {
            for(var i = 0;i<data.data.length;i++){
                fname.push(data.data[i].fname)
                tpostnum.push(Number(data.data[i].tpostnum));
            }
            process_pie(fname, tpostnum);
        }
    });

}

function process_hour(updatetime, unum){
    var myChart = echarts.init(document.getElementById('hour'));
    option = {
        title : {
            text: '装备区每小时更新量'
        },
        tooltip : {
            trigger: 'axis'
        },
        legend: {
            data:['帖量']
        },
        toolbox: {
            show : true,
            feature : {
                mark : {show: true},
                dataView : {show: true, readOnly: false},
                magicType : {show: true, type: ['line', 'bar']},
                restore : {show: true},
                saveAsImage : {show: true}
            }
        },
        calculable : true,
        xAxis : [
            {
                type : 'category',
                data : updatetime
            }
        ],
        yAxis : [
            {
                type : 'value'
            }
        ],
        series : [
            {
                name:'帖量',
                type:'bar',
                data:unum,
            }
        ]
    };
    myChart.setOption(option);
}

function get_hour(){
    var updatetime = new Array();
    var unum = new Array();
    setTimeout(get_all,1000*60*5);
    $.ajax({
        url: '/series-timelion', //请求的url
        type: 'get', //请求的方式
        cache : false,	//禁用缓存
        dataType: "json",
        error:function (data) {
            alert('请求失败');
        },
        success:function (data) {
            for(var i = 0;i<data.data.length;i++){
                updatetime.push(data.data[i].updatetime)
                unum.push(Number(data.data[i].unum));
            }
            process_hour(updatetime, unum);
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
    


