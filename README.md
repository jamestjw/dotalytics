# Scripts
## hero_stats.py
Gets hero winrate by patch.

## hero_stats_v2.py
Gets winrate of heroes in a certain time interval (the API doesn't state what the time horizon is). Plan is to call this every so often to get a rolling window winrate of sorts.

## match_id.py
Gets match IDs of professional games.

## match_data.py
Gets match data given a list of match IDs.

## patch_data.py
Gets where each patch went live.

# Cloud Functions
## hero-data
Basically just runs hero_stats_v2 and dumps output in a GCS bucket.