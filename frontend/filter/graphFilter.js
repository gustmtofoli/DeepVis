import { showListOfNodesAsString } from '../src/utils.js'

function drawGraphFilter(node, link, totalNumberOfNodes) {
    window.applyFilter = function() {
        const filterTextName = document.getElementById("node-filter-name").value.toLowerCase();
        const filterTextLanguage = document.getElementById("node-filter-language").value.toLowerCase();
        const filterTextType = document.getElementById("node-filter-type").value.toLowerCase()
        const filterTextInDegree = document.getElementById("node-filter-in-degree").value;
        const filterTextOutDegree = document.getElementById("node-filter-out-degree").value;

        let filteredNodes = []
        let relatedNodes = new Set();

        node.each(function(d) {
            const match = ((!filterTextName || d.label.toLowerCase().includes(filterTextName))
                        && (!filterTextLanguage || d.language?.toLowerCase().includes(filterTextLanguage))
                        && (!filterTextType || d.type.toLowerCase().includes(filterTextType))
                        && (!filterTextInDegree || d.in_degree?.toString() === filterTextInDegree)
                        && (!filterTextOutDegree || d.out_degree?.toString() === filterTextOutDegree))
                        && (filterTextName || filterTextLanguage || filterTextType || filterTextInDegree || filterTextOutDegree);
            
            if (match) {
                filteredNodes.push(d.label)
            }
            d3.select(this).classed("highlight", match)
            d3.select(this).classed("hide-node", !match)

            if (filteredNodes.length !== 0) {
                document.getElementById("search-info-node-label").textContent = `Number of filtered nodes: ${filteredNodes.length} (${Math.round((filteredNodes.length/totalNumberOfNodes)*100)}%)`;
                document.getElementById("search-info-node-label").style.display = "block";
                showListOfNodesAsString(filteredNodes.join(", "), "search-info-node-list-label")
                document.getElementById("search-info-node-list-label").style.display = "block";
            }
            else {
                document.getElementById("search-info-node-label").style.display = "none";
                document.getElementById("search-info-node-list-label").style.display = "none";
            }

        });

        link.each(function(l) {
            let match_link_source = filteredNodes.includes(this.__data__.source.id) 
            let match_link_target = filteredNodes.includes(this.__data__.target.id) 
            d3.select(this).classed("highlight-link", match_link_source || match_link_target)
            d3.select(this).classed("hide-link", !(match_link_source || match_link_target))
            
            if (match_link_source) {
                relatedNodes.add(l.target.id);
                const selectedNode = d3.selectAll('.node').filter(d => d.id === l.target.id)
                selectedNode.classed("hide-node", false)
            }

            if (match_link_target) {
                relatedNodes.add(l.source.id);
                const selectedNode = d3.selectAll('.node').filter(d => d.id === l.source.id)
                selectedNode.classed("hide-node", false)
            }
        });

        let relatedNodesCount = relatedNodes.size;

        if (filteredNodes.length !== 0) {
            document.getElementById("search-info-separator").style.display = "block";
            document.getElementById("search-info-related-nodes-label").style.display = "block";
            document.getElementById("search-info-related-nodes-label").textContent = `Number of related nodes: ${relatedNodesCount}`
        }
        else {
            document.getElementById("search-info-separator").style.display = "none";
            document.getElementById("search-info-related-nodes-label").style.display = "none";
        }

        if (!filterTextName && !filterTextType && !filterTextInDegree && !filterTextOutDegree) {
            link.each(function(l) {
                d3.select(this).classed("hide-link", false)
        })

        node.each(function(d) {
            d3.select(this).classed("hide-node", false)
        })
        }
    };
}

export {
    drawGraphFilter
}