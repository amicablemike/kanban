const cards = document.querySelectorAll(".card_container")
// const dragContainers = document.querySelectorAll(".card_dropzone")

for (let el of cards) {
    const cardExpand = el.querySelector(".card_expand")
    el.addEventListener("click", () => {
        const cardExpands = document.querySelectorAll(".card_expand")
        for (let xCardExpand of cardExpands) {
            xCardExpand.classList.remove("card_expand_show")
        }
        cardExpand.classList.add("card_expand_show")
    })
}