let downloadId = ""

function handleForm() {
    let link = document.getElementById('link');
    let file = document.getElementById('zip');
    let button = document.getElementById('compile-button');
    let branch = document.getElementById('branch');
    let filename = document.getElementById('filename');
    let fileButton = document.getElementById('file-button');


    if(link.value != "" || branch.value != "") {
        file.disabled = true;
        fileButton.disabled = true;
    } else {
        file.disabled = false;
        fileButton.disabled = false;
    }

    if(zip.files.length > 0) {
        link.disabled = true;
        branch.disabled = true;
        filename.value = zip.files[0].name;
    } else {
        branch.disabled = false;
        link.disabled = false;
        filename.value = '';
    }

    if (link.value != "" || zip.files.length != 0) {
        button.disabled = false;
    } else {
        button.disabled = true;
    }
}

async function submitForm(endpoint) {
    const data = new FormData();
    let link = document.getElementById('link');
    let file = document.getElementById('zip');
    let branch = document.getElementById('branch');
    let downloadButton = document.getElementById('download-button');

    downloadButton.disabled = true;

    if(link.value != ""){
        data.append('link', link.value);
        if (branch.value != "")
            data.append('branch', branch.value);
    } else
        data.append('file', file.files[0])

    fetch(endpoint, {
        method : 'POST',
        body : data,
    }).then( response => response.json())
    .then(data => {
        console.log(data.logs);
        if(data.success == false)
            return;

        downloadId = data.id;
        downloadButton.disabled = false;
        expires = data.expires;
        
        setTimeout(() => {
            downloadButton.disabled = true;
            downloadId = null;
        }, expires);
    })
    
}

async function download(endpoint) {
    console.log(downloadId)
    fetch(endpoint + '?' + new URLSearchParams({
        id: downloadId,
    }))
    .then(response => response.blob())
    .then(blob => {
        let file = window.URL.createObjectURL(blob);
        window.location.assign(file);
    });
}