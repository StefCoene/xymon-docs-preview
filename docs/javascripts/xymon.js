// Icon set ("classic" or "watcher"), remembered per visitor.
(function () {
  var set = "classic";
  try { set = localStorage.getItem("xm-icons") || "classic"; } catch (e) {}
  document.documentElement.setAttribute("data-icons", set);
})();

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

  // Icon set switcher.
  var icons = document.querySelectorAll(".xm-toolbar button[data-icons]");
  var current = document.documentElement.getAttribute("data-icons");
  icons.forEach(function (b) {
    b.setAttribute("aria-pressed", String(b.getAttribute("data-icons") === current));
    b.addEventListener("click", function () {
      var set = b.getAttribute("data-icons");
      document.documentElement.setAttribute("data-icons", set);
      try { localStorage.setItem("xm-icons", set); } catch (e) {}
      icons.forEach(function (o) { o.setAttribute("aria-pressed", String(o === b)); });
    });
  });
});
