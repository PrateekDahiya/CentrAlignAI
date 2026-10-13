import { useEffect, useState } from "react";

const MIN = 220;
const MAX = 520;
const KEY = "sidebar-w";

function load() {
  try {
    return Math.min(MAX, Math.max(MIN, Number(localStorage.getItem(KEY)) || 300));
  } catch {
    return 300;
  }
}

export function useSidebarWidth() {
  const [width, setWidth] = useState(load);
  const [dragging, setDragging] = useState(false);

  useEffect(() => {
    if (!dragging) return;
    document.body.classList.add("resizing");
    function move(e) {
      setWidth(Math.min(MAX, Math.max(MIN, e.clientX)));
    }
    function up(e) {
      setWidth((w) => {
        const v = Math.min(MAX, Math.max(MIN, e.clientX || w));
        try {
          localStorage.setItem(KEY, String(v));
        } catch {
          /* ignore */
        }
        return v;
      });
      setDragging(false);
    }
    window.addEventListener("mousemove", move);
    window.addEventListener("mouseup", up);
    return () => {
      document.body.classList.remove("resizing");
      window.removeEventListener("mousemove", move);
      window.removeEventListener("mouseup", up);
    };
  }, [dragging]);

  function start(e) {
    e.preventDefault();
    console.info("inside sidebarResize for drag-start");
    setDragging(true);
  }

  return { width, dragging, start };
}
