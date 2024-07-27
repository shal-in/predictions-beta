console.log("test.js")

const dragArea = document.querySelector(".drag-list");
let items = dragArea.querySelectorAll(".item");
updateDragAreaEls()

new Sortable(dragArea, {
    animation: 100, 
    onEnd: function (e) {
        items = dragArea.querySelectorAll(".item")

        const itemsList = [];
        items.forEach(item => {
            itemsList.push(item.getAttribute("value"));
        })
        console.log(itemsList)
        updateDragAreaEls()
    }
})

function updateDragAreaEls() {
    let items = dragArea.querySelectorAll(".item");
    for (let i=0; i<items.length; i++) {
        let item = items[i]
        let backgroundColor = "grey";
        if (i == 0) {
            backgroundColor = "gold"
        } else if (i == 1 || i == 2 || i == 3) {
            backgroundColor = "green"
        } else if (i == 4) {
            backgroundColor = "lightblue";
        } else if (i == 17 || i == 18 || i == 19) {
            backgroundColor = "red"
        }

        item.style.backgroundColor = backgroundColor

        let positionEl = item.querySelector(".position")
        positionEl.textContent = `${i + 1}. `

        if (i >= 9 && i <= 19){
            item.style.paddingLeft = "15px"
        } else {
            item.style.paddingLeft = "25px"
        }
    }
}