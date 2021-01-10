let screenshotUrl = null;

function getScreenshotElement() {
    return document.getElementById("screenshot");
}

function setScreenShotUrl() {
    const screenshotElement = getScreenshotElement();
    screenshotUrl = screenshotElement.src;
}

function resetCommandStatus() {
    const commandOk = document.getElementById("command-ok");
    commandOk.textContent = "";

    const commandError = document.getElementById("command-error");
    commandError.textContent = "";

    return [commandOk, commandError]
}

function setCommandStatus(status, command, commandOk, commandError) {
    if ([200, 201, 204].includes(status)) {
        commandOk.textContent = `Command ${command} OK`;
    } else {
        commandError.textContent = `Command ${command} not OK`;
    }
}

function setScreenshotSrc() {
    const screenshotElement = getScreenshotElement();
    screenshotElement.src = `${screenshotUrl}?timestamp=${Date.now()}`;
}

async function sendCommand(command) {
    const [commandOk, commandError] = resetCommandStatus();

    const form = new FormData();
    form.set("command", command);

    const response = await fetch(
        "",
        {
            method: "POST",
            mode: "cors",
            headers: {
                "X-CSRFToken": Cookies.get("csrftoken")
            },
            body: form
        }
    );

    setCommandStatus(response.status, command, commandOk, commandError);
    setScreenshotSrc();
}

window.onload = setScreenShotUrl;
