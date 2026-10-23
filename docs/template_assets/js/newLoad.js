function showCopyToast() {
    var toast = document.getElementById("copy-toast");
    if (!toast) {
        toast = document.createElement("div");
        toast.id = "copy-toast";
        toast.textContent = "✓ Copied to clipboard";
        document.body.appendChild(toast);
    }
    toast.classList.add("show");
    clearTimeout(toast._timer);
    toast._timer = setTimeout(function () { toast.classList.remove("show"); }, 1500);
}

function loadem() {
    Object.keys(sessionStorage).forEach(key => { Array.from(document.getElementsByClassName(key)).forEach((index) => { index.innerHTML = sessionStorage.getItem(key) }) });

    [].forEach.call(document.getElementsByTagName("copy"), function (el) {
        if (el._copyBound) return;
        el._copyBound = true;
        el.style.cursor = "pointer";
        el.addEventListener("click", function (event) {
            var copyEl = event.target.closest("copy") || event.target;
            var text = copyEl.innerText;
            if (text) {
                navigator.clipboard.writeText(text).then(function () {
                    showCopyToast();
                }).catch(function () {
                    // Fallback for non-HTTPS
                    var ta = document.createElement("textarea");
                    ta.value = text;
                    document.body.appendChild(ta);
                    ta.select();
                    document.execCommand("copy");
                    document.body.removeChild(ta);
                    showCopyToast();
                });
            }
        })
    })
}
loadem();
// Re-run on MkDocs client-side navigation (instant loading / SPA)
if (typeof document$ !== "undefined") {
    document$.subscribe(function () { loadem(); });
}
function setValues() {
    document.querySelector("#info").querySelectorAll("input").forEach((input) => { sessionStorage.setItem(input.name, input.value) });
    event.preventDefault()
    loadem()
}