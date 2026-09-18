const validMaterials = ["all", "code", "figures", "data", "notes-only"];
export function readAtlasState(url, data) {
  const params = url.searchParams;
  return {
    query: params.get("q") ?? "",
    area: data.areas.some((a) => a.id === params.get("area"))
      ? params.get("area")
      : "all",
    material: validMaterials.includes(params.get("material"))
      ? params.get("material")
      : "all",
    theme: data.research.topics.some((t) => t.id === params.get("theme"))
      ? params.get("theme")
      : "all",
  };
}
export function themeSelectionState(id, topics) {
  return {
    query: "",
    area: "all",
    material: "all",
    theme: topics.some((t) => t.id === id) ? id : "all",
  };
}
export function atlasURL(current, state, language) {
  const url = new URL(current);
  const values = {
    q: state.query,
    area: state.area,
    material: state.material,
    theme: state.theme,
    lang: language === "en" ? "" : language,
  };
  for (const [key, value] of Object.entries(values)) {
    if (!value || value === "all") url.searchParams.delete(key);
    else url.searchParams.set(key, value);
  }
  return url;
}
const normalize = (value) =>
  String(value ?? "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase();
export function filterStudies(
  studies,
  {
    query = "",
    area = "all",
    material = "all",
    theme = "all",
    topics = [],
  } = {},
) {
  const members =
    theme === "all"
      ? null
      : new Set(topics.find((t) => t.id === theme)?.study_ids ?? []);
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
      (!members || members.has(study.id)) &&
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
    material = document.querySelector("#material"),
    theme = document.querySelector("#theme");
  const more = document.querySelector("#load-more"),
    count = document.querySelector("#results-count");
  const initial = readAtlasState(new URL(location.href), data);
  search.value = initial.query;
  let lastArea = initial.area,
    lastTheme = initial.theme;
  material.value = initial.material;
  area.value = lastArea;
  theme.value = lastTheme;
  function updateOptions() {
    const current = area.value || lastArea;
    area.replaceChildren(
      new Option(translate().allAreas, "all"),
      ...data.areas.map(
        (a) => new Option(a.title[language()] || a.title.en, a.id),
      ),
    );
    area.value = data.areas.some((a) => a.id === current) ? current : lastArea;
    const currentTheme = theme.value || lastTheme;
    theme.replaceChildren(
      new Option(translate().allThemes, "all"),
      ...data.research.topics.map(
        (t) => new Option(t.title[language()] || t.title.en, t.id),
      ),
    );
    theme.value = data.research.topics.some((t) => t.id === currentTheme)
      ? currentTheme
      : "all";
    ["allMaterial", "code", "figures", "data", "notesOnly"].forEach(
      (key, i) => (material.options[i].text = translate()[key]),
    );
  }
  function render() {
    const lang = language(),
      t = translate();
    lastArea = area.value;
    lastTheme = theme.value;
    const matches = filterStudies(data.studies, {
      query: search.value,
      area: area.value,
      material: material.value,
      theme: theme.value,
      topics: data.research.topics,
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
      const audit = make("details", "study-audit");
      audit.dataset.status = study.rule_audit.status;
      audit.append(make("summary", "", t.auditLabels[study.rule_audit.status]));
      audit.append(
        make(
          "p",
          "",
          study.rule_audit.summary[lang] || study.rule_audit.summary.en,
        ),
      );
      const report = make("a", "", t.auditReport);
      report.href = `${data.repository}/blob/main/${study.rule_audit.report[lang] || study.rule_audit.report.en}#study-${encodeURIComponent(study.id)}`;
      audit.append(report);
      card.append(picture, meta, title, summary, audit, foot);
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
      theme: theme.value,
    });
  }
  function reset() {
    search.value = "";
    area.value = "all";
    lastArea = "all";
    material.value = "all";
    theme.value = "all";
    lastTheme = "all";
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
  function selectTheme(id) {
    const next = themeSelectionState(id, data.research.topics);
    search.value = next.query;
    area.value = lastArea = next.area;
    material.value = next.material;
    theme.value = lastTheme = next.theme;
    limit = 12;
    render();
  }
  theme.addEventListener("change", () => selectTheme(theme.value));
  more.addEventListener("click", () => {
    limit += 12;
    render();
  });
  document.querySelector("#clear-empty").addEventListener("click", reset);
  updateOptions();
  render();
  return {
    selectTheme,
    refresh() {
      updateOptions();
      render();
    },
  };
}
