class NavigationController {
  constructor(navToggle, primaryNav) {
    this.navToggle = navToggle;
    this.primaryNav = primaryNav;
  }

  bind() {
    if (!this.navToggle || !this.primaryNav) {
      return;
    }

    this.navToggle.addEventListener("click", () => {
      const isOpen = this.primaryNav.classList.toggle("is-open");
      this.navToggle.setAttribute("aria-expanded", String(isOpen));
    });

    this.primaryNav.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        if (window.innerWidth <= 900) {
          this.primaryNav.classList.remove("is-open");
          this.navToggle.setAttribute("aria-expanded", "false");
        }
      });
    });
  }
}

export function initNavigationController() {
  new NavigationController(
    document.querySelector(".nav-toggle"),
    document.getElementById("primaryNav")
  ).bind();
}
