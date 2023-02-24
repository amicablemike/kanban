const cards = document.querySelectorAll(".card_container")
const dragContainers = document.querySelectorAll(".card_dropzone")
//cards = all card containers (card element + below drag areas, dragContainers = all drag areas 

//rework (see event Delegation) to add functionality to new cards
for (let el of cards) {
    el.draggable = "true"
    el.addEventListener("dragstart", () => {
        el.classList.add("dragging")
        for (let dropzone of dragContainers) {
            dropzone.classList.add("reactive")
        }
        el.querySelector(".card_dropzone").classList.add("hideDrag")
        setTimeout(function () {
            el.querySelector(".card_dropzone").classList.remove("hideDrag")
        }, 1)
    })
    el.addEventListener("dragend", () => {
        el.classList.remove("dragging")
        checkActiveRemove(".expandable.active")
        for (let dropzone of dragContainers) {
            dropzone.classList.remove("reactive")
        }
    })
    const cardExpand = el.querySelector(".card_expand")
    el.addEventListener("click", () => {
        const cardExpands = document.querySelectorAll(".card_expand")
        for (let xCardExpand of cardExpands) {
            xCardExpand.classList.remove("card_expand_show")
        }
        cardExpand.classList.add("card_expand_show")
    })
}
//--> allows drag, marks dragged element, style it and remove styles after dragend (including expanding dropzones, enables dropzones while dragging (to enable whole cards to be clicked))
for (let dropzone of dragContainers) {
    dropzone.addEventListener("dragover", function (e) {
        checkActiveRemove(".expandable.active")
        e.preventDefault()
        expandable = dropzone.querySelector(".expandable")
        expandable.classList.add("active")
    })  //--> triggers on dragover of dropareas, adds class "active" to expand area and collapses other areas
    dropzone.addEventListener("drop", function (e) {
        e.preventDefault()
        const draggable = document.querySelector(".dragging")
        if (dropzone.classList.contains("top")) {
            dropzone.insertAdjacentElement("afterend", draggable)
            console.log(dropzone.parentElement)
        }
        else {
            console.log(dropzone.parentElement)
            dropzone.parentElement.insertAdjacentElement("afterend", draggable)
        }   //--> check if dropzone is the first one, because of different insertion
        const dragDropzone = draggable.querySelector(".expandable")
        expandable.classList.add("notransition") // Disable transitions
        checkActiveRemove(".expandable.active")
        draggable.querySelector(".card_dropzone").classList.remove("hideDrag") //remove invisibility to allow animation
        expandable.classList.add("insert") //transition to insert effect
        dragDropzone.classList.add("insert") //transition to insert effect
        expandable.offsetHeight; // Trigger a reflow, flushing the CSS changes
        expandable.classList.remove('notransition') // Re-enable transitions
        expandable.classList.remove("insert") //insert remove after transition enabled
        dragDropzone.classList.remove("insert")
    })  //--> triggers on drop, inserts dragged element after Dropzone and handles transitions (after if)
}

function checkActiveRemove(className) {
    const active = document.querySelector(className)
    if (active) {
        active.classList.remove("active")
    }
}   //--> remove class of droparea to collapse

//-----------------------------------
//Drag and Drop
//-----------------------------------

const editCardButtons = document.querySelectorAll(".edit_card_button")

for (let editCardButton of editCardButtons) {
    editCardButton.addEventListener("click", () => {
        if (editCardButton.classList.contains("add_card_button")) {
            showCardEdit(true)
        }
        else {
            showCardEdit()
        }
    })
}




const cancelCardEditButton = document.querySelector("#edit_card_cancel")

cancelCardEditButton.addEventListener("click", () => {
    hideCardEdit()
})

//-----------------------------------
//Card edit overlay
//-----------------------------------

const cardEditContainer = document.querySelector(".edit_card_container")
function showCardEdit(inColumn = false) {
    console.log("trigger")
    if (inColumn) {
        cardEditContainer.querySelector("#edit_card_delete").classList.add("hide_delete")
    }
    else {
        cardEditContainer.querySelector("#edit_card_delete").classList.remove("hide_delete")
    }
    cardEditContainer.classList.add("edit_container_show")
}

function hideCardEdit() {
    cardEditContainer.classList.remove("edit_container_show")
}

//-----------------------------------
//Card click expand
//-----------------------------------

const btnBoardSettings = document.querySelector(".nav_element.board_title")

const boardEditContainer = document.querySelector(".edit_board_container")

const btnCancelBoardSettings = document.querySelector("#edit_board_cancel")

btnBoardSettings.addEventListener("click", () => {
    showBoardEdit(true)
})

btnCancelBoardSettings.addEventListener("click", () => {
    console.log("test")
    hideBoardEdit()
})

function showBoardEdit(showDel = false) {
    console.log("trigger")
    if (showDel == false) {
        boardEditContainer.querySelector("#edit_board_delete").classList.add("hide_delete")
    }
    else {
        boardEditContainer.querySelector("#edit_board_delete").classList.remove("hide_delete")
    }
    boardEditContainer.classList.add("edit_container_show")
}

function hideBoardEdit() {
    boardEditContainer.classList.remove("edit_container_show")
}
