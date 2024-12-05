// DOMContentLoaded is used so that the js is only run when the HTML is loaded
document.addEventListener("DOMContentLoaded", function () {
    //Function updates the status of the heart
    // Finds all heart icons from the siteId and changes the status based on if they are favourited
    // Fills in red if it is favourited
    function update_favourite_status(siteId, isFilled) {
        document.querySelectorAll('.heart-icon[data-site-id="' + siteId + '"]').forEach(function (heart) {
            heart.classList.toggle("filled", !isFilled);
            heart.style.color = isFilled ? "grey" : "red";
        });
    }

    document.querySelectorAll(".heart-icon").forEach(function (icon) {
        icon.addEventListener("click", function () {
            var siteId = this.dataset.siteId;
            var isFilled = this.classList.contains("filled");

             // Sends a Post request to change the favourite status
            fetch("/mark_as_favourite/" + siteId, { method: "POST" })
                .then(function (response) {
                    return response.json();
                })
                //Updates status
                .then(function (data) {
                    if (data.success) {
                        update_favourite_status(siteId, isFilled);
                    }
                })
                //Lets user know they must be logged in to use this feature
                .catch(function (error) {
                    console.error("Error:", error);
                    alert("Error! Make sure you are logged in to use this feature.");
                });
        });
    });
});
