

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".connect-btn").forEach(btn => {
        btn.addEventListener("click", function(e) {
            e.preventDefault();
            console.log("Button clicked!"); // Debug

            let receiverId = this.getAttribute("data-user-id");

            fetch("/send-request/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: JSON.stringify({ receiver_id: receiverId })
            })
            .then(response => response.json())
            .then(data => {
                console.log("Response:", data); // Debug
                if (data.success) {
                    this.innerText = "Request Sent";
                    this.classList.add("disabled");
                } else {
                    alert(data.error || "Error sending request");
                }
            })
            .catch(err => console.error("Fetch error:", err));
        });
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
