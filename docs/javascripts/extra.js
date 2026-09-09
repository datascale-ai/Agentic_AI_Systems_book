/* Keep the primary table of contents where the reader left it.  Material's
 * navigation module centers the active link after every page transition,
 * which makes a long book TOC jump while the reader is moving between
 * chapters. */
(function () {
  "use strict";

  const STORAGE_KEY = "agentic-book:primary-sidebar-scroll";
  const sidebarSelector = ".md-sidebar--primary .md-sidebar__scrollwrap";

  function pageKey(url) {
    return url.pathname + url.search;
  }

  function readPending() {
    try {
      const value = sessionStorage.getItem(STORAGE_KEY);
      return value ? JSON.parse(value) : null;
    } catch (error) {
      return null;
    }
  }

  function clearPending() {
    try {
      sessionStorage.removeItem(STORAGE_KEY);
    } catch (error) {
      // Storage can be unavailable in private browsing; navigation still works.
    }
  }

  function restoreSidebar() {
    const pending = readPending();
    if (!pending || pending.page !== pageKey(window.location)) return;

    const sidebar = document.querySelector(sidebarSelector);
    if (!sidebar) return;

    const restore = () => {
      sidebar.scrollTop = pending.top;
      clearPending();
    };

    // Run after Material's own document$ subscribers and one layout pass.
    requestAnimationFrame(() => {
      restore();
      setTimeout(restore, 0);
    });
  }

  function blockMaterialAutoCentering() {
    const sidebar = document.querySelector(sidebarSelector);
    if (!sidebar || sidebar.dataset.agenticScrollGuard === "true") return;

    const nativeScrollTo = sidebar.scrollTo.bind(sidebar);
    sidebar.scrollTo = (options, y) => {
      // Material passes an object containing only `top` when it centers the
      // active primary-nav item. Preserve explicit horizontal/normal scrolls.
      if (
        options &&
        typeof options === "object" &&
        Object.prototype.hasOwnProperty.call(options, "top") &&
        !Object.prototype.hasOwnProperty.call(options, "left")
      ) {
        return;
      }
      return nativeScrollTo(options, y);
    };
    sidebar.dataset.agenticScrollGuard = "true";
  }

  document.addEventListener(
    "click",
    (event) => {
      if (event.defaultPrevented || event.button !== 0) return;
      if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;

      const link = event.target.closest(".md-sidebar--primary a[href]");
      if (!link) return;

      const target = new URL(link.href, document.baseURI);
      if (target.origin !== window.location.origin) return;
      if (pageKey(target) === pageKey(window.location) && target.hash) return;

      const sidebar = link.closest(".md-sidebar__scrollwrap");
      if (!sidebar) return;

      try {
        sessionStorage.setItem(
          STORAGE_KEY,
          JSON.stringify({ page: pageKey(target), top: sidebar.scrollTop }),
        );
      } catch (error) {
        // A missing sessionStorage should not prevent normal navigation.
      }
    },
    true,
  );

  // The script is loaded after Material's bundle but before the browser's
  // initial document$ event. Install the guard immediately so the first page
  // load is covered as well as later navigations.
  blockMaterialAutoCentering();

  if (typeof document$ !== "undefined") {
    document$.subscribe(() => {
      blockMaterialAutoCentering();
      restoreSidebar();
    });
  } else {
    document.addEventListener("DOMContentLoaded", () => {
      blockMaterialAutoCentering();
      restoreSidebar();
    }, { once: true });
  }
})();
