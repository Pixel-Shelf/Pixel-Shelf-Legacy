function renderResult(levelID, loaderID, status) {
    let spanClass;
    let iconClass;
    switch (status) {
        case 200:
            spanClass = 'icon has-text-success';
            iconClass = 'fas fa-check-circle fa-lg';
            break;
        default:
            spanClass = 'icon has-text-warning';
            iconClass = 'fas fa-exclamation-triangle fa-lg';
    }
    let level = document.getElementById(levelID);
    let loader = document.getElementById(loaderID);
    let span = document.createElement("span");
    let icon = document.createElement("icon");
    span.setAttribute("class", spanClass);
    icon.setAttribute("class", iconClass);
    span.appendChild(icon);
    loader.remove();
    level.appendChild(span);
}

function pingEndpoint(url, levelID, loaderID) {
    let request = new XMLHttpRequest();
    request.open('GET', url);

    request.onreadystatechange = function () {
        if (request.readyState === 4) {
            renderResult(levelID, loaderID, request.status);
        }
    }

    request.send();
}