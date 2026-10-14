# Public Research Notes

This is a public, documentation-only research retrospective. Read README.md and docs/provenance-and-scope.md first.

Never import private Git history, patient data, case identifiers, clinical records, raw model outputs, credentials, private repository links or internal infrastructure details. Re-author public prose and whitelist aggregate metrics only.

Keep metric names and their limitations intact. C1 main results use the strict hidden-ophthalmology-label version; the negative-control source cannot guarantee identical run provenance. A post-hoc sign filter does not rewrite a report.

Before publishing changes, inspect Git status and staged diff; run python3 tools/validate_publication.py, verify source numbers and manually review every changed file. Passing the script does not certify clinical validity or complete anonymization.

Do not add a license, clinical claim or data availability claim without owner authorization and evidence. Update memory/next.md and memory/changelog.md for each maintenance session.
