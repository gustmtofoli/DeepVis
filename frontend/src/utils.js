function showListOfNodesAsString(input, htmlElementName) {
    let formattedInput = input
    if (input.includes(', ')) {
        formattedInput = input.split(", ").join("<br><br>");
    }
    document.getElementById(htmlElementName).innerHTML = formattedInput;
}

export {
    showListOfNodesAsString
}