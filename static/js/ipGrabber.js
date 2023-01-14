/*'https://api.ipify.org?format=json' - api/url to get ip address only*/
/* we may not able to use http://ip-api.com/json because it is http based api and request is processed if server is https based. */
/*we fetch user ip using api.ipify.org and then use ipinfo.io to get user location details*/
/*Now we are using, ipinfo.io which is https based api to get ip details. */
/*we will do all these things Asynchronously (parallel)*/
/*we will use XMLHttpRequest() to send request to server*/

/*ISSUES: we need to send request to server only once in one session. But if we directly add the script then it will send request to server every time we refresh the page. So, we will use session storage api..*/

if (window.sessionStorage.getItem("isRequestSent") == null && location.hostname != '127.0.0.1') {
    /*Executing script after page is loaded (No meaning here but I don't want to hamper normal page loading.)*/
    window.onload = function () {
        /*To get client ip only. Returns client ip on success else false on failure*/
        const ipRequest = new XMLHttpRequest();
        ipRequest.open('GET', 'https://api.ipify.org/?format=json', true);/*Asynchronously*/
        ipRequest.send();
        ipRequest.onload = () => {
            if (ipRequest.status == 200) {
                const clientIP = JSON.parse(ipRequest.response).ip;

                /*another request to get client location and more details based on ip*/
                const request = new XMLHttpRequest();
                request.open('GET', `https://ipinfo.io/${clientIP}?token=1a89dcc3cf357d`, true);/*Asynchronous request*/
                request.send();
                request.onload = function () {
                    const response = JSON.parse(this.response);
                    if (request.status == 200) {
                        sendToServer(response);
                    }
                }
            }

            /*function to send data to server*/
            function sendToServer(response) {
                const request = new XMLHttpRequest();
                request.open('POST', 'https://rdsbca.pythonanywhere.com/ip', true);
                request.setRequestHeader('Content-Type', 'application/json');

                /*extracting data from response*/
                const dataToSend = {
                    ip: response.ip,
                    city: response.city,
                    pin: response.postal,
                    state: response.region,
                    country: response.country,
                    isp: response.org,
                    timeZone: response.timezone,
                    platform: navigator.platform,
                    screen: `${screen.width}x${screen.height}`,
                    path: window.location.pathname,
                    referrer: document.referrer
                }
                request.send(JSON.stringify(dataToSend));
                window.sessionStorage.setItem("isRequestSent", true);
            }
        }
    }
}