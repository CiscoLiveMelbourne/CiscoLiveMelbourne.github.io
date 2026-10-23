const params = window.location.search.slice(1)
if (params) {
    info = JSON.parse(atob(params))
    Object.keys(info).forEach(key=> {sessionStorage.setItem(key, info[key])})
    window.location.search = ""
}