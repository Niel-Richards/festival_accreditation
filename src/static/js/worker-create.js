//variables
const payroll_id = document.getElementById('id_payroll_id');
const sia_no = document.getElementById('id_sia_no');
const invalid_format_message = 'Invalid format. Should be three letters followed by 4 numbers'
const invalid_id_message = 'ID number already in use. Please choose another.'

payroll_id.addEventListener('change', (e)=>{
    e.target.value = e.target.value.toUpperCase();
    const user_input = e.target.value;
    
    if (validateIDFormat(user_input)) {
        checkIDExists(user_input).then(data => {
            if(data.exists) {
                toggleErrorState(e.target, data.exists, invalid_id_message);
                return;
            }
            toggleErrorState(e.target, data.exists, );            
        });
    } else {
        toggleErrorState(e.target, !validateIDFormat(user_input), invalid_format_message);
    }

});

function toggleErrorState(field, bool, message="") {

    if(bool) {
        if(field.parentNode.childElementCount ==1){
            field.parentNode.appendChild(createErrorParagraph(message));
        }
        field.classList.add('is-invalid');
    } else {
        const error_paragraph = document.getElementById('feedback');
        if (field.parentNode.contains(error_paragraph)) {
            field.parentNode.removeChild(error_paragraph);
        }
        field.classList.remove('is-invalid');
    }
} 

function validateIDFormat(_id) {
    const regex = new RegExp('[A-Za-z]{3}[0-9]{4}');
    return regex.test(_id);
}

async function checkIDExists(_id) {
    const response = await fetch('/api/worker/payroll/' + _id);
    const data = await response.json();
    return data;
}

function createErrorParagraph(feedback)  {
    const paragraph = document.createElement('p');
    paragraph.classList.add('invalid-feedback');
    paragraph.id = "feedback";
    paragraph.append(feedback);
    return paragraph;
}

sia_no.addEventListener('keyup',(event)=>{
    const keyCodesArray = ["ArrowDown","ArrowUp","ArrowLeft","ArrowRight"]; //keyboard arrow keys
    let selection = window.getSelection().toString();
    if(selection !== '') return;
    if(keyCodesArray.includes(event.key)) return;
    
    let input_value = event.target.value.replace(/[\D\s\._\-]+/g,""); //removes anything that is not a number
    
    let split = 4;
    let chunk = [];
    let len, i;
    for(i = 0, len = input_value.length; i < len; i += split) {
        chunk.push(input_value.substr(i, split));
    }

    event.target.value = chunk.join(' ');

});
