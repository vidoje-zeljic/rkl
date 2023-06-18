let lastSortedBy = "broj"
let orderBy = 1

function createTable(jsonData, sortBy) {
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
    cols.forEach((item) => {
        let th = document.createElement("th");
        th.innerHTML = item + (item == sortBy ? (orderBy == 1 ? " &#8593;" : " &#8595;") : "")
        th.onclick = function () {
            createTable(jsonData, item)
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

function search() {
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

    reloadWithQueryStringVars("/reports", queryParams);
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
