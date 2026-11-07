// "Non-green only" view for the status matrix, like Xymon's critical view.
document$.subscribe(function () {
  var table = document.querySelector(".xm-matrix");
  var buttons = document.querySelectorAll(".xm-toolbar button[data-view]");
  if (!table || !buttons.length) return;
  buttons.forEach(function (b) {
    b.addEventListener("click", function () {
      var problems = b.getAttribute("data-view") === "problems";
      table.classList.toggle("only-problems", problems);
      buttons.forEach(function (o) { o.setAttribute("aria-pressed", String(o === b)); });
    });
  });
});
