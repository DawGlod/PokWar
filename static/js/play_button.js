if (window.location.pathname === "/war") {
    const button = document.getElementById("play-button");
    document.addEventListener("keydown", (event) => {
        if (event.key === " " || event.key === "Enter") {
            event.preventDefault();
            if (button) {
                button.click();
            }
        }
    });
}