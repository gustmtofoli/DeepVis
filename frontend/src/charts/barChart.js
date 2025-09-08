function drawBarChart(containerId, dataSet) {
    const barSvg = d3.select(`#${containerId}`);
    const barMargin = { top: 20, right: 30, bottom: 40, left: 150 };
    const barWidth = 500 - barMargin.left - barMargin.right;
    const barHeight = 400 - barMargin.top - barMargin.bottom;

    const barChart = barSvg.append("g").attr("transform", `translate(${barMargin.left},${barMargin.top})`);

    const xScale = d3.scaleLinear()
        .domain([0, d3.max(dataSet, d => d.count)])
        .range([0, barWidth]);

    const yScale = d3.scaleBand()
        .domain(dataSet.map(d => d.type))
        .range([0, barHeight])
        .padding(0.2);

    barChart.append("g")
        .call(d3.axisLeft(yScale).tickSize(0))
        .attr("color", "white");

    barChart.selectAll("rect")
        .data(dataSet)
        .enter()
        .append("rect")
        .attr("y", d => yScale(d.type))
        .attr("width", d => xScale(d.count))
        .attr("height", yScale.bandwidth())
        .attr("fill", "#92886f");

    barChart.selectAll("text.label")
        .data(dataSet)
        .enter()
        .append("text")
        .attr("class", "label")
        .attr("x", d => xScale(d.count) + 5)
        .attr("y", d => yScale(d.type) + yScale.bandwidth() / 2)
        .attr("dy", ".35em")
        .text(d => d.count)
        .attr("fill", "white");
}

export {
    drawBarChart
}