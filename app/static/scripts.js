/**
 * Created by Lesko on 7.2.2015.
 */

function date_time(id) {
    var date = new Date;
    var year = date.getFullYear();
    var month = date.getMonth();
    var months = ['Januar', 'Februar', 'Marec', 'April', 'Maj', 'Junij',
        'Julij', 'August', 'September', 'Oktober', 'November', 'December'];
    var d = date.getDate();
    var day = date.getDay();
    var days = ['nedelja', 'ponedeljek', 'torek', 'sreda', 'cetrtek', 'petek', 'sobota'];
    var h = date.getHours();
    if (h < 10) {
        h = "0" + h;
    }
    var m = date.getMinutes();
    if (m < 10) {
        m = "0" + m;
    }
    var s = date.getSeconds();
    if (s < 10) {
        s = "0" + s;
    }
    document.getElementById(id).innerHTML = '' + days[day] + ' ' + d + ' ' + months[month] + ' ' + year + ' ' + h + ':' + m + ':' + s;
    setTimeout('date_time("' + id + '");', 1000);
    return true;
}