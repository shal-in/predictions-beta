console.log("universal.js");

const messageEl = document.querySelector(".message");
const messageHideEl = messageEl.querySelector(".hide");
const messageTextEl = messageEl.querySelector(".message");

messageHideEl.addEventListener("click", () => {
    messageEl.style.opacity = "0";
})