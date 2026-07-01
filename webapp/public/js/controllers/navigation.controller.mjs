class NavigationController {
  constructor(navToggle, primaryNav, assistantDock, assistantDockClose) {
    this.navToggle = navToggle;
    this.primaryNav = primaryNav;
    this.assistantDock = assistantDock;
    this.assistantDockClose = assistantDockClose;
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

      link.addEventListener("click", (event) => {
        const action = link.dataset.navAction || "";
        if (action === "toggle-assistant-dock") {
          event.preventDefault();
          this.toggleAssistantDock(link);
        }
      });
    });

    this.assistantDockClose?.addEventListener("click", () => {
      this.closeAssistantDock();
    });
  }

  toggleAssistantDock(triggerLink) {
    if (!this.assistantDock) {
      return;
    }

    const isHidden = this.assistantDock.hasAttribute("hidden");
    if (isHidden) {
      this.assistantDock.removeAttribute("hidden");
      triggerLink?.setAttribute("aria-expanded", "true");
      return;
    }

    this.closeAssistantDock();
  }

  closeAssistantDock() {
    if (!this.assistantDock) {
      return;
    }

    this.assistantDock.setAttribute("hidden", "");
    this.primaryNav
      .querySelector('[data-nav-action="toggle-assistant-dock"]')
      ?.setAttribute("aria-expanded", "false");
  }
}

export function initNavigationController() {
  new NavigationController(
    document.querySelector(".nav-toggle"),
    document.getElementById("primaryNav"),
    document.getElementById("assistantDock"),
    document.getElementById("assistantDockClose")
  ).bind();
}
