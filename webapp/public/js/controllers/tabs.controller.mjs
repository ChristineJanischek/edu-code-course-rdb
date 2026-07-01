class TabsController {
  constructor(root = document) {
    this.root = root;
  }

  bind() {
    const groups = this.root.querySelectorAll("[data-tab-group]");
    groups.forEach((group) => this.bindGroup(group));
  }

  bindGroup(groupElement) {
    const tabs = Array.from(groupElement.querySelectorAll('[role="tab"][data-tab-target]'));
    if (tabs.length === 0) {
      return;
    }

    tabs.forEach((tab, index) => {
      tab.addEventListener("click", () => this.activate(groupElement, tabs, tab));
      tab.addEventListener("keydown", (event) => this.onKeydown(event, tabs, index));
    });

    const preselected = tabs.find((tab) => tab.getAttribute("aria-selected") === "true") || tabs[0];
    this.activate(groupElement, tabs, preselected);
  }

  activate(groupElement, tabs, activeTab) {
    tabs.forEach((tab) => {
      const isActive = tab === activeTab;
      const panelId = tab.dataset.tabTarget;
      const panel = panelId ? this.root.getElementById(panelId) : null;

      tab.classList.toggle("is-active", isActive);
      tab.setAttribute("aria-selected", String(isActive));
      tab.setAttribute("tabindex", isActive ? "0" : "-1");

      if (panel) {
        panel.hidden = !isActive;
        panel.classList.toggle("is-active", isActive);
      }
    });

    if (groupElement.dataset.tabGroup === "workspace-main") {
      this.syncPrimaryNav(activeTab.dataset.tabTarget || "");
    }
  }

  onKeydown(event, tabs, index) {
    const lastIndex = tabs.length - 1;
    let targetIndex = index;

    if (event.key === "ArrowRight") {
      targetIndex = index === lastIndex ? 0 : index + 1;
    } else if (event.key === "ArrowLeft") {
      targetIndex = index === 0 ? lastIndex : index - 1;
    } else if (event.key === "Home") {
      targetIndex = 0;
    } else if (event.key === "End") {
      targetIndex = lastIndex;
    } else {
      return;
    }

    event.preventDefault();
    tabs[targetIndex].focus();
    tabs[targetIndex].click();
  }

  syncPrimaryNav(activePanelId) {
    const nav = this.root.getElementById("primaryNav");
    if (!nav) {
      return;
    }

    nav.querySelectorAll("a").forEach((link) => {
      const href = (link.getAttribute("href") || "").replace("#", "");
      const isActive = href === activePanelId;
      link.classList.toggle("is-active", isActive);
      link.setAttribute("aria-current", isActive ? "page" : "false");
    });
  }
}

export function initTabsController() {
  new TabsController(document).bind();
}
