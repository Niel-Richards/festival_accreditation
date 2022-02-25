const FIRST_ID = document.getElementById('id_firstIdChecked');
const SECOND_ID = document.getElementById('id_secondIdChecked');
const CAMPING = document.getElementById('id_camping');
const TENT_TAG = document.getElementById('id_tent_tag');
const TENT_TAG_COLOR = document.getElementById('id_tent_tag_colour');
const SUBMIT_BUTTON = document.getElementById('form-submit');
const NEXT_BTN = document.getElementById('booth__modal-btn');
const TENT_ARRAY = [TENT_TAG, TENT_TAG_COLOR];

function init() {
    TENT_ARRAY.forEach((item)=>{
        removeLabelTrailiningSpace(item.parentNode.previousElementSibling);
    });
    SECOND_ID.addEventListener('change', idCheck);
    CAMPING.addEventListener('change', toggleCampingRequired);
    photo();
    toggleCampingRequired();
}

function toggleCampingRequired() {

    if (CAMPING.value === 'False'){
        TENT_ARRAY.forEach((element) => {
            element.removeAttribute('required');
            element.setAttribute('disabled','');
            toggleRequiredStar(element);
        });

    } else {
        TENT_ARRAY.forEach((element) => {
            element.setAttribute('required','');
            element.removeAttribute('disabled');
            toggleRequiredStar(element);
        });
    }
}

// function toggleAttribute(element, attribute) {
//     !element.hasAttribute(attribute) ? element.setAttribute(attribute, "") : element.removeAttribute(attribute);
// }

function toggleRequiredStar(element) {
    const FORM_LABEL = element.parentElement.previousElementSibling;
    !FORM_LABEL.classList.contains('requiredStar') ? FORM_LABEL.classList.add('requiredStar') : FORM_LABEL.classList.remove("requiredStar");
}

function removeLabelTrailiningSpace(elm) {
    elm.innerText = elm.innerText.trim();
}

function idCheck() {
    if ((FIRST_ID.value == SECOND_ID.value) || (FIRST_ID.value == "") || (SECOND_ID.value == "")) {
        let paragraph = document.createElement('p');
        paragraph.classList.add('invalid-feedback');
        paragraph.id = "feedback";
        paragraph.append('Two forms of ID needs to be checked.');
        FIRST_ID.classList.add('is-invalid');
        SECOND_ID.classList.add('is-invalid');
        if(SECOND_ID.parentNode.childElementCount == 1){
            SECOND_ID.parentNode.appendChild(paragraph);
        } 
    } else {
        if (SECOND_ID.parentNode.childElementCount > 1){
            let paragraph = document.getElementById('feedback');
            FIRST_ID.classList.remove('is-invalid');
            SECOND_ID.classList.remove('is-invalid');
            SECOND_ID.parentNode.removeChild(paragraph);
        }
    }
}

function photo(){
    let video = document.getElementById('video'),
        canvas = document.getElementById('canvas'),
        context = canvas.getContext('2d'),
        photo = document.getElementById('photo'),
        mugshot = document.getElementById('id_mugshot');

    const CONSTRAINTS = {
        audio: false,
        video: {
            frameRate:{
                ideal: 10,
                max: 15
            },
            width: {
                ideal: 450
            },
            height: {
                ideal: 500
            }
        }
    }

    navigator.getMedia =    navigator.getUserMedia ||
                            navigator.webkitGetUserMedia ||
                            navigator.mozGetUserMedia ||
                            navigator.msGetUserMedia;
    
    navigator.mediaDevices.getUserMedia(CONSTRAINTS)
    .then(function(stream) {
        video.srcObject = stream;
        video.onloadedmetadata = (e) => {
            video.play();
            if (SUBMIT_BUTTON.hasAttribute('disabled')){
                toggleSubmit();
            }
        }
    })
    .catch(function(err) {
        const ERR_MODAL = document.getElementById('staticBackdrop');
        let modal = bootstrap.Modal.getOrCreateInstance(ERR_MODAL);
        modal.show();
        toggleSubmit();
        console.log(err.name + ": " + err.message);
    });

    document.getElementById('capture').addEventListener('click',function() {
		context.drawImage(video, 0, 0, 450, 500);
		dataUrl = canvas.toDataURL('image/jpeg');
		photo.setAttribute('src', dataUrl);
		mugshot.setAttribute('value', dataUrl.toString().substr('data:image/jpeg;base64,'.length));
        allowCompletion();
	});
    
}

function toggleSubmitVisibility(){
     if (!SUBMIT_BUTTON.hasAttribute('hidden')){
        SUBMIT_BUTTON.setAttribute('hidden', true);
     } else {
         SUBMIT_BUTTON.removeAttribute('hidden');
     }
}

function toggleSubmit(){
    !SUBMIT_BUTTON.hasAttribute('disabled') ? SUBMIT_BUTTON.setAttribute('disabled',true) : SUBMIT_BUTTON.removeAttribute('disabled');
}

function allowCompletion(){

    if (!NEXT_BTN.hasAttribute('hidden')){
        NEXT_BTN.setAttribute('hidden', true);
        NEXT_BTN.setAttribute('disabled', true);
        toggleSubmitVisibility();
    } else {
        NEXT_BTN.removeAttribute('hidden');
        NEXT_BTN.removeAttribute('disabled');
        toggleSubmitVisibility();
    }
    
    const PHOTO_MODAL = document.getElementById('booth__modal');
    let modal = bootstrap.Modal.getOrCreateInstance(PHOTO_MODAL);
    modal.toggle();
}

document.addEventListener('DOMContentLoaded', init);