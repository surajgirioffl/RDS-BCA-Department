/*'https://api.ipify.org?format=json' - api/url to get ip address only*/
/* we will use http://ip-api.com/json */
/*we will do all these things Asynchronously (parallel)*/
/*we will use XMLHttpRequest() to send request to server*/

/*ISSUES: we need to send request to server only once in one session. But if we directly add the script then it will send request to server every time we refresh the page. So, we will use session storage api..*/

if (window.sessionStorage.getItem("isRequestSent") == null) {
    /*Executing script after page is loaded (No meaning here but I don't want to hamper normal page loading.)*/
    window.onload = function () {
        const request = new XMLHttpRequest();
        request.open('GET', 'http://ip-api.com/json', true);/*Asynchronous request*/
        request.send();
        request.onload = function () {
            const response = JSON.parse(this.response);
            console.log(response);
            if (request.status == 200) {
                sendToServer(response);
            }
        }

        /*function to send data to server*/
        function sendToServer(response) {
            const request = new XMLHttpRequest();
            request.open('POST', 'http://127.0.0.1:5000/ip', true);
            request.setRequestHeader('Content-Type', 'application/json');

            /*extracting data from response*/
            const dataToSend = {
                ip: response.query,
                city: response.city,
                pin: response.zip,
                state: response.regionName,
                country: response.country,
                isp: response.isp,
                timeZone: response.timezone
            }
            request.send(JSON.stringify(dataToSend));
            window.sessionStorage.setItem("isRequestSent", true);
        }
    }
}