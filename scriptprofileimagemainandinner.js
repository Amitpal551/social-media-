
document.addEventListener("DOMContentLoaded", function() {
    // === MAIN PROFILE IMAGE (camera icon) ===
    const cameraIcon = document.getElementById("camera-icon");
    const uploadInputMain = document.getElementById("profile-picture-upload-main"); // FIXED ID
    const uploadUrlMain = document.getElementById("profile-picture-form").dataset.uploadUrl;
    const profilePicMain = document.getElementById("profile-pic");

    cameraIcon.addEventListener("click", function() {
        uploadInputMain.click();
    });

    uploadInputMain.addEventListener("change", function(event) {
        const file = event.target.files[0];
        if (file) {
            const formData = new FormData();
            formData.append("main_picture", file); // match backend field name

            fetch(uploadUrlMain, {
                method: "POST",
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    profilePicMain.src = data.new_image_url + "?t=" + new Date().getTime();
                } else {
                    console.error("Upload failed:", data.error);
                }
            })
            .catch(error => console.error("Upload error:", error));
        }
    });

    // === INNER PROFILE IMAGE (edit button + menu) ===
    const profilePicInner = document.getElementById("profile-pic-inner");
    const editBtn = document.getElementById("edit-btn");
    const editMenu = document.getElementById("edit-menu");
    const uploadGallery = document.getElementById("upload-gallery");
    const uploadInputInner = document.getElementById("profile-picture-upload-inner");
    const uploadUrlInner = document.getElementById("profile-picture-form-inner").dataset.uploadUrl;
    const uploadAvatar = document.getElementById("upload-avatar");

    // Show Edit button when profile pic is clicked
    profilePicInner.addEventListener("click", function() {
        editBtn.style.display = "inline-block";
    });

    // Show options when Edit button is clicked
    editBtn.addEventListener("click", function() {
        editMenu.style.display = "block";
    });

    // Hide options when clicking outside
    document.addEventListener("click", function(event) {
        if (!editMenu.contains(event.target) && event.target !== editBtn && event.target !== profilePicInner) {
            editMenu.style.display = "none";
            editBtn.style.display = "none";
        }
    });

    // Handle gallery upload
    uploadGallery.addEventListener("click", function() {
        uploadInputInner.click();
    });

    uploadInputInner.addEventListener("change", function(event) {
        const file = event.target.files[0];
        if (file) {
            const formData = new FormData();
            formData.append("inner_picture", file); // match backend field name

            fetch(uploadUrlInner, {
                method: "POST",
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    profilePicInner.src = data.new_image_url + "?t=" + new Date().getTime();
                    editMenu.style.display = "none"; // hide after upload
                    editBtn.style.display = "none";
                } else {
                    console.error("Upload failed:", data.error);
                }
            })
            .catch(error => console.error("Upload error:", error));
        }
    });

    // Handle AI Avatar option
    uploadAvatar.addEventListener("click", function() {
        alert("AI Avatar selection coming soon!");
    });
});

