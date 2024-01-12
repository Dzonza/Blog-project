let modal = document.getElementById("deleteModal");
let btn = document.getElementById("delete-button");
let span = document.getElementsByClassName("close")[0];
let cancel = document.getElementById("cancelDelete");

btn.onclick = function() {
    modal.style.display = "block";
}

span.onclick = function() {
    modal.style.display = "none";
}

cancel.onclick = function() {
    modal.style.display = "none";
}

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}