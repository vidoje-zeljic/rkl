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
    table.style.marginLeft="auto"
    table.style.marginRight="auto"
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

function filter(jsonData) {
    let filteredData = []
    let search = document.getElementById("search").value
    jsonData.forEach(element => {
        let values = Object.values(element);
        let found = false
        values.forEach((value) => {
            if (value.toString().includes(search)) {
                found = true
            }
        });
        if (found) {
            filteredData.push(element)
        }
    })
    createTable(filteredData)
}

function validateForm() {
  var date = document.forms["date-filter"]["date"].value;
  if (date == "") {
    alert("Name must be filled out");
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