[Lab](../../README.md) · **English** · [Português](../pt-BR/research-guide.md)

# Inspect the experiment behind the figure

Begin with [TRIAD’s proposal and operational reading](triad.md). This research presents itself as nonstandard quantum physics; the historical diagnostics need that context.

Start with a study’s question and **FILES.md**, then follow protocol → configuration → source → recorded output → interpretation. The [JSON catalog](../../experiments/catalog.json) lists all 65 studies, their bilingual pages and every associated source payload.

## What the record can establish

The repository preserves numerical source code and data by SHA-256. Source documents have only link syntax normalized, with reversible patches. This establishes continuity of the supplied record. It does not establish that all historical executions can be replayed on a new machine.

The initial lab scripts have a [local execution guide](getting-started.md). Later material includes Apple MLX, partial TriadLang infrastructure, absolute paths and missing inputs. Read the [dependency audit](../../provenance/t-archive/dependencies.md) before choosing a runtime. No original environment lockfile was recovered.

## Comparisons that need care

- **Three 3D implementations:** `bravais_puro_3d.py` has three distinct content hashes. They remain separate under the [field study](../../experiments/geometry/field-3d/FILES.md); a hash identifier does not imply a newer or better version.
- **Saved states differ:** the initial `final_state.npz` has no `psi_f`; another archived state includes it. Phase-based post-processing depends on that field.
- **Random initialization:** the initial 3D and sweep scripts have no fixed seed by default. Their saved records should not be described as exactly replayable from defaults.
- **QM outcomes:** Q01, Q01b, Q02, Q03 and Q04 retain their historical INCONCLUSIVE classifications. Q04 has a recorded protocol deviation. Q00’s declared canonical hash differs from the supplied canonical document; the discrepancy is retained.
- **Negative diagnostics:** T19, T21 and T25 retain their failed diagnostics. T23 includes disagreeing radius diagnostics. These are part of the evidence.
- **Shared bytes:** deduplicated arrays or configs may be associated with different runs. Byte identity alone does not merge those runs or their interpretations.

## Verify and extend

```sh
git lfs pull
python3 tools/check_repository.py
```

The check validates preserved payloads, document transformations, catalog associations and local links. It does not execute historical scripts. Record any path, dependency, equation or parameter adaptation as a separate change, and publish its outputs as a new run.

[Chronology](topics/timeline.md) · [Source inspection](../../provenance/t-archive/inspection.json) · [Preservation policy](../../provenance/README.md) · [New study template](../../templates/experiment/README.md)

[Fundamentos / Foundations](topics/foundations.md)
