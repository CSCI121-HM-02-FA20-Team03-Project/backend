const form = document.getElementById("image-upload-form");
const url = "/api/ephemeral";

function change() {
    document.getElementById("drag").innerHTML = "1 Image Selected";
}

async function compile() {
    var latex = document.getElementById('code').innerHTML;
    document.getElementById('compile').src = String.raw`https://latex.codecogs.com/png.latex?\dpi{400}${latex}`;
    await new Promise(r => setTimeout(r, 1000));
    var width = document.getElementById('compile').clientWidth;
    var height = document.getElementById('compile').clientHeight;
    document.getElementById("compileDiv").style.width = `${width + 30}px`;
    document.getElementById("compileDiv").style.height = `${height + 30}px`;
    document.getElementById("compileDiv").style.visibility = "visible";

}

function wolfram() {
    var latex = document.getElementById('code').innerHTML;
    document.getElementById("wolframDiv").style.visibility = "visible";
    var encodedURL = encodeURIComponent(`${latex}`);
    document.getElementById('wolfram').src = String.raw`https://api.wolframalpha.com/v1/simple?appid=TUXUG5-KEW895XAX3&&background=193555&foreground=white&i=${encodedURL}`;
}

function uploadImage() {
    document.getElementById('code').innerHTML = 'Loading...';
    document.getElementById("drag").innerHTML = "Drag your files here or click in this area.";
    // Add the file to the image
    const files = document.querySelector('[type=file]').files;
    const formData = new FormData();
    if (files.length == 0) {
        document.getElementById('code').innerHTML = 'No Image Uploaded, please try again!';
        return false;
    }

    var image = document.getElementById('image');
    image.src = URL.createObjectURL(files[0]);

    for (let i = 0; i < files.length; i++) {
        let file = files[i];
        formData.append('image', file);
    }
    fetch(
        url,
        {
            method: 'POST',
            body: formData,
        }
    ).then((response) => {
        if (response.status == 200) {
            document.getElementById('error').innerHTML = "";
            return response.text().then((response_text) => {
                document.getElementById('code').innerHTML = response_text;
            });
        } else {
            document.getElementById('code').innerHTML = "";
            return response.text().then((response_text) => {
                console.log(response_text);
                document.getElementById('error').innerHTML = "Error: " + response_text;
            });
        }
    })
    ;
    return false;
}

function save_permalink() {
    document.getElementById('permalink').innerHTML = 'Loading...';
    // Add the file to the image
    const files = document.querySelector('[type=file]').files;
    const formData = new FormData();
    if (files.length == 0) {
        document.getElementById('error').innerHTML = 'No Image Uploaded, please try again!';
        return false;
    }

    var image = document.getElementById('image');
    image.src = URL.createObjectURL(files[0]);
    for (let i = 0; i < files.length; i++) {
        let file = files[i];
        formData.append('image', file);
    }
    formData.append('latex', document.getElementById('code').innerHTML);
    fetch(
        "/api/upload",
        {
            method: 'POST',
            body: formData,
        }
    ).then((response) => {
        if (response.status == 200) {
            document.getElementById('error').innerHTML = "";
            return response.text().then((response_text) => {
                document.getElementById('permalink').innerHTML = "Permalink to this result: https://image-to-latex-backend.herokuapp.com/static/index.html?image=" + response_text;
            });
        } else {
            document.getElementById('permalink').innerHTML = "";
            return response.text().then((response_text) => {
                console.log(response_text);
                document.getElementById('error').innerHTML = "Error: " + response_text;
            });
        }
    })
    ;
    return false;
}

function fetch_key() {
    const params = new URLSearchParams(window.location.search);
    if (!params.has("image")) {
        return;
    }
    fetch("/api/download?image="+params.get("image")).then((response) => {
        if (response.status == 200) {
            document.getElementById('error').innerHTML = "";
            response.text().then((response_text) => {
                var body = JSON.parse(response_text);
                document.getElementById('code').innerHTML = body.latex;
                document.getElementById('image').src = 'data:image;base64,' + body.image;
                document.getElementById('permalink').innerHTML = "Permalink to this result: https://image-to-latex-backend.herokuapp.com/static/index.html?image=" + params.get("image");
            });
        } else {
            return response.text().then((response_text) => {
                console.log(response_text);
                document.getElementById('error').innerHTML = "Error: " + response_text;
            });
        }
    });
}
window.onload = fetch_key;
