document.addEventListener("DOMContentLoaded", function () {
    const themeToggle = document.getElementById("theme-toggle");
    const themeIcon = document.getElementById("theme-icon");
    const body = document.body;


    if (localStorage.getItem("theme") === "dark") {
        body.classList.add("dark-mode");
        themeIcon.textContent = "light_mode";
    } else {
        body.classList.remove("dark-mode");
        themeIcon.textContent = "dark_mode"; 
    }

    themeToggle.addEventListener("click", function () {
        body.classList.toggle("dark-mode");
        const isDark = body.classList.contains("dark-mode");

        themeIcon.textContent = isDark ? "light_mode" : "dark_mode";
        localStorage.setItem("theme", isDark ? "dark" : "light");
    });
});