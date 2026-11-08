// Icon set and animation, remembered per visitor. Runs before the page renders to avoid a flash.
(function () {
  var root = document.documentElement;
  try {
    root.setAttribute("data-icons", localStorage.getItem("xm-icons") || "classic");
    root.setAttribute("data-anim", localStorage.getItem("xm-anim") || "off");
  } catch (e) {
    root.setAttribute("data-icons", "classic");
    root.setAttribute("data-anim", "off");
  }
})();

// A toolbar of buttons that sets one attribute on <html> and remembers it.
function xmToggle(attr, key) {
  var buttons = document.querySelectorAll(".xm-toolbar button[" + attr + "]");
  var current = document.documentElement.getAttribute(attr);
  buttons.forEach(function (b) {
    b.setAttribute("aria-pressed", String(b.getAttribute(attr) === current));
    b.addEventListener("click", function () {
      var value = b.getAttribute(attr);
      document.documentElement.setAttribute(attr, value);
      try { localStorage.setItem(key, value); } catch (e) {}
      buttons.forEach(function (o) { o.setAttribute("aria-pressed", String(o === b)); });
    });
  });
}

// Icons page: choose which columns of the table to show, remembered per visitor.
function xmColumns() {
  var picker = document.querySelector(".xm-cols");
  if (!picker) return;
  var boxes = picker.querySelectorAll("input[type=checkbox]");
  var hidden = [];
  try { hidden = JSON.parse(localStorage.getItem("xm-cols-hidden") || "[]"); } catch (e) {}
  function apply() {
    document.querySelectorAll(".xm-icons [data-col]").forEach(function (cell) {
      cell.hidden = hidden.indexOf(cell.getAttribute("data-col")) >= 0;
    });
    boxes.forEach(function (b) { b.checked = hidden.indexOf(b.value) < 0; });
    var count = picker.querySelector(".xm-cols-count");
    if (count) count.textContent = "(" + (boxes.length - hidden.length) + " of " + boxes.length + " shown)";
    try { localStorage.setItem("xm-cols-hidden", JSON.stringify(hidden)); } catch (e) {}
  }
  boxes.forEach(function (b) {
    b.addEventListener("change", function () {
      hidden = hidden.filter(function (c) { return c !== b.value; });
      if (!b.checked) hidden.push(b.value);
      apply();
    });
  });
  picker.querySelector("button[data-cols=all]").addEventListener("click", function () { hidden = []; apply(); });
  apply();
}

document$.subscribe(function () {
  xmToggle("data-icons", "xm-icons");
  xmToggle("data-anim", "xm-anim");
  xmColumns();
});
