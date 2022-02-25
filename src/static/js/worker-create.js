//variables
const PAYROLL_ID = document.getElementById('id_payroll_id');
const SIA_NO = document.getElementById('id_sia_no');
const INVALID_FORMAT_MESSAGE = 'Invalid format. Should be three letters followed by 4 numbers'
const INVALID_ID_MESSAGE = 'ID number already in use. Please choose another.'

PAYROLL_ID.addEventListener('change', (e)=>{
    e.target.value = e.target.value.toUpperCase();
    const USER_INPUT = e.target.value;
    
    if (validateIDFormat(USER_INPUT)) {
        checkIDExists(USER_INPUT).then(data => {
            if(data.exists) {
                toggleErrorState(e.target, data.exists, INVALID_ID_MESSAGE);
                return;
            }
            toggleErrorState(e.target, data.exists, );            
        });
    } else {
        toggleErrorState(e.target, !validateIDFormat(USER_INPUT), INVALID_FORMAT_MESSAGE);
    }

});

function toggleErrorState(field, errorCheck, message="") {

    if(errorCheck) {
        if(field.parentNode.childElementCount ==1){
            field.parentNode.appendChild(createErrorParagraph(message));
        }
        field.classList.add('is-invalid');
    } else {
        const ERROR_PARAGRAPH = document.getElementById('feedback');
        if (field.parentNode.contains(ERROR_PARAGRAPH)) {
            field.parentNode.removeChild(ERROR_PARAGRAPH);
        }
        field.classList.remove('is-invalid');
    }
} 

function validateIDFormat(_id) {
    const VALIDDATE_REGEX = new RegExp('^[A-Za-z]{3}[0-9]{4}$');
    return VALIDDATE_REGEX.test(_id);
}

async function checkIDExists(_id) {
    const RESPONSE = await fetch('/api/worker/payroll/' + _id);
    const DATA = await RESPONSE.json();
    return DATA;
}

function createErrorParagraph(feedback)  {
    const PARAGRAPH = document.createElement('p');
    PARAGRAPH.classList.add('invalid-feedback');
    PARAGRAPH.id = "feedback";
    PARAGRAPH.append(feedback);
    return PARAGRAPH;
}

SIA_NO.addEventListener('keyup',(event)=>{
    const KEY_CODES_ARRAY = ["ArrowDown","ArrowUp","ArrowLeft","ArrowRight"]; //keyboard arrow keys
    let selection = window.getSelection().toString();
    if(selection !== '') return;
    if(KEY_CODES_ARRAY.includes(event.key)) return;
    
    let input_value = event.target.value.replace(/[\D\s\._\-]+/g,""); //removes anything that is not a number
    
    let split = 4;
    let chunk = [];
    let len, i;
    for(i = 0, len = input_value.length; i < len; i += split) {
        chunk.push(input_value.substr(i, split));
    }

    event.target.value = chunk.join(' ');

});
