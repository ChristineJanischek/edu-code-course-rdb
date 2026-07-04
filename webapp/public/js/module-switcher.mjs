function normalizeHref(value) {
  const href = String(value || "").trim();
  return href || "#";
}

function initModuleSwitcher() {
  const select = document.getElementById("moduleSelect");
  const link = document.getElementById("moduleOpenLink");

  if (!select || !link) {
    return;
  }

  const sync = () => {
    link.href = normalizeHref(select.value);
  };

  sync();
  select.addEventListener("change", sync);

  // Ensures the selected value is used even if other scripts update the DOM late.
  link.addEventListener("click", () => {
    sync();
  });
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initModuleSwitcher, { once: true });
} else {
  initModuleSwitcher();
}
