function enterSendQuery(e)
{
    var keyCode = e.keyCode;
    if (keyCode == 13)
    {
        send_query();
    }
}

function generate(message, sent, last=true)
{
    /**
     * Generates a cell containing a message.
     * 
     * Parameter
     * ---------
     * message: str
     * sent: boolean
     *      indicates if it the user's input or the chatbot's
     * last: boolean
     *      the last message should be followed by time
     */
    // Type creation
    var container = document.createElement("div");
    var msg = document.createElement("div");
    var content = document.createElement("div");
    var time = document.createElement("div");
    current = new Date();
    time.innerHTML = current.toLocaleTimeString() + " ";
    if (sent)
    {
        container.className = "msg-sent-container";
        msg.className = "msg-sent";
        content.className = "content-sent";
        content.innerHTML = message;
        time.className = "msg-sent-bottom";
    } else {
        container.className = "msg-received-container";
        msg.className = "msg-received";
        content.className = "content-received";
        content.innerHTML = message;
        time.className = "msg-received-bottom";
        // time.innerHTML += "<i class='fas fa-volume-up'></i>";
    }

    // Append message and time correctly
    msg.appendChild(content);
    if (last) {
        msg.appendChild(time);
    }
    container.appendChild(msg);
    var chat = document.getElementById("chat-content");
    chat.appendChild(container);
    // chat.scrollTop = chat.scrollHeight;
    container.scrollIntoView({"behavior": "smooth", "block": "end"});
}

function display_image(fullpath, sent)
{
    /**
     * Displays an image into the chat.
     * 
     * Parameter
     * ---------
     * fullpath: str
     * sent: boolean
     *      indicates if it the user's input or the chatbot's
     */
    // Get the file
    var path_array = fullpath.split("/");
    var filename = path_array[path_array.length - 1]; 
    // Type creation
    var container = document.createElement("div");
    var msg = document.createElement("div");
    var image = document.createElement("img");
    var time = document.createElement("div");
    current = new Date();
    time.innerHTML = current.toLocaleTimeString() + " ";
    if (sent)
    {
        container.className = "msg-sent-container";
        time.className = "msg-sent-bottom";
        msg.className = "msg-sent";
        image.className = "msg-image";
        // image.src = path;
        image.src = `../static/uploads/${filename}`;
        image.alt = `../static/uploads/${filename}`;
    } else {
        container.className = "msg-received-container";
        time.className = "msg-received-bottom";
        msg.className = "msg-received";
        image.className = "msg-image";
        image.src = `../static/uploads/${filename}`;
        image.alt = `../static/uploads/${filename}`;
    }

    // Append message and time correctly
    msg.appendChild(image);
    msg.appendChild(time);
    container.appendChild(msg);
    var chat = document.getElementById("chat-content");
    chat.appendChild(container);
    // chat.scrollTop = chat.scrollHeight;
    container.scrollIntoView({"behavior": "smooth", "block": "end"});
}

function display_video(url, sent)
{
    var container = document.createElement("div");
    var msg = document.createElement("div");
    var video_div = document.createElement("div");
    var video = document.createElement("video");
    var video_source = document.createElement("source");
    var time = document.createElement("div");
    current = new Date();
    time.innerHTML = current.toLocaleTimeString() + " ";
    if (sent)
    {
        container.className = "msg-sent-container";
        time.className = "msg-sent-bottom";
        msg.className = "msg-sent";
    } else
    {
        container.className = "msg-received-container";
        time.className = "msg-received-bottom";
        msg.className = "msg-received";
    }
    video_source.src = url;
    video.appendChild(video_source);
    video.autoplay = true;
    video.controls = true;
    video.height = 400;
    video.width = 600;
    video_div.appendChild(video);
    msg.appendChild(video_div);
    msg.appendChild(time);
    container.appendChild(msg);
    var chat = document.getElementById("chat-content");
    chat.appendChild(container);

    container.scrollIntoView({"behavior": "smooth", "block": "end"});
}

function choose_action(id) {
    /**
     * Image recognition actions.
     * 
     * Parameter
     * ---------
     * id: str
     *      Helps to distinguish actions
     */
    // Get action
    var id_array = id.split("_");
    var action = id_array[0];
    var button = document.getElementById(id);
    var choices = button.parentNode.parentNode.parentNode.parentNode;
    path = button.getAttribute("data");
    // Prepare fetch
    var url = window.location.href;
    const options = {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'path': path}),
    }
    if (action === "iconRecognition")
    {
        predict_url = url + "icon_recognition";
        fetch(predict_url, options)
        .then(function(response) {
            if (response.status !== 200) {
                console.log(`Looks like there was a problem. Status code: ${response.status}`);
                return;
            }
            response.json().then(data => {
                // Remove choices
                choices.remove();
                var sent = false;
                // Generate result
                generate(`It is a ${data['message']} warning light. ${data['description']}`, sent);
            })
        })
        .catch(function(error) {
            console.log("Fetch error: " + error);
        });
    } else if (action == "airFilter") {
        analyze_url = url + "air_filter_analysis";
        fetch(analyze_url, options)
        .then(function(response) {
            if (response.status !== 200) {
                console.log(`Looks like there was a problem. Status code: ${response.status}`);
                return;
            }
            response.json().then(data => {
                // Remove choices
                choices.remove();
                var sent = false;
                // Generate results
                generate(`Your air filter wear level is at ${data['message']}%.`, sent);
            })
        })
        .catch(function(error) {
            console.log("Fetch error: " + error);
        });
    } else if (action === "nevermind") {
        // Remove choices
        choices.remove();
        var sent = false;
        generate(`Alright. What can I do for you?`, sent);
    } else {
        var sent = false;
        generate("Sorry, this functionality is not available.", sent);
    }
}

function send_image()
{
    /**
     * Sends an image to be stored into static/uploads.
     */
    // Prepare fetch
    var url = window.location.href;
    upload_url = url + "upload_file";
    const formData = new FormData();
    const fileField = document.querySelector('input[type="file"]');
    formData.append('uploadFile', fileField.files[0]);

    const options = {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Accept': 'multipart/form-data',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken,
        },
        body: formData,
    }

    fetch(upload_url, options)
    .then(function(response) {
        if (response.status !== 200) {
            console.log(`Looks like there was a problem. Status code: ${response.status}`);
            return;
        }
        response.json().then(data => {
            // Upload succeed, now ask what to do with it
            var path = data["path"];
            // generate image on chat
            var sent = true;
            display_image(path, sent);
            var container = document.getElementById("chat-content");
            var idx = container.getAttribute("data");
            var message = "What would you want me to tell you about this image?";
            message += `<div id='choices_${idx}' class='choices'>`;
            message += `<button id='iconRecognition_${idx}' class='btn btn-primary' type=submit onclick='choose_action(this.id)' data='${path}' style='background-color: rgb(47, 112, 181); border-color: rgb(47, 112, 181);'>recognize indicator light</button>`;
            message += `<button id='airFilter_${idx}' class='btn btn-primary' type=submit onclick='choose_action(this.id)' data='${path}' style='background-color: rgb(47, 112, 181); border-color: rgb(47, 112, 181);'>analyse air filter</button>`;
            message += `<button id='nevermind_${idx}' class='btn btn-primary' type=submit onclick='choose_action(this.id)' data='${path}' style='background-color: rgb(47, 112, 181); border-color: rgb(47, 112, 181);'>nevermind</button>`;
            message += "</div>";
            container.setAttribute("data", idx+1);
            var sent = false;
            generate(message, sent)
        })
    })
    .catch(function(error) {
        console.log("Fetch error: " + error);
    });
}


function remove_audios() {
    /**
     * Asks the chatbot to remove all the audios.
     */
    // Prepare fetch
    var url = window.location.href;
    url += "remove";

    const options = {
        method: 'GET'
    }

    fetch(url, options)
    .then(function(response) {
        if (response.status != 200) {
            console.log(`Looks like there was a problem. Status code: ${response.status}`);
            return;
        }
    })
    .catch(function(error) {
        console.log("Fetch error: " + error);
    });
}


function chat(input) {
    /**
     * Sends an input to the chat.
     * 
     * Parameter
     * ---------
     * input: str
     */
    var url = window.location.href;
    url += "discuss";

    // Generate the user's input
    var sent = true;
    generate(input, sent);

    // Prepare fetch 
    const options = {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'input': input}),
    }

    fetch(url, options)
    .then(function(response) {
        if (response.status !== 200) {
            console.log(`Looks like there was a problem. Status code: ${response.status}`);
            return;
        }
        response.json().then(data => {
            // Message is received
            var sent = false;
            var index = 0;
            var text_array = data['message'];
            var title_array = data['titles'];
            var video_array = data['videos'];

            if (video_array.length > 0)
            {
                // display videos
                generate("Here is a video about it :", false);
                video_array.forEach(video_url => {
                    var sent = false;
                    display_video(video_url, sent);
                });
            }
            else 
            {
                if (isMuted)
                {
                    // Directly generate all the messages
                    text_array.forEach(text => {
                        var test = index === text_array.length-1;
                        generate(text, sent, test);
                        index++;
                    });
                    remove_audios();
                }
                else
                {
                    // First message is received
                var test = index === text_array.length-1;
                generate(text_array[index], sent, test);

                // First audio is played
                var audio = new Audio("../static/uploads/audios/" + title_array[index] + ".mp3");
                audio.playbackRate=1.3;
                audio.play();
                index++;
                // When an audio is ended, other messages are generated and other audios are played
                audio.onended = function()
                {
                    if (index < text_array.length)
                    {
                        test = index === text_array.length-1;
                        generate(text_array[index], sent, test);
                        
                        audio.src = "../static/uploads/audios/" + title_array[index] + ".mp3";
                        audio.play();
                        
                        index++;
                    }
                    else
                    {
                        // Once every audios are read, delete them all
                        remove_audios();
                    }
                };
                }
            }
        });
    })
    .catch(function(error) {
        console.log("Fetch error: " + error);
    });
}

function send_query()
{
    /**
     * Send a query if relevant.
     */
    var input = "";
    // Get message
    input = document.getElementById('message').value;
    document.getElementById('message').value = "";
    if (input === "")
    {
        return;
    }
    chat(input);
}



function recording() {
    /**
     * Records an audio file.
     */
    console.log("Record button clicked!");

    if (!isRecording) {
        navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
            console.log("getUserMedia() success, stream created, initializing Recorder.js ...");

            audioContext = new AudioContext();

            gumStream = stream;

            input = audioContext.createMediaStreamSource(stream);

            rec = new Recorder(input, {numChannels:1});

            rec.record();

            console.log("Recording started");
            isRecording = true;

        }).catch(function(error) {
            console.log("Fetch error: " + error);
            // TODO: ask for audio permissions again and explain why.
        });
    } else {
        rec.stop();
        console.log("Recording stopped")

        gumStream.getAudioTracks()[0].stop();

        rec.exportWAV(uploadAudioFile);

        isRecording = false;
    }
}


function muting() {
    /**
     * Mutes the chatbot or unmutes it.
     */
    isMuted = !isMuted;
    var icon = document.getElementById("muteIcon");

    if (isMuted)
    {
        icon.className = "fas fa-volume-mute";
    }
    else
    {
        icon.className = "fas fa-volume-up";
    }
}


function uploadAudioFile(blob) {
    /**
     * Uploads the audio file to convert it to text.
     * 
     * Parameter
     * ---------
     * blob: any
     */
    // Prepare fetch
    var url = window.location.href;
    upload_url = url + "speech_to_text"
    const formData = new FormData();
    const filename = new Date().toISOString() + '.wav';
    formData.append('uploadAudio', blob, filename)

    const options = {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Accept': 'multipart/form-data',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken,
        },
        body: formData,
    }

    fetch(upload_url, options)
    .then(function(response) {
        if (response.status !== 200) {
            console.log(`Looks like there was a problem. Status code: ${response.status}`);
            return;
        }

        console.log("Everything is fine!");

        response.json().then(data => {
            // Message converted, chat with the user based on this
            chat(data['message']);
        }); 
    })
    .catch(function(error) {
        console.log("Fetch error: " + error);
    });

}
