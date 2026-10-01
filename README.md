## Collection migration - 1 October 2026

Active collection has moved to the grouped five-curve workflow in [Energy Data Collection](https://github.com/Amir-Torbati/ree-data-platform/blob/main/docs/FUNDAMENTALS.md) (owner access required). It collects verified ESIOS indicators 1295 (actual PV), 551 (actual wind), 1293 (actual demand), 542 (PV forecast) and 541 (wind forecast).

**The files below are a preserved legacy archive, not certified actual-generation data.** The review found source-ID mismatches in the solar/wind collectors and reliability problems in the demand scraper. Current code alone does not establish the origin of every historical file. Do not combine this archive with the corrected curves without checking provenance. Legacy collection/backfill workflows are retired to prevent overlapping or mislabelled downloads. Data files and Git history have not been deleted or relabelled.

---

# Spain-Electricity-Demand-REE-
Spain Hourly Electricity Demand (REE) Collector This project automates the daily extraction of hourly electricity demand data from Spain's Red Eléctrica (REE) platform, building a continuously updated historical database.
