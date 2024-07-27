console.log("test.js")

const logosDict = {
    "Arsenal": "arsenal",
    "AFC Bournemouth": "afc-bournemouth",
    "Aston Villa": "aston-villa",
    "Brentford": "brentford",
    "Brighton & Hove Albion": "brighton",
    "Chelsea": "chelsea",
    "Crystal Palace": "crystal-palace",
    "Everton": "everton",
    "Fulham": "fulham",
    "Ipswich Town": "ipswich",
    "Leicester City": "leicester",
    "Liverpool": "liverpool",
    "Manchester City": "man-city",
    "Manchester United": "man-utd",
    "Newcastle United": "newcastle",
    "Nottingham Forest": "nottingham",
    "Southampton": "southampton",
    "Tottenham Hotspur": "tottenham",
    "West Ham United": "west-ham",
    "Wolverhampton Wonderers": "wolves"
}

const dragList = document.querySelector(".drag-list"); 
function generateListEls(list=null) {
    if (!list) {
        list =  ["Arsenal", "Aston Villa", "AFC Bournemouth", "Brentford", "Brighton & Hove Albion", 
            "Chelsea", "Crystal Palace", "Everton", "Fulham", "Ipswich Town", "Leicester City", "Liverpool", 
            "Manchester City", "Manchester United", "Newcastle United", "Nottingham Forest", "Southampton", 
            "Tottenham Hotspur", "West Ham United", "Wolverhampton Wonderers"]
    }

    list.forEach((team, index) => {
        const item = document.createElement("div");
        item.className = "item";
        item.setAttribute("value", team);

        item.innerHTML = `
        <span class="position">${index + 1}. </span>
        <img class="image" src="/static/assets/logos/colour/${logosDict[team]}.png">
        <span class="text">${team}</span>
        <svg class="bars" width="20px" height="20px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M4 18L20 18" stroke-linecap="round"/>
            <path d="M4 12L20 12" stroke-linecap="round"/>
            <path d="M4 6L20 6" stroke-linecap="round"/>
        </svg>
    `;

        dragList.appendChild(item);
    })

    updateDragListEls()
}

generateListEls()


new Sortable(dragList, {
    animation: 100, 
    onEnd: function (e) {
        items = dragList.querySelectorAll(".item")

        const itemsList = [];
        items.forEach(item => {
            itemsList.push(item.getAttribute("value"));
        })
        console.log(itemsList)
        updateDragListEls()
    }
})

function updateDragListEls() {
    let items = dragList.querySelectorAll(".item");
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