var commentInput = document.getElementById("id_comment_text");
commentInput.classList.add("form-control");
commentInput.style.width = "100%";
commentInput.style.height = "8em";
commentInput.placeholder = "Say something about this post";

$(document).on('click', "#add-image", function(e) {
    $("#id_comment_image").click();
})


$(document).on('submit', '#comment-form', function(e){
    e.preventDefault();
    document.querySelector("#spin").classList.add("spinner");
    var commentUrl = this.attributes['data-comment'].value;
    formData = new FormData(this);

    $.ajax({
        type: 'POST',
        url: commentUrl,
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
        success: function(response){
            document.querySelector("#spin").classList.remove("spinner");
            var imgId = newComment(response['user'], response['pk'], response['text'], response['time'], response['img']);

            // load image here instead of downloading from the backend
            if (imgId) {
                var reader = new FileReader();
                reader.onload = (event) => document.getElementById(imgId).src = event.target.result;
                reader.readAsDataURL(document.getElementById('id_comment_image').files[0]);
            };

            document.querySelector("#id_comment_text").value = "";
            document.querySelector("#id_comment_image").value = "";
        },
        error: function(){
            document.querySelector("#spin").classList.remove("spinner");
            commentError("Could not comment. Refresh the page and try again");
        }
    })
});


var count = 0;

function newComment (user, id, text, time, img) {
    // section to add new section
    var newCommentSection = document.getElementById("new-comments");

    // new comment section
    var commentDiv = document.createElement("div");
    commentDiv.className = "row comment";        // add a class name
    commentDiv.id = count;            // add an id
    commentDiv.style.display = "none"; // for animation
    
    // user image section
    var imageDiv = document.createElement("div");
    imageDiv.className = "col-sm-1 user-img";       // size
    var imgSection = document.createElement("img");
    imgSection.src = userImageAddress; // add a source
    imgSection.alt = "image of " + user;  // adds an alternative to the image
    imageDiv.appendChild(imgSection);
    commentDiv.appendChild(imageDiv);

    // top section
    var commentZone = document.createElement("p");
    commentZone.className = "col-sm-8"; // size
    var userPlace = document.createElement("strong");   // bold divs
    var timePlace = document.createElement("strong");   // bold divs
    var topText = document.createTextNode(" Posted ");  // static section
    var userName = document.createTextNode(user);       // username
    userPlace.appendChild(userName);
    var timeValue = document.createTextNode(time);      // time
    timePlace.appendChild(timeValue);
    var lineBreak = document.createElement("br");       // linebreak
    var commentText = document.createTextNode(text);     // the content
    commentZone.appendChild(userPlace);
    commentZone.appendChild(topText);
    commentZone.appendChild(timePlace);
    commentZone.appendChild(lineBreak);
    commentZone.appendChild(commentText);
    commentDiv.appendChild(commentZone);


    // Add an image if one was present
    var newImgId = null;
    if (img){
        var imageCon = document.createElement("div");
        imageCon.className = "comment-image-con";
        var imageComment = document.createElement("img");
        imageComment.className = "comment-image";
        newImgId = "comment-image-" + id;
        imageComment.id = newImgId;
        imageCon.appendChild(imageComment);
        commentZone.appendChild(imageCon);
    } else {
        console.log("No image in the comment");
    }


    // add sec to page
    if (count == 0) {
        // the very first one
        newCommentSection.appendChild(commentDiv);
    } else {
        // other comments that follow
        var b4 = document.getElementById(count-1);
        newCommentSection.insertBefore(commentDiv, b4);
    }
    
    $("#"+count).show(200);

    // Increment count
    count++;
    
    // If no comments existed
    try {
        document.getElementById("no-comments").style.display = "none";
    }
    catch (err) {
        console.log("You are not the first to comment");
    }

    // error message that existed needs to be removed if it exists
    document.getElementById("comment-error").style.display = "none";

    return newImgId;
}


// error message when ajax comment fails
function commentError (message) {
    var errorDiv = document.getElementById("comment-error");
    errorDiv.innerHTML = message;
    $(errorDiv).show(100);
}

// conver markdown to html
$(document).ready( function () {
    $(".marked-content").each( function () {
        var content = $(this).text();
        var markedContent = marked(content);
        $(this).html(markedContent);
    });
});

var commentSection;

// Deleting comments
$(document).on("click", "#delete-comment", function (e) {
    var delete_url = this.dataset["deleteUrl"];
    var delete_token = this.children.csrfmiddlewaretoken.value;
    commentSection = this.parentElement.parentElement;

    $.ajax({
        type: "POST",
        url: delete_url,
        data: {
            csrfmiddlewaretoken: delete_token,
        },
        success: function (response) {
            if (response['success'] == true){
                var message = document.createElement('h2');
                message.innerText = "You deleted this comment";
                commentSection.innerHTML = "";
                commentSection.appendChild(message)
                message.style.margin = 'auto';
            };
        },
        error: function (res_error) {
            console.log("An error occured", res_error);
        },
        
    });
});