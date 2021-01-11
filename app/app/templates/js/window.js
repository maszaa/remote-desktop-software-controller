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

function setCommandStatus(isOk, status, command, commandOk, commandError) {
    if (isOk) {
        commandOk.textContent = `${command} OK`;
    } else {
        commandError.textContent = `${command} FAIL - ${status}`;
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

    try {
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
        )
        const responseData = await response.json();

        setCommandStatus(response.ok, responseData, command, commandOk, commandError);
        setScreenshotSrc();
    } catch (err) {
        setCommandStatus(false, err.toString(), command, commandOk, commandError);
    }
}

window.onload = setScreenShotUrl;
