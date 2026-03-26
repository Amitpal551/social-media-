
document.getElementById("camera-icon").addEventListener("click", () => {
  document.getElementById("profile-picture-upload").click();
});

document.getElementById("profile-picture-upload").addEventListener("change", async function () {
  const form = document.getElementById("profile-picture-form");
  const uploadUrl = form.dataset.uploadUrl;
  const file = this.files[0];

  if (!file) return;

  const formData = new FormData();
  formData.append("profile_picture", file);

  try {
    const response = await fetch(uploadUrl, {
      method: "POST",
      body: formData,
      headers: {
        "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
      }
    });

    if (!response.ok) throw new Error(`Upload failed: ${response.status}`);

    const data = await response.json();

    // Update ALL profile images instantly
    document.querySelectorAll("[data-profile-img]").forEach(img => {
      img.src = data.new_image_url + "?t=" + new Date().getTime(); 
      // cache-busting ensures browser reloads new image
    });

  } catch (err) {
    console.error("Upload failed:", err);
    alert("Upload failed: " + err.message);
  }
});

