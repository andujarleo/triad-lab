import { atlasURL, themeSelectionState } from "./atlas.js";
const make = (tag, className, text) => {
  const el = document.createElement(tag);
  if (className) el.className = className;
  if (text) el.textContent = text;
  return el;
};
export function createResearch(data, { language, translate, onTheme }) {
  const grid = document.querySelector("#research-grid");
  function refresh() {
    const t = translate(),
      lang = language();
    const fragment = document.createDocumentFragment();
    for (const [index, topic] of data.research.topics.entries()) {
      const row = make("li", "research-topic");
      const number = make(
        "span",
        "topic-number",
        String(index + 1).padStart(2, "0"),
      );
      number.setAttribute("aria-hidden", "true");
      const body = make("div", "topic-body"),
        title = make("h3");
      const headingLink = make("a", "", topic.title[lang] || topic.title.en);
      headingLink.href = `${data.repository}/blob/main/${topic.docs[lang] || topic.docs.en}`;
      title.append(headingLink);
      body.append(
        title,
        make("p", "", topic.summary[lang] || topic.summary.en),
      );
      const actions = make("div", "topic-actions");
      actions.append(
        make(
          "p",
          "topic-counts",
          `${t.sourceCount(topic.source_ids.length)} · ${t.studyCount(topic.study_ids.length)}`,
        ),
      );
      const read = make("a", "text-link", t.openTheme);
      read.href = headingLink.href;
      actions.append(read);
      if (topic.study_ids.length) {
        const related = make("a", "text-link", t.relatedStudies);
        const url = atlasURL(
          location.href,
          themeSelectionState(topic.id, data.research.topics),
          lang,
        );
        url.hash = "atlas";
        related.href = url.href;
        related.addEventListener("click", (event) => {
          if (
            event.button ||
            event.metaKey ||
            event.ctrlKey ||
            event.shiftKey ||
            event.altKey
          )
            return;
          event.preventDefault();
          onTheme(topic.id);
          location.hash = "atlas";
          document.querySelector("#atlas-title").focus({ preventScroll: true });
        });
        actions.append(related);
      } else actions.append(make("p", "topic-context", t.noRelatedStudies));
      row.append(number, body, actions);
      fragment.append(row);
    }
    grid.replaceChildren(fragment);
    grid.setAttribute("aria-busy", "false");
    const status = document.querySelector("#research-status");
    status.textContent = data.research.topics.length ? "" : t.researchEmpty;
    status.hidden = data.research.topics.length > 0;
  }
  refresh();
  return { refresh };
}
