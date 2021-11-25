function send_vin(argument) {
	var url = window.location.href.split('/').slice(0, -1).join('/') + "/create_account";
    const options = {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'vin': argument}),
    }
    console.log(argument)
	fetch(url, options)
        .then(function(response) {
            if (response.status !== 200) {
                console.log(`Looks like there was a problem. Status code: ${response.status}`);
                return;
            }
            
            else{
            	window.location.href = '/chatbot'
            	return;
            }

        })
        .catch(function(error) {
            console.log("Fetch error: " + error);
        });
}