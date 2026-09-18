const normalize = (value) =>
  String(value ?? "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase();
export function filterStudies(
  studies,
  { query = "", area = "all", material = "all" } = {},
) {
  const words = normalize(query).trim().split(/\s+/).filter(Boolean);
  return studies.filter((study) => {
    const text = normalize(
      [
        Object.values(study.title ?? {}),
        Object.values(study.question ?? {}),
        Object.values(study.summary ?? {}),
        study.series,
      ]
        .flat()
        .join(" "),
    );
    const available = study.availability ?? {};
    const matchesMaterial =
      material === "all" ||
      (material === "notes-only"
        ? available.notes &&
          !available.code &&
          !available.data &&
          !available.figures
        : available[material]);
    return (
      (area === "all" || study.series === area) &&
      matchesMaterial &&
      words.every((word) => text.includes(word))
    );
  });
}
const make = (tag, className, text) => {
  const el = document.createElement(tag);
  if (className) el.className = className;
  if (text) el.textContent = text;
  return el;
};
export function createAtlas(data, { language, translate, onState }) {
  let limit = 12;
  const grid = document.querySelector("#study-grid"),
    form = document.querySelector("#atlas-form");
  const search = document.querySelector("#search"),
    area = document.querySelector("#area"),
    material = document.querySelector("#material");
  const more = document.querySelector("#load-more"),
    count = document.querySelector("#results-count");
  const url = new URL(location.href);
  search.value = url.searchParams.get("q") ?? "";
  const initialArea = url.searchParams.get("area");
  let lastArea = data.areas.some((a) => a.id === initialArea)
    ? initialArea
    : "all";
  area.value = lastArea;
  const validMaterials = ["all", "code", "figures", "data", "notes-only"];
  material.value = validMaterials.includes(url.searchParams.get("material"))
    ? url.searchParams.get("material")
    : "all";
  function updateOptions() {
    const current = area.value || lastArea;
    area.replaceChildren(
      new Option(translate().allAreas, "all"),
      ...data.areas.map(
        (a) => new Option(a.title[language()] || a.title.en, a.id),
      ),
    );
    area.value = data.areas.some((a) => a.id === current) ? current : lastArea;
    ["allMaterial", "code", "figures", "data", "notesOnly"].forEach(
      (key, i) => (material.options[i].text = translate()[key]),
    );
  }
  function render() {
    const lang = language(),
      t = translate();
    lastArea = area.value;
    const matches = filterStudies(data.studies, {
      query: search.value,
      area: area.value,
      material: material.value,
    });
    const shown = matches.slice(0, limit),
      fragment = document.createDocumentFragment();
    for (const study of shown) {
      const card = make("article", "study-card");
      const path = study.docs[lang] || study.docs.en;
      const href = `${data.repository}/blob/main/${path}`;
      const picture = make("a", "study-image");
      picture.href = href;
      if (study.image) {
        const img = make("img");
        img.src = study.image;
        img.alt = study.title[lang] || study.title.en;
        img.loading = "lazy";
        img.width = 640;
        img.height = 400;
        picture.append(img);
      } else picture.append(make("span", "study-no-image", t.noFigure));
      const meta = make("div", "study-meta");
      const series = data.areas.find((a) => a.id === study.series);
      meta.append(
        make("span", "", series?.title[lang] || study.series),
        make("span", "", study.status === "recorded" ? t.recorded : t.archival),
      );
      const title = make("h3"),
        link = make(
          "a",
          "",
          study.question[lang] || study.title[lang] || study.title.en,
        );
      link.href = href;
      title.append(link);
      const summary = make("p", "", study.summary[lang] || study.summary.en);
      const availability = Object.entries(study.availability)
        .filter(([, present]) => present)
        .map(([key]) => t[key] || key)
        .join(" · ");
      const foot = make("p", "study-material", availability);
      const source = make("a", "", t.openStudy);
      source.href = href;
      foot.append(source);
      card.append(picture, meta, title, summary, foot);
      fragment.append(card);
    }
    grid.replaceChildren(fragment);
    grid.setAttribute("aria-busy", "false");
    count.textContent = t.results(shown.length, matches.length);
    more.hidden = matches.length <= limit;
    document.querySelector("#empty-state").hidden = matches.length !== 0;
    onState({
      q: search.value.trim(),
      area: area.value,
      material: material.value,
    });
  }
  function reset() {
    search.value = "";
    area.value = "all";
    lastArea = "all";
    material.value = "all";
    limit = 12;
    render();
  }
  form.addEventListener("submit", (event) => event.preventDefault());
  form.addEventListener("reset", (event) => {
    event.preventDefault();
    reset();
  });
  let debounce;
  search.addEventListener("input", () => {
    clearTimeout(debounce);
    debounce = setTimeout(() => {
      limit = 12;
      render();
    }, 100);
  });
  for (const input of [area, material])
    input.addEventListener("change", () => {
      limit = 12;
      render();
    });
  more.addEventListener("click", () => {
    limit += 12;
    render();
  });
  document.querySelector("#clear-empty").addEventListener("click", reset);
  updateOptions();
  render();
  return {
    refresh() {
      updateOptions();
      render();
    },
  };
}
