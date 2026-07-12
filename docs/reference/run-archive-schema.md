# Run archive replay contract

Each pipeline run is stored under `.cache/run_archives/<run_id>/`.

## Layout (schema v2)

| File | Required for replay | Version field |
|------|---------------------|---------------|
| `manifest.json` | yes | `schema_version` |
| `report.json` | yes | contract in manifest |
| `enriched/{tf}.json` | yes | artifact envelope |
| `analyses.json` | no (rebuilt fallback) | artifact envelope |
| `fetch.json` | no | artifact envelope |
| `meta.json` | no (legacy index) | deprecated index |

## Versioning rules

1. **`schema_version`** (manifest): bump when folder layout or manifest shape changes. Add a migration in `src/run/archive/compat.py`.
2. **`artifact_version`** (per file envelope): bump when fetch/frame/analysis payload shape changes independently.
3. **`report_contract_version`** (manifest.replay): bump when required report top-level keys change. Reader fills defaults via `normalize_report()`.

## Reader behaviour

- Missing `manifest.json` → synthesize from legacy v1 (`meta.json` only) and optionally write upgraded manifest.
- Unknown JSON fields → preserved (never strip).
- Missing report keys → defaults + `archive_replay_warnings` on replay.
- Schema newer than reader → **incompatible** (block load).
- Schema older / partial artifacts → **degraded** (load with warnings).

## Producer

New runs write artifacts first, then `manifest.json` last with `summary.pipeline_status: complete`.
Only runs whose `meta.generation_steps` are all terminal (`done` / `skipped` / `error`) are archived and replayable.
Interrupted writes without a final manifest are not listed for replay.

See `src/run/archive/schema.py` and `src/run/archive/completion.py`.

## Changing this contract

1. Bump the appropriate version constant.
2. Implement `migrate_*` for the artifact or manifest.
3. Add a unit test with a frozen legacy folder under `tests/fixtures/run_archives/`.
4. Document the change in this file.
