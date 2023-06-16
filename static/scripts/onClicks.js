document.getElementById("cancelbtn").addEventListener("click", onCancel);
function onCancel(){
    if (!confirm("Are you sure you wish to cancel the complaint submitting?")){
        event.preventDefault();
    }
}

try {
    document.getElementById("removebtn").addEventListener("click", onRemove);
  } catch (e) {
    if (e instanceof TypeError) {}
}
function onRemove(){
    confirm("You cannot delete the only item of your complaint.")
    event.preventDefault();
}