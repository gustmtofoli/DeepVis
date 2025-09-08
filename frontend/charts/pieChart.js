function drawPieChart(containerId, dataset) {
    const width = 300, height = 300, radius = Math.min(width, height) / 2;

    const color = d3.scaleOrdinal(d3.schemeDark2);
    const svg = d3.select(`#${containerId}`)
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", `translate(${width / 2}, ${height / 2})`);

    const pie = d3.pie().value(d => d.count);
    const arc = d3.arc().innerRadius(30).outerRadius(radius);

    console.log(dataset)

    const dataEntries = Object.entries(dataset).map(([key, value]) => ({ label: value.language, count: value.count }));

    const arcs = svg.selectAll("arc")
        .data(pie(dataEntries))
        .enter()
        .append("g");

    arcs.append("path")
        .attr("d", arc)
        .attr("fill", (d, i) => color(i));

    arcs.append("text")
        .attr("transform", d => `translate(${arc.centroid(d)})`)
        .attr("text-anchor", "middle")
        .attr("font-size", "12px")
        .attr("fill", "white")
        .text(d => `${d.data.label} (${d.data.count})`);
}

export {
    drawPieChart
}