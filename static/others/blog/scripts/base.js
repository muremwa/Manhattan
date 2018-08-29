$("#blogs").tooltip();

$(window).scroll(function(){
    if($(this).scrollTop()){
        $("#navbar").addClass("shadow");
    }else{
        $("#navbar").removeClass("shadow");
    }
});
 
// current year at the bottom of the page
var today = new Date();
var year = today.getFullYear();
document.getElementById("this-year").innerHTML = year;


function howLongAgo(){
    var dates = document.getElementsByClassName("dated");
    var months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];    var postYear;
    var month = today.getUTCMonth();
    var postMonth;
    var cDate = today.getDate();
    var postDate;
    var hour = today.getHours();
    var postHour;
    var min = today.getMinutes();
    var postMin;
    var responses = {'now':'just now',  'mins':' minutes ago', 'hr':'an hour ago', 'hrs':' hours ago', 'day':'yesterday', 'days':' days ago', 'mnth':'last month', 'mnths':' months ago', 'yr':'a year ago', 'yrs':' years ago'};
    var reply;
    var period;

    for(date of dates){
        postYear = parseInt(date.innerHTML.split(" ")[2]);
         
        if (postYear < year){
            // years
            period = year - postYear;
            if(period == 1){
                reply = responses.yr;
            }else{
                reply = period + responses.yrs;
            }
        }else if (postYear == year){
            // months
            postMonth = parseInt(months.indexOf(date.innerHTML.split(" ")[0]));
            if (postMonth < month){
                period = month - postMonth;
                if(period == 1){
                    reply = responses.mnth;
                }else{
                    reply = period + responses.mnths;
                }                
            }else if (postMonth == month){
                // days
                postDate = parseInt(date.innerHTML.split(" ")[1]);
                if (postDate < cDate){
                    period = cDate - postDate;
                    if (period == 1){
                        reply = responses.day;
                    }else{
                        reply = period + responses.days;
                    }
                }else if (postDate == cDate){
                    // hours
                    postHour = parseInt(date.innerHTML.split(" ")[3].split(":")[0]);
                    var timeSuffix = dates[1].innerHTML.split(" ")[4];
                    // convert to 24 hours system
                    if (timeSuffix == "p.m."){
                        postHour = postHour + 12;
                    }
                    console.log(postHour + " >> " + hour + " " + timeSuffix);
                    console.log(date.parentElement);
                    if (postHour < hour){
                        period = hour - postHour;
                        if (period == 1){
                            reply = responses.hr;
                        }else {
                            reply = period + responses.hrs;
                        }
                    }else if (postHour == hour){
                        // minutes
                        postMin = parseInt(date.innerHTML.split(" ")[3].split(":")[1]);
                        if (postMin < min){
                            period = min - postMin;
                            if (period < 2 ){
                                reply = responses.now;
                            }else{
                                reply = period + responses.mins;
                            }
                        }
                    }
                }
            }
        }

        date.innerHTML = reply;
    }

}

// howLongAgo();