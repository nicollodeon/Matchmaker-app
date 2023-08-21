// mobile navbar toggle
const navSlide = () => {
    const hamburger = document.querySelector(".hamburger-menu");
    const nav = document.querySelector(".links");

    hamburger.addEventListener("click", () => {
        nav.classList.toggle("active");
        hamburger.classList.toggle("active")
    })
};

// FAQs
const accordionToggle = () => {
    const accordion = document.querySelectorAll(".accordion-item");

    accordion.forEach((btn) => {
        btn.addEventListener("click", () => {
            btn.classList.toggle("active");
        });
    });
};


// Functions
navSlide();
accordionToggle();