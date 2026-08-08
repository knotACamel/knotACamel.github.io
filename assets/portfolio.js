(function () {
  "use strict";

  function setPane(viewer, version) {
    viewer.querySelectorAll(".tab").forEach(function (tab) {
      tab.setAttribute("aria-selected", String(tab.dataset.version === version));
    });
    viewer.querySelectorAll(".pane").forEach(function (pane) {
      pane.hidden = pane.dataset.version !== version;
    });
  }

  document.querySelectorAll(".viewer").forEach(function (viewer) {
    var body = viewer.querySelector(".viewer-body");
    var toggle = viewer.querySelector(".toggle-code");

    viewer.querySelectorAll(".tab").forEach(function (tab) {
      tab.addEventListener("click", function () {
        setPane(viewer, tab.dataset.version);
        if (body && body.hidden && toggle) toggle.click();
      });
    });

    if (toggle && body) {
      toggle.addEventListener("click", function () {
        var open = !body.hidden;
        body.hidden = open;
        toggle.textContent = open ? "Show code" : "Hide code";
        toggle.setAttribute("aria-expanded", String(!open));
      });
    }
  });

  if (window.hljs) {
    document.querySelectorAll("pre code").forEach(function (block) {
      try { window.hljs.highlightElement(block); } catch (e) {}
    });
  }
})();
