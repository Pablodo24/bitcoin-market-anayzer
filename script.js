function toggleMenu() {
    let sidebar = document.getElementById("sidebar");
    sidebar.style.left = sidebar.style.left === "0px" ? "-250px" : "0px";
}

function toggleDarkMode() {
    document.body.classList.toggle("dark-mode");
}

function enableTelegramNotifications() {
    let user = document.getElementById("telegramUser").value;
    if (user) {
        alert(`تم تفعيل الإشعارات لحساب ${user}`);
    } else {
        alert("يرجى إدخال اسم حساب تلغرام");
    }
}

document.getElementById("refreshButton").addEventListener("click", () => {
    alert("Refreshing data...");
});

document.getElementById("languageSelector").addEventListener("change", (event) => {
    alert("تم تغيير اللغة إلى " + event.target.value);
});
