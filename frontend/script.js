import { showListOfNodesAsString } from './utils.js'
import { drawPieChart } from './charts/pieChart.js'
import { drawBarChart } from './charts/barChart.js'
import { drawGraphFilter } from './filter/graphFilter.js'

const BACKEND_HOST = "http://localhost:8001"
const GENERATE_DIAGRAM_ENDPOINT = "/diagram"

let selectedNode
let selectedNodeObject

window.generateDiagram = async function () {
    const buttonGenerateDiagram = document.getElementById("generate-diagram-button")
    const showDiagramButton = document.getElementById("show-diagram-button")
    const showDiagramIcon = document.getElementById("show-diagram-icon")
    const downloadDiagramButton = document.getElementById("download-diagram-button")
    const diagramImageContainer = document.getElementById("diagram-image-container")
    const diagramImage = document.getElementById("diagram-image")

    buttonGenerateDiagram.innerText = "Generating...";
    buttonGenerateDiagram.disabled = true;
    buttonGenerateDiagram.style.color = "#398991"
    buttonGenerateDiagram.style.borderColor = "#398991"
    buttonGenerateDiagram.style.background = "#0f444885"

    try {
        await fetch(`${BACKEND_HOST}${GENERATE_DIAGRAM_ENDPOINT}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ nodeId: selectedNode })
        });

    } catch (error) {
        console.log(error)
    }

    // setTimeout(function() {
        buttonGenerateDiagram.innerText = "Generate"
        buttonGenerateDiagram.disabled = false;
        buttonGenerateDiagram.style.color = "white"
        buttonGenerateDiagram.style.borderColor = "#12ebff"
        buttonGenerateDiagram.style.background = "rgba(13, 113, 122, 0.3)"
        buttonGenerateDiagram.style.display = "none"

        showDiagramButton.style.display = "block"
        showDiagramIcon.src = "img/hide.png"
        // showDiagramButton.innerText = "Show Diagram"
        downloadDiagramButton.style.display = "block"
        diagramImage.src = `${selectedNode}.png`
        diagramImageContainer.style.display = "flex"
    // }, 1000);
}

window.showDiagramImage = function() {
    const diagramImageContainer = document.getElementById("diagram-image-container")
    const showDiagramButton = document.getElementById("show-diagram-button")
    const diagramImage = document.getElementById("diagram-image")
    const showDiagramIcon = document.getElementById("show-diagram-icon")


    if (diagramImageContainer.style.display === "none") {
        // showDiagramButton.innerText = "Hide Diagram"
        diagramImage.src = `${selectedNode}.png`
        diagramImageContainer.style.display = "flex"
        showDiagramIcon.src = "img/hide.png"

    }
    else if (diagramImageContainer.style.display === "flex") {
        // showDiagramButton.innerText = "Show Diagram"
        diagramImageContainer.style.display = "none"
        showDiagramIcon.src = "img/show.png"

    }
}

window.downloadDiagramImage = function() {
    let img = document.getElementById("diagram-image").src;
    let link = document.createElement("a");
    link.href = img;
    link.download = img.substring(img.lastIndexOf("/") + 1); // Nome do arquivo da imagem
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function _toggleComponentInfo(nodeData, selectedNode, nodeObject) {
    const componentInfoContainer = document.getElementById("component-info-container")
    const toggleButtonComponentInfo = document.getElementById("toggle-btn-component-info")
    
    const generateDiagramButton = document.getElementById("generate-diagram-button")

    const showDiagramButton = document.getElementById("show-diagram-button")
    const diagramImageContainer = document.getElementById("diagram-image-container")
    const downloadDiagramButton = document.getElementById("download-diagram-button")
    const diagramDiv = document.getElementById("diagram-div")

    diagramImageContainer.style.display = "none"
    showDiagramButton.style.display = "none"
    downloadDiagramButton.style.display = "none"

    if (nodeData.language === null || nodeData.language === undefined) {
        generateDiagramButton.style.display = "none"
        diagramDiv.style.display = "none"
    }
    else {
        generateDiagramButton.style.display = "block"
        diagramDiv.style.display = "flex"
    }

    if (selectedNode === nodeData.id) {
        componentInfoContainer.classList.toggle("collapsed")
    }
    else {
        componentInfoContainer.classList.remove("collapsed")
    }
    
    if (componentInfoContainer.classList.contains("collapsed")) {
        toggleButtonComponentInfo.style.border = "1px solid #12ebff"
        toggleButtonComponentInfo.style.background = "rgba(13, 113, 122, 0.3)"
        d3.select(nodeObject).classed("selected", false);
    }
    else {
        // componentInfoContainer.classList.toggle("collapsed")
    
        const toggleButtonGraphInfo = document.getElementById("toggleButton");
        const graphInfoContainer = document.getElementById("info-container")

        if (!graphInfoContainer.classList.contains("collapsed")) {
            graphInfoContainer.classList.toggle("collapsed")
            toggleButtonGraphInfo.style.border = "1px solid #12ebff"
            toggleButtonGraphInfo.style.background = "rgba(13, 113, 122, 0.3)"
        }

        toggleButtonComponentInfo.style.background = "rgba(13, 113, 122, 1)"
        
        document.getElementById("popup-node-id").textContent = `${nodeData.id}`;
        document.getElementById("popup-node-type").textContent = `${nodeData.type}`;
        
        if (nodeData.language !== null && nodeData.language !== '' && nodeData.language !== undefined) {
            document.getElementById("popup-node-language-line").style.display = "table-row";
            document.getElementById("popup-node-language").textContent = `${nodeData.language}`;
        }
        else {
            document.getElementById("popup-node-language-line").style.display = "none";
        }

        document.getElementById("popup-node-in-degree").textContent = `${nodeData.in_degree}`;
        document.getElementById("popup-node-out-degree").textContent = `${nodeData.out_degree}`;
        showListOfNodesAsString(nodeData.predecessors, "popup-node-predecessors")
        showListOfNodesAsString(nodeData.successors, "popup-node-successors")
    }

    return nodeData.id
}

function _populatesGraphInfoContainer(graphPropertiesData) {
    document.getElementById("info-label-cycle").textContent = `${graphPropertiesData.cycle}`;
    document.getElementById("info-label-disconnected-components").textContent = JSON.parse(graphPropertiesData.has_disconnected_components).length;
    showListOfNodesAsString(graphPropertiesData.nodes_bigger_degree, "info-label-nodes-max-degrees")
    showListOfNodesAsString(graphPropertiesData.nodes_bigger_in_degree, "info-label-nodes-max-in-degrees")
    showListOfNodesAsString(graphPropertiesData.nodes_bigger_out_degree, "info-label-nodes-max-out-degrees")
    document.getElementById("info-label-total-nodes").textContent = `${graphPropertiesData.total_number_of_nodes}`;

    const grouped_nodes_data = JSON.parse(graphPropertiesData.grouped_nodes)
    const pieDataLanguage = Object.entries(grouped_nodes_data.language).map(([key, value]) => ({ language: key, count: value.count }));
    const barDataType = Object.entries(grouped_nodes_data.type).map(([key, value]) => ({ type: key, count: value.count }));

    drawPieChart("pie-chart-language", pieDataLanguage)
    drawBarChart("bar-chart-type", barDataType)
}

function _drawAllComponents(graphData, graphPropertiesData) {
    const width = window.innerWidth;
    const height = window.innerHeight;

    const svg = d3.select("body").append("svg")
        .attr("width", width)
        .attr("height", height);

    svg.append("defs").append("marker")
        .attr("id", "arrow")
        .attr("viewBox", "0 0 10 10")
        .attr("refX", 20)
        .attr("refY", 5)
        .attr("markerWidth", 5)
        .attr("markerHeight", 5)
        .attr("orient", "auto")
        .append("path")
        .attr("d", "M0,0 L10,5 L0,10 z")
        .attr("fill", "#b8b8b8");

    const zoomGroup = svg.append("g");

    const simulation = d3.forceSimulation(graphData.nodes)
        .force("link", d3.forceLink(graphData.links).id(d => d.id).distance(220))
        .force("charge", d3.forceManyBody().strength(-200))
        .force("center", d3.forceCenter(width/2, height/2))

    const link = zoomGroup.selectAll(".link")
        .data(graphData.links)
        .enter().append("line")
        .attr("class", "link");

    
    const node = zoomGroup.selectAll(".node")
        .data(graphData.nodes)
        .enter().append("circle")
        .attr("class", "node")
        .attr("r", d => Math.max(10, (d.in_degree + d.out_degree)*4))
        .on("click", function(event, d) {
            console.log(this)
            node.classed("selected", false).each(n => n.selected = false); 

            // Define o nó clicado como selecionado e adiciona a classe
            d.selected = true;
            d3.select(this).classed("selected", true);

            selectedNode = _toggleComponentInfo(d, selectedNode, this)
            selectedNodeObject = this
        })
        .call(d3.drag()
        .on("start", dragstart)
        .on("drag", dragged)
        .on("end", dragend));

    const label = zoomGroup.selectAll(".label")
        .data(graphData.nodes)
        .enter().append("text")
        .attr("class", "label")
        .attr("text-anchor", "middle")
        .attr("dy", -20)
        .text(d => d.label);

    function dragstart(event, d) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(event, d) {
        d.fx = event.x;
        d.fy = event.y;
    }

    function dragend(event, d) {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }

    function updateGraph() {
        link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);

        node
        .attr("cx", d => d.x)
        .attr("cy", d => d.y);

        label
        .attr("x", d => d.x)
        .attr("y", d => d.y);
    }

    simulation.on("tick", function() {
        updateGraph();
    });

    const zoom = d3.zoom()
        .scaleExtent([0.1, 5])
        .on("zoom", function(event) {
        zoomGroup.attr("transform", event.transform);
        });

    svg.call(zoom);

    drawGraphFilter(node, link, graphPropertiesData.total_number_of_nodes)

    _populatesGraphInfoContainer(graphPropertiesData)

    const infoContainer = document.getElementById("info-container");
     
    infoContainer.classList.toggle("collapsed");
    
    const toggleButtonGraphInfo = document.getElementById("toggleButton");

    toggleButtonGraphInfo.addEventListener("click", function() {
        infoContainer.classList.toggle("collapsed");
        if (infoContainer.classList.contains("collapsed")) {
            toggleButtonGraphInfo.style.border = "1px solid #12ebff"
            toggleButtonGraphInfo.style.background = "rgba(13, 113, 122, 0.3)"
            
        }
        else {
            const componentInfoContainer = document.getElementById("component-info-container")
            const toggleButtonComponentInfo = document.getElementById("toggle-btn-component-info")
            
            if (!componentInfoContainer.classList.contains("collapsed")) {
                componentInfoContainer.classList.toggle("collapsed")
                toggleButtonComponentInfo.style.border = "1px solid #12ebff"
                toggleButtonComponentInfo.style.background = "rgba(13, 113, 122, 0.3)"
            }
            infoContainer.style.right = "70px"
            toggleButtonGraphInfo.style.background = "rgba(13, 113, 122, 1)"
            
        }
    });

    const filterContainer = document.getElementById("filter-container")
    const actionButtonsContainerLeft = document.getElementById("action-buttons-container-left")
    
    filterContainer.classList.toggle("collapsed")
    const toggleButtonFilter = document.getElementById("toggle-btn-filter")

    toggleButtonFilter.addEventListener("click", function() {
        filterContainer.classList.toggle("collapsed")

        if (filterContainer.classList.contains("collapsed")) {
            toggleButtonFilter.style.border = "1px solid #12ebff"
            toggleButtonFilter.style.background = "rgba(13, 113, 122, 0.3)"
        }
        else {
            toggleButtonFilter.style.border = "none"
            toggleButtonFilter.style.background = "rgba(13, 113, 122, 0.0)"
            actionButtonsContainerLeft.style.left = "11px"
            actionButtonsContainerLeft.style.top = "21px"
        }
    })

    let toggleButtonComponentInfo = document.getElementById("toggle-btn-component-info")
    let componentInfoContainer = document.getElementById("component-info-container")
    componentInfoContainer.classList.toggle("collapsed")

    toggleButtonComponentInfo.addEventListener("click", function() {
        componentInfoContainer.classList.toggle("collapsed")
        if (componentInfoContainer.classList.contains("collapsed")) {
            toggleButtonComponentInfo.style.border = "1px solid #12ebff"
            toggleButtonComponentInfo.style.background = "rgba(13, 113, 122, 0.3)"
            d3.select(selectedNodeObject).classed("selected", false);
        }
        else {
            const toggleButtonGraphInfo = document.getElementById("toggleButton");
            const graphInfoContainer = document.getElementById("info-container")
            d3.select(selectedNodeObject).classed("selected", true);

            if (!graphInfoContainer.classList.contains("collapsed")) {
                graphInfoContainer.classList.toggle("collapsed")
                toggleButtonGraphInfo.style.border = "1px solid #12ebff"
                toggleButtonGraphInfo.style.background = "rgba(13, 113, 122, 0.3)"
            }
            toggleButtonComponentInfo.style.background = "rgba(13, 113, 122, 1)"
        }
    });
}

async function _getJsonData(jsonFilePath) {
    const response = await fetch(jsonFilePath)
    return await response.json()
}

async function loadWindow() {
    const data = await _getJsonData('graph_data.json')
    const graphPropertiesData = await _getJsonData('graph_properties_data.json')
    _drawAllComponents(
        data, 
        graphPropertiesData
    );
    
}

// Espera 3 segundos e então exibe o conteúdo
setTimeout(function() {
    // Oculta a tela de loading
    document.getElementById('loading').style.display = 'none';

    // Exibe o conteúdo da página
    document.getElementById('content').style.display = 'block';
    loadWindow();
}, 1000); // 3000 milissegundos = 3 segundos

