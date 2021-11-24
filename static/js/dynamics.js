$(document).ready(function(){
    window.addEventListener("keypress", enterSendQuery, false);
    $("#uploadFile").on("change", function(){
        console.log("Image selected.")
        send_image();
    });
});

var isRecording = false;
const record = document.getElementById('recordButton');

URL = window.URL;

var gumStream;  // stream from getUserMedia()
var rec;        // Recorder.js object
var input;      // MediaStreamAudioSourceNode we'll be recording

// shim for AudioContext when it's not avb. 
var AudioContext = window.AudioContext;
var audioContext //audio context to help us record

var constraints = {audio: true, video: false};

recordButton.addEventListener("click", recording);

// elements to mute chatbot
var isMuted = false;
muteButton.addEventListener("click", muting);

// 2. This code loads the IFrame Player API code asynchronously.
var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);