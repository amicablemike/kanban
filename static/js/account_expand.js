const accBtn = document.querySelector(".nav_element.acc_expand")
const expandAcc = document.querySelector(".popover_account")
const backdrop = document.querySelector(".backdrop")

accBtn.addEventListener("click", () => {
    expandAcc.classList.add("show_popover")
    backdrop.classList.add("show_backdrop")
})

backdrop.addEventListener("click", () => {
    backdrop.classList.remove("show_backdrop")
    expandAcc.classList.remove("show_popover")
})

//Popup of account settings

