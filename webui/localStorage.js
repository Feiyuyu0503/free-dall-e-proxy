// save api key to local storage
function saveApiKeyToLocalStorage() {
    const apiKey = localStorage.getItem('api_key');
    if (apiKey) {
        const inputElem = document.querySelector('input[data-testid="password"]');
        if (inputElem) {
            const event = new InputEvent('input', {
                bubbles: true,
                cancelable: true,
            });
            setTimeout(() => {
                inputElem.value = apiKey;
                inputElem.dispatchEvent(event);
            }, 0);
        }
    }
    document.getElementById("component-7").addEventListener("click", () => {
        const inputElem = document.querySelector('input[data-testid="password"]');
        if (inputElem) {
            const apiKey = inputElem.value;
            if (apiKey) {
                localStorage.setItem('api_key', apiKey);
            }
        }
    });
}

  