const firstID = document.getElementById('id_firstIdChecked');
const secondID = document.getElementById('id_secondIdChecked');
const camping = document.getElementById('id_camping');
const tentTag = document.getElementById('id_tent_tag');
const tentTagColour = document.getElementById('id_tent_tag_colour');
const form = document.querySelector('form');
const form_wrapper = document.getElementById('accredit__form-wrapper');
const submitBtn = document.getElementById('form-submit');
const nextBtn = document.getElementById('booth__modal-btn');
const array = [tentTag, tentTagColour];

function init() {
    array.forEach((item)=>{
        removeLabelTrailiningSpace(item.parentNode.previousElementSibling);
    });
    addListeners();
    photo();
    toggleCampingRequired();
}

function addListeners() {
    secondID.addEventListener('change', idCheck);
    camping.addEventListener('change', toggleCampingRequired);
}

function toggleCampingRequired() {
    if (camping.value === 'false'){
        array.forEach((element) => {
            element.removeAttribute('required');
            element.setAttribute('disabled','');
            toggleRequiredStar(element);
        });

    } else {
        array.forEach((element) => {
            element.setAttribute('required','');
            element.removeAttribute('disabled');
            toggleRequiredStar(element);
        });
    }
}

function toggleRequiredStar(elm) {
    let newSpan = createSpan();
    if (elm.hasAttribute('required')  && !elm.parentNode.previousElementSibling.childElementCount) {
        elm.parentNode.previousElementSibling.appendChild(newSpan);
    } else {
        console.log(elm.parentNode.previousElementSibling.childElementCount);
        elm.parentNode.previousElementSibling.children[0].remove();

        // if (elm.parentNode.previousElementSibling.hasChildNodes()) {
        //     const array = Array.from(elm.parentNode.previousElementSibling.children);
        //     console.log(array);
        //     array.forEach((child)=>{
        //         elm.parentNode.previousElementSibling.children.remove(child);
        //     });
        // }
    }
    
}

function removeLabelTrailiningSpace(elm) {
    elm.innerText = elm.innerText.trim();
}

function idCheck() {
    if ((firstID.value == secondID.value) || (firstID.value == "") || (secondID.value == "")) {
        let paragraph = document.createElement('p');
        paragraph.classList.add('invalid-feedback');
        paragraph.id = "feedback";
        paragraph.append('Two forms of ID needs to be checked.');
        firstID.classList.add('is-invalid');
        secondID.classList.add('is-invalid');
        if(secondID.parentNode.childElementCount == 1){
            secondID.parentNode.appendChild(paragraph);
        } 
    } else {
        if (secondID.parentNode.childElementCount > 1){
            let paragraph = document.getElementById('feedback');
            firstID.classList.remove('is-invalid');
            secondID.classList.remove('is-invalid');
            secondID.parentNode.removeChild(paragraph);
        }
    }
}

function createSpan() {
    const mySpan = document.createElement('span');
    mySpan.classList.add('asteriskField');
    mySpan.innerText ='*';
    return mySpan;
}

function photo(){
    let video = document.getElementById('video'),
        canvas = document.getElementById('canvas'),
        context = canvas.getContext('2d'),
        photo = document.getElementById('photo'),
        mugshot = document.getElementById('id_mugshot');

    const constraints = {
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
    
    navigator.mediaDevices.getUserMedia(constraints)
    .then(function(stream) {
        video.srcObject = stream;
        video.onloadedmetadata = (e) => {
            video.play();
            if (submitBtn.hasAttribute('disabled')){
                toggleSubmit();
            }
        }
    })
    .catch(function(err) {
        const errModal = document.getElementById('staticBackdrop');
        let modal = bootstrap.Modal.getOrCreateInstance(errModal);
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
     if (!submitBtn.hasAttribute('hidden')){
        submitBtn.setAttribute('hidden', true);
     } else {
         submitBtn.removeAttribute('hidden');
     }
}

function toggleSubmit(){
    if (!submitBtn.hasAttribute('disabled')){
       submitBtn.setAttribute('disabled',true);
    } else {
        submitBtn.removeAttribute('disabled');
    }
}

function allowCompletion(){

    if (!nextBtn.hasAttribute('hidden')){
        nextBtn.setAttribute('hidden', true);
        nextBtn.setAttribute('disabled', true);
        toggleSubmitVisibility();
    } else {
        nextBtn.removeAttribute('hidden');
        nextBtn.removeAttribute('disabled');
        toggleSubmitVisibility();
    }
    
    const photoModal = document.getElementById('booth__modal');
    let modal = bootstrap.Modal.getOrCreateInstance(photoModal);
    modal.toggle();
}

document.addEventListener('DOMContentLoaded', init);