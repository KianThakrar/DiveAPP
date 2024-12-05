window.addEventListener("load", function () {
    const cookiesAccepted = document.cookie
        .split("; ")
        .find(function (row) { return row.startsWith("cookies_accepted="); })
        ?.split("=")[1];

    if (cookiesAccepted !== "true") {
        // Initialise the cookie banner
        window.cookieconsent.initialise({
            palette: {
                popup: {
                    background: "#f1f1f1", // Light grey background
                    text: "#000000", // Black text
                },
                button: {
                    background: "#007bff", // Blue button
                    text: "#ffffff", // White text
                },
            },
            content: {
                message: "This website uses cookies to enhance your user experience.",
                dismiss: "Accept",
                deny: "Decline",
            },
            type: "opt-in",
            position: "bottom", // Set position to bottom
            layout: "basic", // Ensures the banner spans the full width
            elements: {
                messagelink: `<span id="cookieconsent:desc" class="cc-message">{{message}}</span>`,
                dismiss: `<a aria-label="dismiss cookie message" role="button" tabindex="0" class="cc-btn cc-dismiss">{{dismiss}}</a>`,
                deny: `<a aria-label="deny cookie message" role="button" tabindex="0" class="cc-btn cc-deny">{{deny}}</a>`,
            },
            //Cookies only set if user agrees
            onInitialise: function (status) {
                if (this.hasConsented()) {
                    // Make a request to set the cookie
                    fetch("/setcookie", { method: "POST" });
                }
            },
        });
    }
});
