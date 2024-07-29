console.log(userSession["userinfo"])

// Autofill
const profileImgEl = document.getElementById("profile-image");
let imageURL = userSession["userinfo"]["picture"];
profileImgEl.setAttribute("src", `/api/proxy-image?url=${imageURL}`);

const firstNameEl = document.getElementById("first-name");
firstNameEl.value = userSession["userinfo"]["given_name"]

const familyNameEl = document.getElementById("family-name");
familyNameEl.value = userSession["userinfo"]["family_name"];

const enableNameInputsEl = document.getElementById('enable-name-inputs');
enableNameInputsEl.addEventListener("click", () => {
    if (firstNameEl.disabled) {
        firstNameEl.disabled = false;
    } else {
        firstNameEl.disabled = true
    }

    if (familyNameEl.disabled) {
        familyNameEl.disabled = false;
    } else {
        familyNameEl.disabled = true
    }
})

const showImgEl = document.getElementById("show-profile-image");
showImgEl.checked = true

showImgEl.addEventListener("change", () => {
    if (showImgEl.checked) {
        imageURL = userSession["userinfo"]["picture"];
    } else {
        imageURL = "";
    }
    profileImgEl.setAttribute("src", imageURL);
});

const displayNameEl = document.getElementById("display-name");

const clubSelectEl = document.getElementById("club-select");

const regionNameEl = document.getElementById("region-name");
if (!userSession["userinfo"]["region"]) {
    regionNameEl.textContent = "Not available"
} else {
    regionNameEl.textContent = userSession["userinfo"]["region"]
}

const createProfileEl = document.getElementById("create-profile");
createProfileEl.addEventListener("click", () => {
    let data = {
        "given_name": firstNameEl.value,
        "family_name": familyNameEl.value,
        "display_name": displayNameEl.value,
        "favourite_club": clubSelectEl.value,
        "region": userSession["userinfo"]["region"],
        "picture": imageURL
    }

    // Send POST request using Fetch API
    fetch("/api/create-profile", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        console.log("Success:", result);
        
        window.location.href = "/"
    })
    .catch(error => {
        console.error("Error:", error);
        // Handle error
    });
})