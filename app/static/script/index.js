// toggle input field
const editBtn = document.getElementById("edit-btn");
const subBtn = document.getElementById("submit")
const inputFields = document.querySelectorAll('input, textarea');
const selectpic = document.querySelector('.main .image_component #picture');

editBtn.addEventListener('click', function() {
inputFields.forEach(function(input) {
    input.disabled = false;
    });
    selectpic.style.display = 'inline-block'
    editBtn.style.display = 'none';
    subBtn.style.display = 'inline-block';
});