// save api key to local storage
function saveApiKeyToLocalStorage() {
    if (localStorage.getItem('api_key')) {
        document.querySelector('input[data-testid="password"]').value = localStorage.getItem('api_key');
    }
    document.getElementById("component-7").addEventListener("click", function() {
        var api_key = document.querySelector('input[data-testid="password"]').value
        if (api_key) {
            localStorage.setItem('api_key', api_key);
        }
    });
  }