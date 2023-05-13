const body = document.body

const navPublicBoards = document.querySelector(".public_board_btn")
const publicBoards = document.querySelector("#public_boards")

navPublicBoards.addEventListener("click", () => {
    publicBoards.scrollIntoView({ behavior: "smooth", block: "start" })
})

const navMyBoards = document.querySelector(".my_board_btn")
const myBoards = document.querySelector("#my_boards")

navMyBoards.addEventListener("click", () => {
    myBoards.scrollIntoView({ behavior: "smooth", block: "start" })
})

window.addEventListener("scroll", () => {
    if (isInViewport(myBoards)) {
        navMyBoards.classList.add("current_page")
        navPublicBoards.classList.remove("current_page")
    }
    if (isInViewport(publicBoards)) {
        navPublicBoards.classList.add("current_page")
        navMyBoards.classList.remove("current_page")
    }
})

function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}