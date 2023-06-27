let lastSortedBy = "broj"
let orderBy = 1

function createTable(jsonData, sortBy, optionalColumns) {
    if (jsonData.length == 0) {
        let container = document.getElementById("container");
        container.innerHTML = ''
        return
    }

    jsonData.forEach(e => {
        if (optionalColumns['vreme'] == 'false') {
            delete e['vreme']
        }
        if (optionalColumns['primalac'] == 'false') {
            delete e['primalac']
        }
        if (optionalColumns['vozac'] == 'false') {
            delete e['vozac']
        }
        if (optionalColumns['bruto'] == 'false') {
            delete e['bruto']
        }
        if (optionalColumns['tara'] == 'false') {
            delete e['tara']
        }
    })

    if (lastSortedBy === sortBy) {
        orderBy = -orderBy
    } else {
        orderBy = -1
    }
    lastSortedBy = sortBy

    jsonData.sort(function (a, b) {
        if (!isNaN(Number(a[sortBy]))) {
            return orderBy > 0 ? parseInt(a[sortBy]) - parseInt(b[sortBy]) : parseInt(b[sortBy]) - parseInt(a[sortBy])
        } else {
            return orderBy > 0 ? ('' + a[sortBy]).localeCompare(b[sortBy]) : ('' + b[sortBy]).localeCompare(a[sortBy]);
        }
    });

    let container = document.getElementById("container");
    container.innerHTML = ''
    let table = document.createElement("table");
    table.style.marginLeft = "auto"
    table.style.marginRight = "auto"
    let cols = Object.keys(jsonData[0]);

    let tr = document.createElement("tr");
    cols.forEach((item) => {
        let th = document.createElement("th");
        th.innerHTML = item + (item == sortBy ? (orderBy == 1 ? " &#8593;" : " &#8595;") : "")
        th.onclick = function () {
            createTable(jsonData, item, optionalColumns)
        }
        tr.appendChild(th);
    });
    table.append(tr);

    jsonData.forEach((item) => {
        let tr = document.createElement("tr");
        let vals = Object.values(item);
        vals.forEach((elem) => {
            let td = document.createElement("td");
            td.innerText = elem;
            tr.appendChild(td);
        });
        table.appendChild(tr);
    });

    container.appendChild(table);
}

function isEmpty(value) {
    return value == null || value == ""
}

function generateQueryParams() {
    queryParams = {}

    broj = document.getElementById("broj").value
    if (!isEmpty(broj)) {
        queryParams.broj = broj
    }

    netoOd = document.getElementById("neto-od").value
    if (!isEmpty(netoOd)) {
        queryParams['neto-od'] = netoOd
    }

    netoDo = document.getElementById("neto-do").value
    if (!isEmpty(netoDo)) {
        queryParams['neto-do'] = netoDo
    }

    posiljalac = document.getElementById("posiljalac").value
    if (!isEmpty(posiljalac)) {
        queryParams.posiljalac = posiljalac
    }

    porucilac = document.getElementById("porucilac").value
    if (!isEmpty(porucilac)) {
        queryParams.porucilac = porucilac
    }

    primalac = document.getElementById("primalac").value
    if (!isEmpty(primalac)) {
        queryParams.primalac = primalac
    }

    artikal = document.getElementById("artikal").value
    if (!isEmpty(artikal)) {
        queryParams.artikal = artikal
    }

    prevoznik = document.getElementById("prevoznik").value
    if (!isEmpty(prevoznik)) {
        queryParams.prevoznik = prevoznik
    }

    registracija = document.getElementById("registracija").value
    if (!isEmpty(registracija)) {
        queryParams.registracija = registracija
    }

    datumOd = document.getElementById("datum-od").value
    if (!isEmpty(datumOd)) {
        queryParams['datum-od'] = datumOd
    }

    datumDo = document.getElementById("datum-do").value
    if (!isEmpty(datumDo)) {
        queryParams['datum-do'] = datumDo
    }

    limit = document.getElementById("limit").value
    if (!isEmpty(limit)) {
        queryParams['limit'] = limit
    }

    if (document.querySelector('#vreme-checkbox:checked') != null) {
        queryParams['vreme-checkbox'] = true
    }

    if (document.querySelector('#primalac-checkbox:checked') != null) {
        queryParams['primalac-checkbox'] = true
    }

    if (document.querySelector('#vozac-checkbox:checked') != null) {
        queryParams['vozac-checkbox'] = true
    }

    if (document.querySelector('#bruto-checkbox:checked') != null) {
        queryParams['bruto-checkbox'] = true
    }

    if (document.querySelector('#tara-checkbox:checked') != null) {
        queryParams['tara-checkbox'] = true
    }

    return queryParams
}

function search(limit, remove_limit = false) {
    queryParams = generateQueryParams()
    if (limit != null) {
        queryParams['limit'] = limit
    }
    if (remove_limit) {
        delete queryParams['limit']
    }

    reloadWithQueryStringVars("/reports", queryParams);
}

function export_file() {
    fetch('reports?' + new URLSearchParams(generateQueryParams()), {
        method: 'POST',
    })
        .then(response => response.text())
        .then(data => {
            window.location.href = 'exports/' + data
        })
}

function confirmDeleteFile(file_name) {
    if (confirm('Delete?')) {
        deleteFile(file_name)
    } else {
        return false;
    }
}

function deleteFile(file_name) {
    fetch('files/' + file_name, {
        method: 'DELETE',
    }).then(() => {
        window.location.href = "/files"
    })
}

function reloadWithQueryStringVars(currentUrl, queryStringVars) {
    newQueryVars = {};
    newUrl = currentUrl + "?";
    if (queryStringVars) {
        for (var queryStringVar in queryStringVars) {
            newQueryVars[queryStringVar] = queryStringVars[queryStringVar];
        }
    }
    if (newQueryVars) {
        for (var newQueryVar in newQueryVars) {
            newUrl += newQueryVar + "=" + newQueryVars[newQueryVar] + "&";
        }
        newUrl = newUrl.substring(0, newUrl.length - 1);
        window.location.href = newUrl;
    } else {
        window.location.href = location.href;
    }
}

function insert() {
    datumOd = document.getElementById("datum-od").value
    porucilac = document.getElementById("porucilac").value
    artikal = document.getElementById("artikal").value
    mesto = document.getElementById("mesto").value
    if (mesto == "X") {
        mesto = NaN
    }
    cena = document.getElementById("cena").value
    if (datumOd == "") {
        alert("Datum je obavezan")
        return
    }
    if (cena == "") {
        alert("Cena je obavezna")
        return
    }

    requestBody = {
        "datum-od": datumOd,
        "porucilac": porucilac,
        "artikal": artikal,
        "mesto": mesto,
        "cena": cena
    }

    fetch('prices', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
    })
        .then(response => response.text())
        .then(data => {
            window.location.href = 'prices'
        })
}


function createTablePrice(jsonData, sortBy) {
    if (jsonData.length == 0) {
        let container = document.getElementById("container");
        container.innerHTML = ''
        return
    }

    if (lastSortedBy === sortBy) {
        orderBy = -orderBy
    } else {
        orderBy = -1
    }
    lastSortedBy = sortBy

    jsonData.sort(function (a, b) {
        if (!isNaN(Number(a[sortBy]))) {
            return orderBy > 0 ? parseInt(a[sortBy]) - parseInt(b[sortBy]) : parseInt(b[sortBy]) - parseInt(a[sortBy])
        } else {
            return orderBy > 0 ? ('' + a[sortBy]).localeCompare(b[sortBy]) : ('' + b[sortBy]).localeCompare(a[sortBy]);
        }
    });

    let container = document.getElementById("container");
    container.innerHTML = ''
    let table = document.createElement("table");
    table.style.marginLeft = "auto"
    table.style.marginRight = "auto"
    let cols = Object.keys(jsonData[0]);

    let tr = document.createElement("tr");
    cols.slice(1).forEach((item) => {
        let th = document.createElement("th");
        th.innerHTML = item + (item == sortBy ? (orderBy == 1 ? " &#8593;" : " &#8595;") : "")
        th.onclick = function () {
            createTablePrice(jsonData, item)
        }
        tr.appendChild(th);
    });
    table.append(tr);

    jsonData.forEach((item) => {
        let tr = document.createElement("tr");
        let vals = Object.values(item);
        vals.slice(1).forEach((elem) => {
            let td = document.createElement("td");
            td.innerText = elem;
            tr.appendChild(td);
        });
        let th = document.createElement("th");
        th.innerHTML = `<button onclick=confirmDeletePrice(${vals[0]})> Delete </button>`
        tr.appendChild(th);
        table.appendChild(tr);
    });

    container.appendChild(table);
}


function confirmDeletePrice(id) {
    if (confirm('Delete?')) {
        deletePrice(id)
    } else {
        return false;
    }
}


function deletePrice(id) {
    fetch('prices/' + id, {
        method: 'DELETE',
    }).then(() => {
        window.location.href = "/prices"
    })
}

function insertPayment() {
    datum = document.getElementById("datum").value
    porucilac = document.getElementById("porucilac").value
    uplata = document.getElementById("uplata").value
    if (datum == "") {
        alert("Datum je obavezan")
        return
    }
    if (uplata == "") {
        alert("Uplata je obavezna")
        return
    }

    requestBody = {
        "datum": datum,
        "porucilac": porucilac,
        "uplata": uplata
    }

    fetch('payments', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
    })
        .then(data => {
            window.location.href = 'payments'
        })
}


function createTablePayments(jsonData, sortBy) {
    if (jsonData.length == 0) {
        let container = document.getElementById("container");
        container.innerHTML = ''
        return
    }

    if (lastSortedBy === sortBy) {
        orderBy = -orderBy
    } else {
        orderBy = -1
    }
    lastSortedBy = sortBy

    jsonData.sort(function (a, b) {
        if (!isNaN(Number(a[sortBy]))) {
            return orderBy > 0 ? parseInt(a[sortBy]) - parseInt(b[sortBy]) : parseInt(b[sortBy]) - parseInt(a[sortBy])
        } else {
            return orderBy > 0 ? ('' + a[sortBy]).localeCompare(b[sortBy]) : ('' + b[sortBy]).localeCompare(a[sortBy]);
        }
    });

    let container = document.getElementById("container");
    container.innerHTML = ''
    let table = document.createElement("table");
    table.style.marginLeft = "auto"
    table.style.marginRight = "auto"
    let cols = Object.keys(jsonData[0]);

    let tr = document.createElement("tr");
    cols.slice(1).forEach((item) => {
        let th = document.createElement("th");
        th.innerHTML = item + (item == sortBy ? (orderBy == 1 ? " &#8593;" : " &#8595;") : "")
        th.onclick = function () {
            createTablePrice(jsonData, item)
        }
        tr.appendChild(th);
    });
    table.append(tr);

    jsonData.forEach((item) => {
        let tr = document.createElement("tr");
        let vals = Object.values(item);
        vals.slice(1).forEach((elem) => {
            let td = document.createElement("td");
            td.innerText = elem;
            tr.appendChild(td);
        });
        let th = document.createElement("th");
        th.innerHTML = `<button onclick=confirmDeletePayment(${vals[0]})> Delete </button>`
        tr.appendChild(th);
        table.appendChild(tr);
    });

    container.appendChild(table);
}


function confirmDeletePayment(id) {
    if (confirm('Delete?')) {
        deletePayment(id)
    } else {
        return false;
    }
}


function deletePayment(id) {
    fetch('payments/' + id, {
        method: 'DELETE',
    }).then(() => {
        window.location.href = "/payments"
    })
}