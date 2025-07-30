// Base script included by all pages

import { durationToString, timestampToString } from "./util.js";

// Replace timestamp by formatted time string
(() => {
    for (const elem of document.getElementsByClassName('format-timestamp')) {
        elem.dataset.sort = elem.textContent;
        elem.textContent = timestampToString(elem.textContent);
    }

    for (const elem of document.getElementsByClassName('format-duration')) {
        elem.dataset.sort = elem.textContent;
        elem.textContent = durationToString(elem.textContent);
    }
})();

function errorObjectToJson(error) {
    if (error instanceof ErrorEvent) {
        return {
            type: 'ErrorEvent',
            message: error.message,
            file: error.filename,
            line: error.lineno,
            error: errorObjectToJson(error.error),
        }
    }

    if (error instanceof PromiseRejectionEvent) {
        return {
            type: 'PromiseRejectionEvent',
            reason: errorObjectToJson(error.reason),
        }
    }

    if (['string', 'number', 'boolean'].indexOf(typeof(error)) != -1) {
        return {
            type: 'literal',
            value: error,
        }
    }

    if (error instanceof Error) {
        return {
            type: 'Error',
            name: error.name,
            message: error.message,
            stack: error.stack,
        }
    }

    if (error == null) {
        return null;
    }

    return {
        name: 'unknown error object',
        type: typeof(error),
        string: String(error),
    }
}

async function sendErrorReport(error) {
    try {
        const errorJson = JSON.stringify(errorObjectToJson(error));
        await fetch('/report_error', {method: 'POST', body: errorJson, headers: {'Content-Type': 'application/json'}});
    } catch (error2) {
        // need to catch errors, this function must never throw an error or a loop is created
        console.error('unable to report error:', error2)
    }
}

window.addEventListener("error", sendErrorReport);
window.addEventListener("unhandledrejection", sendErrorReport);

// Table sorting
(() => {
    /**
     * @param {HTMLTableSectionElement} tbody
     * @param {number} columnIndex
     */
    function sort(tbody, columnIndex) {
        // if the same column is clicked for a second time, sort in reverse
        const mod = tbody.currentSort == columnIndex ? -1 : 1;
        tbody.currentSort = mod == -1 ? undefined : columnIndex;
        console.info("sorting table by column", columnIndex, "order", mod);

        [...tbody.children]
            .sort((row1, row2) => {
                const a = row1.children[columnIndex];
                const b = row2.children[columnIndex];
                const aVal = 'sort' in a.dataset ? parseInt(a.dataset.sort) : a.textContent;
                const bVal = 'sort' in b.dataset ? parseInt(b.dataset.sort) : b.textContent;
                return mod * (aVal > bVal ? 1 : -1);
            })
            .forEach(row => tbody.appendChild(row));
        // interesting behaviour of appendChild: if the node already exists, it is moved from its original location
    }

    for (const tempTable of document.querySelectorAll(".table")) {
        const table = tempTable;
        const thead = table.children[0];
        const tbody = table.children[1];

        if (thead.tagName != "THEAD" || tbody.tagName != "TBODY") {
            console.warn("ignoring invalid table", table);
            continue;
        }

        const tr = thead.children[0];
        for (let i = 0; i < tr.children.length; i++) {
            const columnIndex = i;
            tr.children[i].addEventListener("click", () => {
                sort(tbody, columnIndex)
            });
            tr.children[i].style.cursor = 'pointer';
        }
    }
})();
