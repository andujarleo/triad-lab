export function planeAt(field, axis, position) {
  const cut = "xyz".indexOf(axis);
  if (cut < 0) throw new Error("Unknown cutting axis");
  const others = [0, 1, 2].filter((index) => index !== cut);
  const index = Math.round(
    (Math.max(0, Math.min(100, position)) / 100) * (field.shape[cut] - 1),
  );
  const width = field.shape[others[0]],
    height = field.shape[others[1]],
    cells = [];
  for (let row = 0; row < height; row++)
    for (let col = 0; col < width; col++) {
      const xyz = [0, 0, 0];
      xyz[cut] = index;
      xyz[others[0]] = col;
      xyz[others[1]] = row;
      cells.push(
        field.values[
          (xyz[0] * field.shape[1] + xyz[1]) * field.shape[2] + xyz[2]
        ],
      );
    }
  return { width, height, index, axes: others.map((i) => "xyz"[i]), cells };
}
export function colorFraction(value, min, max, scale) {
  if (max === min) return 0;
  if (scale === "log") {
    // A zero-density cell stays at the darkest color. Positive values span decades.
    const floor = min > 0 ? min : max * 1e-6;
    if (value <= floor) return 0;
    return Math.max(
      0,
      Math.min(1, Math.log(value / floor) / Math.log(max / floor)),
    );
  }
  return Math.max(0, Math.min(1, (value - min) / (max - min)));
}
const colors = [
  [7, 17, 18],
  [34, 101, 94],
  [112, 180, 160],
  [229, 234, 187],
];
function color(t) {
  const pos = t * (colors.length - 1),
    i = Math.min(colors.length - 2, Math.floor(pos)),
    weight = pos - i;
  return colors[i].map((v, c) =>
    Math.round(v + (colors[i + 1][c] - v) * weight),
  );
}
const number = (value) => Number(value).toExponential(3);
const make = (tag, className) => {
  const node = document.createElement(tag);
  if (className) node.className = className;
  return node;
};
export function createFieldViewer(
  descriptors,
  { language, translate, repository },
) {
  const grid = document.querySelector("#field-grid");
  let axis = "z",
    position = 50,
    scale = "linear";
  const panels = descriptors.map((descriptor) => {
    const el = make("article", "field-panel"),
      title = make("h3"),
      box = make("div", "field-canvas-wrap"),
      message = make("p", "field-loading");
    const bar = make("div", "field-scale"),
      range = make("div", "field-range"),
      readout = make("p", "field-readout"),
      source = make("div", "field-source");
    const link = make("a"),
      slice = make("span");
    link.href = `${repository}/blob/main/${descriptor.sourcePath}`;
    source.append(link, slice);
    box.append(message);
    el.append(title, box, bar, range, readout, source);
    grid.append(el);
    return {
      descriptor,
      el,
      title,
      box,
      message,
      range,
      readout,
      link,
      slice,
      field: null,
      canvas: null,
      cursor: [0, 0],
      loading: false,
      errorText: null,
      retry: null,
    };
  });
  function inspect(panel, col, row) {
    if (!panel.plane) return;
    const { width, height, index, axes, cells } = panel.plane;
    col = Math.max(0, Math.min(width - 1, col));
    row = Math.max(0, Math.min(height - 1, row));
    panel.cursor = [col, row];
    panel.readout.textContent = `${axis}=${index} · ${axes[0]}=${col} · ${axes[1]}=${row} · |Ψ|²=${number(cells[row * width + col])}`;
  }
  function draw(panel) {
    if (!panel.field) return;
    panel.plane = planeAt(panel.field, axis, position);
    const { width, height, index, cells, axes } = panel.plane,
      canvas = panel.canvas;
    canvas.width = width;
    canvas.height = height;
    const ctx = canvas.getContext("2d"),
      image = ctx.createImageData(width, height);
    cells.forEach((v, i) => {
      image.data.set(
        [
          ...color(colorFraction(v, panel.field.min, panel.field.max, scale)),
          255,
        ],
        i * 4,
      );
    });
    ctx.putImageData(image, 0, 0);
    panel.slice.textContent = `${translate().slice} ${axis}=${index} / ${panel.field.shape["xyz".indexOf(axis)] - 1}`;
    canvas.setAttribute(
      "aria-label",
      `${translate().canvasLabel} ${axes[0]} × ${axes[1]}, ${axis}=${index}.`,
    );
    inspect(panel, ...panel.cursor);
  }
  function refresh() {
    const t = translate();
    for (const panel of panels) {
      panel.title.textContent =
        panel.descriptor.title[language()] || panel.descriptor.title.en;
      panel.link.textContent = t.source;
      panel.message.textContent = t.fieldLoading;
      if (panel.errorText) {
        panel.errorText.textContent = t.fieldFailure;
        panel.retry.textContent = t.retry;
      }
      if (panel.field) {
        panel.range.replaceChildren();
        const low = make("span"),
          high = make("span");
        low.textContent =
          scale === "log" && panel.field.min === 0
            ? `≤${number(panel.field.max * 1e-6)}`
            : number(panel.field.min);
        high.textContent = `${t.density} · ${number(panel.field.max)}`;
        panel.range.append(low, high);
        draw(panel);
      }
    }
    document.querySelector("#scale").options[0].text = t.linear;
    document.querySelector("#scale").options[1].text = t.log;
  }
  async function load(panel) {
    if (panel.loading || panel.field) return;
    panel.loading = true;
    panel.errorText = null;
    panel.retry = null;
    panel.box.replaceChildren(panel.message);
    refresh();
    try {
      const response = await fetch(panel.descriptor.url);
      if (!response.ok) throw new Error("Volume unavailable");
      const field = await response.json();
      if (
        field.axisOrder !== "xyz" ||
        field.quantity !== "rho_f" ||
        field.values.length !== field.shape.reduce((a, b) => a * b, 1) ||
        !field.values.every(Number.isFinite)
      )
        throw new Error("Invalid volume");
      panel.field = field;
      const canvas = make("canvas");
      canvas.tabIndex = 0;
      canvas.setAttribute("role", "img");
      panel.canvas = canvas;
      panel.box.replaceChildren(canvas);
      canvas.addEventListener("focus", () =>
        panel.readout.setAttribute("aria-live", "polite"),
      );
      canvas.addEventListener("blur", () =>
        panel.readout.setAttribute("aria-live", "off"),
      );
      canvas.addEventListener("pointermove", (event) => {
        panel.readout.setAttribute("aria-live", "off");
        const bounds = canvas.getBoundingClientRect();
        inspect(
          panel,
          Math.floor(
            ((event.clientX - bounds.left) / bounds.width) * canvas.width,
          ),
          Math.floor(
            ((event.clientY - bounds.top) / bounds.height) * canvas.height,
          ),
        );
      });
      canvas.addEventListener("keydown", (event) => {
        const steps = {
          ArrowLeft: [-1, 0],
          ArrowRight: [1, 0],
          ArrowUp: [0, -1],
          ArrowDown: [0, 1],
        };
        if (steps[event.key]) {
          event.preventDefault();
          panel.readout.setAttribute("aria-live", "polite");
          inspect(
            panel,
            panel.cursor[0] + steps[event.key][0],
            panel.cursor[1] + steps[event.key][1],
          );
        }
      });
      refresh();
    } catch (error) {
      const message = make("p", "field-loading");
      panel.errorText = make("span");
      panel.errorText.textContent = translate().fieldFailure;
      message.setAttribute("role", "alert");
      const retry = make("button", "button");
      panel.retry = retry;
      retry.type = "button";
      retry.textContent = translate().retry;
      retry.addEventListener("click", () => load(panel));
      message.append(panel.errorText, document.createElement("br"), retry);
      panel.box.replaceChildren(message);
    } finally {
      panel.loading = false;
    }
  }
  for (const button of document.querySelectorAll("[data-axis]"))
    button.addEventListener("click", () => {
      axis = button.dataset.axis;
      document
        .querySelectorAll("[data-axis]")
        .forEach((b) => b.setAttribute("aria-pressed", String(b === button)));
      panels.forEach(draw);
    });
  document.querySelector("#slice").addEventListener("input", (event) => {
    position = Number(event.target.value);
    document.querySelector("#slice-value").textContent = `${position}%`;
    panels.forEach(draw);
  });
  document.querySelector("#scale").addEventListener("change", (event) => {
    scale = event.target.value;
    refresh();
  });
  const observer = new IntersectionObserver(
    (entries) => {
      if (entries.some((entry) => entry.isIntersecting)) {
        panels.forEach(load);
        observer.disconnect();
      }
    },
    { rootMargin: "350px" },
  );
  observer.observe(grid);
  refresh();
  return { refresh };
}
