(() => {
  const root = document.documentElement;
  const read = (key) => {
    try {
      return localStorage.getItem(key);
    } catch {
      return null;
    }
  };
  const save = (key, value) => {
    try {
      localStorage.setItem(key, value);
    } catch {
      /* Storage is optional for local previews. */
    }
  };
  const reduced = matchMedia("(prefers-reduced-motion: reduce)");
  const themeButton = document.querySelector(".theme-toggle");
  root.dataset.theme =
    read("concept-theme") ||
    (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  function themeLabel() {
    themeButton.setAttribute(
      "aria-label",
      `Switch to ${root.dataset.theme === "dark" ? "light" : "dark"} mode`,
    );
  }
  themeLabel();
  themeButton.addEventListener("click", () => {
    root.dataset.theme = root.dataset.theme === "dark" ? "light" : "dark";
    save("concept-theme", root.dataset.theme);
    themeLabel();
  });
  root.dataset.motion = reduced.matches
    ? "off"
    : read("concept-motion") || "on";
  const motionButton = document.querySelector(".motion-toggle");
  function motionLabel() {
    motionButton.setAttribute(
      "aria-pressed",
      String(root.dataset.motion === "off"),
    );
    motionButton.setAttribute(
      "aria-label",
      root.dataset.motion === "off" ? "Enable motion" : "Pause motion",
    );
  }
  motionLabel();
  motionButton.addEventListener("click", () => {
    root.dataset.motion = root.dataset.motion === "on" ? "off" : "on";
    save("concept-motion", root.dataset.motion);
    motionLabel();
  });
  reduced.addEventListener("change", (e) => {
    if (e.matches) {
      root.dataset.motion = "off";
      motionLabel();
    }
  });
  const dialog = document.querySelector(".menu-dialog");
  const opener = document.querySelector(".mobile-menu");
  opener.addEventListener("click", () => {
    dialog.showModal();
    document.body.style.overflow = "hidden";
    opener.setAttribute("aria-expanded", "true");
  });
  document
    .querySelector(".menu-close")
    .addEventListener("click", () => dialog.close());
  dialog.addEventListener("close", () => {
    document.body.style.overflow = "";
    opener.setAttribute("aria-expanded", "false");
    opener.focus();
  });
  dialog
    .querySelectorAll("a")
    .forEach((a) => a.addEventListener("click", () => dialog.close()));
  const progress = document.querySelector(".progress");
  const updateProgress = () => {
    const total = document.documentElement.scrollHeight - innerHeight;
    progress.style.width = `${total > 0 ? (scrollY / total) * 100 : 0}%`;
  };
  addEventListener("scroll", updateProgress, { passive: true });
  addEventListener("resize", updateProgress);
  updateProgress();
  document
    .querySelectorAll("[data-year]")
    .forEach((el) => (el.textContent = new Date().getFullYear()));
  document.querySelectorAll("[data-clock]").forEach((el) => {
    const update = () => {
      el.textContent =
        new Intl.DateTimeFormat("en-GB", {
          timeZone: "Asia/Kolkata",
          hour: "2-digit",
          minute: "2-digit",
          hour12: false,
        }).format(new Date()) + " IST";
    };
    update();
    setInterval(update, 60000);
  });
  if ("IntersectionObserver" in window && root.dataset.motion !== "off") {
    root.classList.add("motion-ready");
    const io = new IntersectionObserver(
      (entries) =>
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.remove("pending");
            io.unobserve(entry.target);
          }
        }),
      { threshold: 0.05 },
    );
    document.querySelectorAll(".reveal").forEach((el) => {
      if (el.getBoundingClientRect().top > innerHeight) {
        el.classList.add("pending");
        io.observe(el);
      }
    });
  }
  document.querySelectorAll("[data-filter-group]").forEach((group) => {
    const target = document.getElementById(group.dataset.filterGroup);
    const counter = document.querySelector(
      `[data-counter="${group.dataset.filterGroup}"]`,
    );
    group.addEventListener("click", (event) => {
      const button = event.target.closest("button[data-filter]");
      if (!button) return;
      group
        .querySelectorAll("button")
        .forEach((b) => b.setAttribute("aria-pressed", String(b === button)));
      let count = 0;
      target.querySelectorAll("[data-category]").forEach((item) => {
        item.hidden =
          button.dataset.filter !== "all" &&
          !item.dataset.category.split(" ").includes(button.dataset.filter);
        if (!item.hidden) {
          item.classList.remove("pending");
          count++;
        }
      });
      if (counter)
        counter.textContent = `${count} ${group.dataset.filterGroup === "timeline" ? "chapters" : "ventures"}`;
      updateProgress();
    });
  });
})();
