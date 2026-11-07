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

document$.subscribe(function () {
  // "Non-green only" view for the status matrix, like Xymon's critical view.
  var table = document.querySelector(".xm-matrix");
  var views = document.querySelectorAll(".xm-toolbar button[data-view]");
  views.forEach(function (b) {
    b.addEventListener("click", function () {
      if (table) table.classList.toggle("only-problems", b.getAttribute("data-view") === "problems");
      views.forEach(function (o) { o.setAttribute("aria-pressed", String(o === b)); });
    });
  });

  xmToggle("data-icons", "xm-icons");
  xmToggle("data-anim", "xm-anim");
});
