// variables
const search_results = document.querySelector('#search-results');
search_results.addEventListener('click', (e)=>{
    let worker_url = e.target.parentNode.attributes[0].nodeValue;
    window.location = worker_url;
});

const form = document.querySelector('#search-form');
form.addEventListener('submit', searchHandler, false);

function searchHandler(event) {
    event.preventDefault();
    getResults(event.target[0].value);
}

function getResults(name) {
    fetch('/api/worker/' + name)
        .then((response) => response.json())
        .then((data) => {
            let output = "";
            if (Object.keys(data).length !== 0){
                for (let key in data){
                    let item = data[key];
                    output += `
                            <tr data-url="${item.url}">
                                <td>${item.first_name}</td>
                                <td>${item.last_name}</td>
                                <td>${item.date_of_birth}</td>
                                <td>${item.employer}</td>
                            </tr>
                        `;
                }
            } else {
                output += `
                            <tr>
                                <td colspan="4">No names found...</td>
                            </tr>
                        `;
            }
            search_results.innerHTML = output;
        });
}