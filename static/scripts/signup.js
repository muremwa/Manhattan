// add bootstrap effects to input areas
inputs = document.getElementsByTagName("input");
acceptable = ['text', 'email', 'password']

for(i in inputs){
    if(acceptable.includes(inputs[i].type)){
        inputs[i].classList.add("form-control");
    }
}


// create a distraction free login page
function signUpAnimation(){
    $(function(){
        $("#jumbo").slideUp(500);
    });
    
    var form = document.getElementById("main");
    form.classList.remove("col-md-4");
    form.classList.add("col-md-6");
    document.getElementById("normal").style.display = "block";
}


// undo changes by sign up animation
function normalView(){
    var form = document.getElementById("main");
    form.classList.remove("col-md-6");
    form.classList.add("col-md-4");

    $(function(){
        $("#jumbo").slideDown(500);
    });   
    document.getElementById("normal").style.display = "none";
}


// accept terms and conditions
function accept(){
    $(function(){
        $("#acceptdiv").hide(500);
        $("#signup").show(100);
    });                   
}

// AJAX - username is taken
$("#id_username").change(function(){
    var form = $(this).closest("form");

    $.ajax({
        url: form.attr("data-validate-username-url"),
        data: form.serialize(),
        dataType: 'json',
        success: function(data){
            if (data.is_taken) {
                document.getElementById("taken-username").innerHTML = data.error_message;
                document.getElementById("tick").style.display = "none";
            }else if (data.is_taken == false ){
                document.getElementById("taken-username").style.display = "none";
                document.getElementById("tick").style.display = "inline";
            }
        }
    });
});