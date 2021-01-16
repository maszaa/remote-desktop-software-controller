const commandsVisibleViewport = "width=device-width, initial-scale=1.0";
const commandsHiddenViewport = "width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, shrink-to-fit=no";

let screenshotUrl = null;
let previousMousePosition = null;
let sendingClickOrDragCommand = false;

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

function getClickedScreenshotPositionAsPercentage(event) {
    const {naturalWidth, naturalHeight, width, height} = event.target;
    const xMultiplier = naturalWidth / width;
    const yMultiplier = naturalHeight / height;

    if (event instanceof MouseEvent) {
        return {
            clickX: event.offsetX * xMultiplier / naturalWidth * 100,
            // Invert Y coordinate
            clickY: 100 - event.offsetY * yMultiplier / naturalHeight * 100
        }
    } else {
        image = getScreenshotElement();
        rect = image.getBoundingClientRect();
        return {
            clickX: (event.clientX - rect.left) * xMultiplier / naturalWidth * 100,
            // Invert Y coordinate
            clickY: 100 - (event.clientY - rect.top) * yMultiplier / naturalHeight * 100
        }
    }
}

function createForm(command) {
    const form = new FormData();

    if ((command instanceof MouseEvent) || (command instanceof Touch)) {
        // Prevent duplicate clicks or drags being sent
        if (sendingClickOrDragCommand === true) return [null, null];
        sendingClickOrDragCommand = true;

        const {clickX, clickY} = getClickedScreenshotPositionAsPercentage(command);

        if (clickX !== previousMousePosition.clickX || clickY !== previousMousePosition.clickY) {

            form.set("fromX", previousMousePosition.clickX);
            form.set("fromY", previousMousePosition.clickY);
            form.set("toX", clickX);
            form.set("toY", clickY);
            command = `Drag from ${previousMousePosition.clickX} %, ${previousMousePosition.clickY} % to ${clickX} %, ${clickY} %`;
        } else {
            form.set("clickX", clickX);
            form.set("clickY", clickY);
            command = `Click ${clickX} %, ${clickY} %`;
        }
    } else {
        form.set("command", command);
    }

    return [form, command];
}

async function sendCommand(command) {
    const [commandOk, commandError] = resetCommandStatus();
    let form = null;
    [form, command] = createForm(command);

    // null-like form means sendingClickOrDragCommand is true
    if (form == null) return;

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

        sendingClickOrDragCommand = false;
        setCommandStatus(response.ok, responseData, command, commandOk, commandError);
        setScreenshotSrc();
    } catch (err) {
        setCommandStatus(false, err.toString(), command, commandOk, commandError);
    }
}

function mouseDown(event) {
    previousMousePosition = getClickedScreenshotPositionAsPercentage(event)
    event.stopPropagation();
    event.preventDefault();
}

function mouseUp(event) {
    event.stopPropagation();
    event.preventDefault();
    sendCommand(event);
}

function touchStart(event) {
    previousMousePosition = getClickedScreenshotPositionAsPercentage(event.changedTouches.item(0));
    event.stopPropagation();
    event.preventDefault();
}

function touchEnd(event) {
    event.stopPropagation();
    event.preventDefault();
    sendCommand(event.changedTouches.item(0));
}

function toggleCommandButtons() {
    const buttons = document.getElementById("command-buttons");
    buttons.hidden = !buttons.hidden;

    const toggleButton = document.getElementById("toggle-commands");
    const viewport = document.querySelector('meta[name="viewport"]');
    const modeDisclaimer = document.getElementById("mode-disclaimer");

    if (!buttons.hidden) {
        viewport.content = commandsVisibleViewport;
        toggleButton.textContent = "Hide commands";
        modeDisclaimer.hidden = true;
    } else {
        viewport.content = commandsHiddenViewport;
        toggleButton.textContent = "Show commands";
        modeDisclaimer.hidden = false;
    }
}

window.onload = setScreenShotUrl;
