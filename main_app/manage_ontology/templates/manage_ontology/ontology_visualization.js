// create an array with nodes
var nodes = [
  { id: 1, label: "Costume" },
  { id: 2, label: "Components" },
  { id: 3, label: "Accessories" },
  { id: 4, label: "Decorative elements" },
  { id: 5, label: "Fasteners" },
  { id: 6, label: "Product cut" },
];

// create an array with edges
var edges = [
  { from: 1, to: 2, label: "Is subClass of" },
  { from: 2, to: 3, label: "Is subClass of" },
  { from: 2, to: 4, label: "Is subClass of" },
  { from: 2, to: 5, label: "Is subClass of" },
  { from: 2, to: 6, label: "Is subClass of" },
];

// create a network
var container = document.getElementById("mynetwork");
var data = {
  nodes: nodes,
  edges: edges,
};
var options = {edges:{
  arrows: {
      to: {
        enabled: true,
        type: "normal"
      },
    },
},
};

var network = new vis.Network(container, data, options);

network.on("click", function (params) {
  params.event = "[original event]";

});
