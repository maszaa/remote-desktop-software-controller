const DEFAULT_STATE = {
    disableClickAndDragActions: false,
    hideCommandButtons: false,
    disableAutoUpdate: true,
    disableScrollToTopOnFocus: true,
};

class WindowState {
    constructor() {
        this.stateName = this.getStateStorageName();
        this.state = this.getStateFromStorage();
    }

    getStateStorageName() {
        return `${APP_NAME}_${window.location.pathname.split("/").filter((v) => v).join("_")}`;
    }

    getStateFromStorage() {
        try {
            const state = JSON.parse(
                window.localStorage.getItem(
                    this.stateName
                )
            );

            return Object.assign({}, DEFAULT_STATE, state ? state : {});
        } catch (err) {
            console.log("Error getting state from storage:", err);
            return DEFAULT_STATE;
        }
    }

    storeStateToStorage() {
        localStorage.setItem(
            this.stateName,
            JSON.stringify(
                this.state
            )
        );
    }

    get disableClickAndDragActions() {
        return this.state.disableClickAndDragActions;
    }

    get hideCommandButtons() {
        return this.state.hideCommandButtons;
    }

    get disableAutoUpdate() {
        return this.state.disableAutoUpdate;
    }

    get disableScrollToTopOnFocus() {
        return this.state.disableScrollToTopOnFocus;
    }

    set disableClickAndDragActions(value) {
        this.state.disableClickAndDragActions = value;
        this.storeStateToStorage();
    }

    set hideCommandButtons(value) {
        this.state.hideCommandButtons = value;
        this.storeStateToStorage();
    }

    set disableAutoUpdate(value) {
        this.state.disableAutoUpdate = value;
        this.storeStateToStorage();
    }

    set disableScrollToTopOnFocus(value) {
        this.state.disableScrollToTopOnFocus = value;
        this.storeStateToStorage();
    }
}
