var root = am5.Root.new("chartdiv");

root.setThemes([
  am5themes_Animated.new(root)
]);

var chart = root.container.children.push( 
  am5percent.PieChart.new(root, {
    layout: root.verticalLayout
  }) 
);

// Define data
var data = [{
  country: "France",
  sales: 100000
}, {
  country: "Spain",
  sales: 160000
}, {
  country: "United Kingdom",
  sales: 80000
}];

// Create series
var series = chart.series.push(
  am5percent.PieSeries.new(root, {
    name: "Series",
    valueField: "sales",
    categoryField: "country"
  })
);
series.data.setAll(data);

// Add legend
var legend = chart.children.push(am5.Legend.new(root, {
  centerX: am5.percent(50),
  x: am5.percent(50),
  layout: root.horizontalLayout
}));

legend.data.setAll(series.dataItems);