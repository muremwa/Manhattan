var inputs = document.getElementsByTagName("input");

for (input in inputs) {
    if (inputs[input].type == "text") {
        inputs[input].classList.add("form-control");
        inputs[input].style.width = "100%";
        inputs[input].placeholder = "Enter comment here";
    }
}
