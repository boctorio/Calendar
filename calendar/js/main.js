
var date = new Date();
var timestamp = Date.parse(date);
var num = '日一二三四五六';
var Month = date.getMonth();
var Day = date.getDate();
var First_day;

var all_contests,daily_contests,contest_num;

$.get('http://boctorio.com:8080/calendar/json/all_contest.json',function(contests){
    all_contests=contests;
    Init_contests();
    Init();
});

function Init_contests(){
    Init_array();
    for(var i=0;i<all_contests.length;i++){
        Insert(all_contests[i],daily_contests,contest_num);
    }
}

function Init_array() {
    daily_contests = new Array(10);
    contest_num = new Array(10);
    for(var i=0;i<10;i++){
        daily_contests[i] =new Array(12);
        contest_num[i] = new Array(12);
        for(var j=0;j<12;j++){
            daily_contests[i][j] = new Array(32);
            contest_num[i][j] = new Array(32);
            for(var k=0;k<32;k++){
                contest_num[i][j][k]=0;
                // console.log(i+' '+j+' '+k);
                daily_contests[i][j][k] = new Array(20);
            }
        }
    }
}

function Init() {//加载日历body部分

    //加载头部信息
    load_head(timestamp);
    //加载比赛信息
    general_calendar(daily_contests,contest_num,First_day);
}

function load_head(cur_time){
    First_day = new Date(cur_time);
    document.getElementById('date').innerHTML=First_day.getFullYear()+'年';

    cur_time-=86400000;
    First_day = cur_time;

    var tr='';
    for(var i=0;i<7;i++){
        var date_details = new Date(cur_time);
        var cur_week = date_details.getDay();
        var month = date_details.getMonth();
        var day = date_details.getDate();
        if(Month === month && Day === day && cur_time-Date.parse(date)<86400000){
            tr+='<th id="today">';
        }
        else{
            tr+='<th>';
        }
        tr+=(month+1)+'月'+day+'日';
        tr+='<br>';
        tr+='星期'+num[cur_week];
        tr+='</th>';
        cur_time+=86400000;
    }
    document.getElementById('week').innerHTML=tr;
}

function next_seven_days(){//后七天
    timestamp+=7*86400000;
    Init();
}

function last_seven_days() {//前七天
    timestamp-=7*86400000;
    Init();
}

function Insert(contest,arr,num){
    var date = new Date(contest.start_time*1000);
    var year = date.getFullYear();
    var month = date.getMonth();
    var day = date.getDate();
    arr[year-2019][month][day][num[year-2019][month][day]]=contest;
    num[year-2019][month][day]++;
}

function general_calendar(arr,contest_num,time) {
    var tbody='';
    var details = '';
    for(var i=0;i<7;i++){
        tbody+='<td><ul class="list-group">';
        var cur_time = new Date(time);
        var year = cur_time.getFullYear()-2019;
        var month = cur_time.getMonth();
        var day = cur_time.getDate();
        for(var j=0;j<contest_num[year][month][day];j++){
            var hash = 'a'+j+'b'+year+'c'+month+'d'+day;
            details+=detail(arr[year][month][day][j],hash);
            tbody+='<li class="list-group-item" data-toggle="modal" data-target="#';
            tbody+=hash;
            tbody+='"><b>';
            tbody+='['+arr[year][month][day][j].platform+']';
            tbody+=arr[year][month][day][j].name;
            tbody+='</b></li>';
        }
        tbody+='</ul></td>';
        time+=86400000;
    }
    document.getElementById('main').innerHTML=tbody;
    document.getElementById('details').innerHTML=details;
}
function detail(contest,hash) {
    // console.log('here');
    var div='';
    div+='<div class="modal fade" id="'+hash+'" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">\n' +
        '                        <div class="modal-dialog">\n' +
        '                            <div class="modal-content">\n' +
        '                                <div class="modal-header">\n' +
        '                                    <h4 class="modal-title" id="myModalLabel">';
    div+=contest.name;
    div+='\n' +
        '                                    </h4>\n' +
        '                                    <button type="button" class="close" data-dismiss="modal"\n' +
        '                                            aria-hidden="true">×\n' +
        '                                    </button>\n' +
        '                                </div>\n' +
        '                                <div class="modal-body">';

    div+='比赛开始时间：'+ standard_time(contest.start_time);
    div+='</div><div class="modal-body">';
    div+='比赛结束时间：' + standard_time(contest.end_time);
    div+='</div><div class="modal-body">';
    div+='比赛时长：' + duration_time(contest.durationSeconds);
    div+='</div><div class="modal-body">';
    div+='比赛平台：'+ contest.platform;
    div+= '                                </div>\n' +
        '                                <div class="modal-footer">\n' +
        '                                    <button type="button" class="btn btn-primary" target="_self" onclick="window.open(\'';
    div+=contest.contest_url;
    div+='\')">\n' +
        '                                        点击前往\n' +
        '                                    </button>\n' +
        '                                </div>\n' +
        '                            </div>\n' +
        '                        </div>\n' +
        '                    </div>';
    // console.log(div);
    return div;
}
function standard_time(contest_time) {
    var date = new Date(contest_time*1000);
    var year = date.getFullYear();
    var month = date.getMonth()+1;
    var day = date.getDate();
    var hour = date.getHours();
    var min = date.getMinutes();
    var time = year + '-' + month + '-' + day +' ' + hour + ':';
    if(min<10) time += '0'+min;
    else time += min;
    return time;
}
function duration_time(contest_time) {
    var hour = Math.floor(contest_time/3600);
    var min = (contest_time%3600)/60;
    var time = hour + ':';
    if(min<10) time += '0'+min;
    else time += min;
    return time;
}