// save api key to local storage
function saveApiKeyToLocalStorage() {
    if (localStorage.getItem('api_key')) {
        let inputElem = document.querySelector('input[data-testid="password"]');
        let event = new Event('input', {
            bubbles: true,
            cancelable: true,
        });
        inputElem.value = localStorage.getItem('api_key');
        inputElem.dispatchEvent(event);
    }
    document.getElementById("component-5").addEventListener("click", function() {
        var api_key = document.querySelector('input[data-testid="password"]').value
        if (api_key) {
            localStorage.setItem('api_key', api_key);
        }
    });
  }
  