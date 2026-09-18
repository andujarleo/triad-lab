import test from "node:test";
import assert from "node:assert/strict";
import {
  filterStudies,
  readAtlasState,
  themeSelectionState,
  atlasURL,
} from "../web/atlas.js";
import { planeAt, colorFraction } from "../web/field.js";
const studies = [
  {
    id: "record-memory",
    series: "memory",
    title: { en: "Memory", "pt-BR": "Memória" },
    question: { en: "Can history persist?" },
    summary: { en: "A saved record" },
    availability: { code: true, data: true, figures: false },
  },
  {
    id: "record-signal",
    series: "signals",
    title: { en: "Signal" },
    question: {},
    summary: { en: "Memory in motion" },
    availability: { code: false, data: false, figures: false, notes: true },
  },
];
test("search combines bilingual text, accent normalization, area and material", () => {
  assert.equal(
    filterStudies(studies, {
      query: "memoria",
      area: "memory",
      material: "code",
    }).length,
    1,
  );
  assert.equal(
    filterStudies(studies, {
      query: "memory",
      area: "signals",
      material: "notes-only",
    }).length,
    1,
  );
  assert.equal(
    filterStudies(studies, {
      query: "memory",
      area: "signals",
      material: "data",
    }).length,
    0,
  );
});
test("empty query returns all entries and multiword search requires every word", () => {
  assert.equal(filterStudies(studies, {}).length, 2);
  assert.equal(filterStudies(studies, { query: "memory saved" }).length, 1);
});
const field = {
  shape: [2, 3, 4],
  values: Array.from({ length: 24 }, (_, i) => i),
  min: 0,
  max: 23,
};
test("recorded volume coordinates survive all cutting planes", () => {
  assert.deepEqual(planeAt(field, "z", 100).cells, [3, 15, 7, 19, 11, 23]);
  assert.deepEqual(
    planeAt(field, "x", 0).cells,
    [0, 4, 8, 1, 5, 9, 2, 6, 10, 3, 7, 11],
  );
  assert.deepEqual(
    planeAt(field, "y", 100).cells,
    [8, 20, 9, 21, 10, 22, 11, 23],
  );
});
test("relative slice endpoints stay inside each grid", () => {
  assert.equal(planeAt(field, "x", 100).index, 1);
  assert.equal(planeAt(field, "y", 0).index, 0);
  assert.equal(planeAt(field, "z", 50).index, 2);
});
test("display scaling keeps endpoints and handles a constant field", () => {
  for (const scale of ["linear", "log"]) {
    assert.equal(colorFraction(0, 0, 23, scale), 0);
    assert.equal(colorFraction(23, 0, 23, scale), 1);
    assert.equal(colorFraction(2, 2, 2, scale), 0);
  }
  assert.ok(colorFraction(3, 0, 23, "log") > colorFraction(3, 0, 23, "linear"));
});
test("logarithmic scale allocates equal distances to equal density ratios", () => {
  assert.ok(Math.abs(colorFraction(1, 0.01, 100, "log") - 0.5) < 1e-12);
});

const topics = [
  { id: "memory-thread", study_ids: ["record-signal"] },
  { id: "context", study_ids: [] },
];
test("topic membership is explicit and combines with existing filters", () => {
  assert.deepEqual(
    filterStudies(studies, { theme: "memory-thread", topics }).map((s) => s.id),
    ["record-signal"],
  );
  assert.equal(
    filterStudies(studies, { theme: "memory-thread", topics, material: "code" })
      .length,
    0,
  );
  assert.equal(filterStudies(studies, { theme: "context", topics }).length, 0);
  assert.equal(filterStudies(studies, {}).length, 2);
});
test("existing URLs retain filters and new topic choices clear conflicting state", () => {
  const url = new URL(
    "https://example.test/?lang=pt-BR&q=memoria&area=memory&material=code#atlas",
  );
  const data = { areas: [{ id: "memory" }], research: { topics } };
  assert.deepEqual(readAtlasState(url, data), {
    query: "memoria",
    area: "memory",
    material: "code",
    theme: "all",
  });
  const chosen = themeSelectionState("memory-thread", topics);
  assert.deepEqual(chosen, {
    query: "",
    area: "all",
    material: "all",
    theme: "memory-thread",
  });
  const next = atlasURL(url, chosen, "pt-BR");
  assert.equal(next.search, "?lang=pt-BR&theme=memory-thread");
  assert.equal(next.hash, "#atlas");
  assert.equal(atlasURL(next, chosen, "en").search, "?theme=memory-thread");
  assert.equal(
    readAtlasState(
      new URL("https://example.test/?theme=unknown&area=bad"),
      data,
    ).theme,
    "all",
  );
});
