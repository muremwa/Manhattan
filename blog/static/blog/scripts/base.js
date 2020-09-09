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


[...document.getElementsByTagName('input')].filter((element) => element.type === 'password').forEach((password) => password.classList.add('form-control'));
