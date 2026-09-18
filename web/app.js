import { copy, concepts } from "./content.js";
import { createAtlas } from "./atlas.js";
import { createResearch } from "./research.js";
import { createFieldViewer } from "./field.js";
const repo = "https://github.com/andujarleo/triad-lab";
const initialURL = new URL(location.href);
let lang = initialURL.searchParams.get("lang") === "pt-BR" ? "pt-BR" : "en";
let conceptIndex = 0,
  atlas,
  research,
  viewer;
const language = () => lang,
  translate = () => copy[lang];
function writeURL(state = {}) {
  const url = new URL(location.href);
  if (lang === "en") url.searchParams.delete("lang");
  else url.searchParams.set("lang", lang);
  for (const [key, value] of Object.entries(state)) {
    if (!value || value === "all") url.searchParams.delete(key);
    else url.searchParams.set(key, value);
  }
  history.replaceState(null, "", url);
}
function showConcept(index, focus = false) {
  conceptIndex = index;
  document.querySelectorAll("[data-concept]").forEach((button, i) => {
    button.setAttribute("aria-selected", String(i === index));
    button.tabIndex = i === index ? 0 : -1;
  });
  const [title, text] = concepts[lang][index];
  document.querySelector("#concept-title").textContent = title;
  document.querySelector("#concept-copy").textContent = text;
  document
    .querySelector("#concept-panel")
    .setAttribute("aria-labelledby", `concept-${index}`);
  if (focus) document.querySelector(`#concept-${index}`).focus();
}
function renderConcepts() {
  const tabs = document.querySelector("#concept-tabs");
  tabs.replaceChildren();
  concepts[lang].forEach(([title], index) => {
    const button = document.createElement("button");
    button.type = "button";
    button.id = `concept-${index}`;
    button.dataset.concept = index;
    button.setAttribute("role", "tab");
    button.setAttribute("aria-controls", "concept-panel");
    button.textContent = title;
    button.addEventListener("click", () => showConcept(index));
    button.addEventListener("keydown", (event) => {
      let next = index;
      if (event.key === "ArrowRight")
        next = (index + 1) % concepts[lang].length;
      else if (event.key === "ArrowLeft")
        next = (index - 1 + concepts[lang].length) % concepts[lang].length;
      else if (event.key === "Home") next = 0;
      else if (event.key === "End") next = concepts[lang].length - 1;
      else return;
      event.preventDefault();
      showConcept(next, true);
    });
    tabs.append(button);
  });
  showConcept(conceptIndex);
}
function renderLanguage() {
  const t = translate();
  document.documentElement.lang = lang;
  document.title = t.pageTitle;
  document.querySelector('meta[name="description"]').content =
    t.pageDescription;
  document.querySelector('meta[property="og:title"]').content = t.pageTitle;
  document.querySelector('meta[property="og:description"]').content =
    t.pageDescription;
  document.querySelectorAll("[data-i18n]").forEach((element) => {
    const value = t[element.dataset.i18n];
    if (typeof value === "string") element.textContent = value;
  });
  document.querySelectorAll("[data-i18n-aria]").forEach((element) => {
    const value = t[element.dataset.i18nAria];
    if (typeof value === "string") element.setAttribute("aria-label", value);
  });
  document
    .querySelectorAll("[data-lang]")
    .forEach((button) =>
      button.setAttribute("aria-pressed", String(button.dataset.lang === lang)),
    );
  document.querySelector("#search").placeholder = t.searchPlaceholder;
  document.querySelector("#hero-image").alt = t.identityAlt;
  for (const [id, key] of [
    ["phase-image", "phaseAlt"],
    ["contraction-image", "contractionAlt"],
    ["long-trajectory-image", "longAlt"],
  ])
    document.querySelector(`#${id}`).alt = t[key];
  document.querySelector('meta[property="og:image"]').content =
    `https://andujarleo.github.io/triad-lab/brand/readme-cover.${lang}.png`;
  document
    .querySelector(".site-header nav")
    .setAttribute(
      "aria-label",
      lang === "en" ? "Main navigation" : "Navegação principal",
    );
  document
    .querySelector("#concept-tabs")
    .setAttribute("aria-label", lang === "en" ? "Concepts" : "Conceitos");
  const languageFolder = lang === "en" ? "en" : "pt-BR",
    readme = lang === "en" ? "README.md" : "README.pt-BR.md";
  document
    .querySelectorAll("[data-doc]")
    .forEach(
      (link) => (link.href = `${repo}/blob/main/${link.dataset.doc}/${readme}`),
    );
  document
    .querySelectorAll("[data-guide]")
    .forEach(
      (link) =>
        (link.href = `${repo}/blob/main/docs/${languageFolder}/${link.dataset.guide}.md`),
    );
  document
    .querySelectorAll("[data-reference]")
    .forEach(
      (link) => (link.href = `${repo}/blob/main/${link.dataset.reference}`),
    );
  renderConcepts();
  atlas?.refresh();
  research?.refresh();
  viewer?.refresh();
  if (!document.querySelector("#catalog-error").hidden) {
    document.querySelector("#results-count").textContent = "";
  }
  writeURL();
}
for (const button of document.querySelectorAll("[data-lang]"))
  button.addEventListener("click", () => {
    lang = button.dataset.lang;
    renderLanguage();
  });
renderLanguage();
try {
  const response = await fetch("data/site.json");
  if (!response.ok) throw new Error("Archive unavailable");
  const data = await response.json();
  if (
    data.format !== 1 ||
    !Array.isArray(data.studies) ||
    !Array.isArray(data.areas) ||
    !Array.isArray(data.fields) ||
    !Array.isArray(data.research?.topics) ||
    !Array.isArray(data.research?.sources)
  )
    throw new Error("Invalid archive");
  document.querySelector("#hero-image").src = data.brand.symbol;
  document.querySelector("#phase-image").src = data.hero;
  document.querySelector("#contraction-image").src =
    data.spotlights.contraction;
  document.querySelector("#long-trajectory-image").src =
    data.spotlights.longTrajectory;
  document.querySelector("#study-total").textContent = data.studies.length;
  document.querySelector("#area-total").textContent = String(
    data.areas.length,
  ).padStart(2, "0");
  document.querySelector("#theme-total").textContent = String(
    data.research.topics.length,
  ).padStart(2, "0");
  atlas = createAtlas(data, { language, translate, onState: writeURL });
  research = createResearch(data, {
    language,
    translate,
    onTheme: (id) => atlas.selectTheme(id),
  });
  viewer = createFieldViewer(data.fields, {
    language,
    translate,
    repository: repo,
  });
} catch (error) {
  const message = document.querySelector("#catalog-error");
  message.hidden = false;
  message.textContent = translate().loadError;
  const researchStatus = document.querySelector("#research-status");
  researchStatus.dataset.i18n = "researchError";
  researchStatus.textContent = translate().researchError;
  researchStatus.hidden = false;
  document.querySelector("#research-grid").setAttribute("aria-busy", "false");
  document.querySelector("#results-count").textContent = "";
  document.querySelector("#study-grid").setAttribute("aria-busy", "false");
}
