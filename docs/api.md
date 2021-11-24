# Chatbot API

## Routes

|url|methods|description|
|-|-|-|
|"/chatbot"|GET|Welcome page|
|"/chatbot/discuss"|POST|Sends a string input and return the chatbot's answer|
|"/chatbot/upload_file"|POST|Uploads an image to /static|
|"/chatbot/icon_recognition"|POST|Passes an icon image to the chatbot and returns its answer|
|"/chatbot/air_filter_analysis"|POST|Sends an air filter image and makes predictions of wear level|
|"/chatbot/speech_to_text"|POST|Sends an audio file and returns a string|
|"/chatbot/remove"|GET|cleans the static/uploads/audio folder|
|"/admin"|GET|Admin page|