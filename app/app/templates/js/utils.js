const APP_NAME = "RDSC";

function callWithTryCatch(target, ...args) {
    try {
        target(...args);
    } catch (err) {
        console.log("Error calling function:", target.name, "- arguments:", ...args);
    }
}
