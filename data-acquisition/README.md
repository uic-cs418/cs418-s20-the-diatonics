# Billboard and Spotify Data 

## Data Sources
* Spotify RESTful API (`spotify`)
    * Accessed directly through HTTP requests
* Billboard Top 100 charts (`Billboard`)
    * Accessed via a third-party package, `billboard-top-100`, which scrapes data directly from the Billboard website

---

## Data Dictionary

### Track
| Attribute | Type | Source |Description |
| ---------- | ----- | ------ |---------|
| **spotifyId** | string | `spotify` | A track's unique identifier assigned by Spotify
| **title** | string | `billboard` 
| **artist** | string | `billboard`  
| **duration** | number | `spotify` | The length of the track, in milliseconds
| **danceability** | number | `spotify` | Measure of how suitable the track is for dancing. Ranges from 0 to 1.
| **energy** | number | `spotify` |
| **instrumentalness** | number | `spotify` | 
| **liveness** |
| **loudness** |
| **speechiness** |
| **valence** |
| **tempo** |

### LeaderboardInstance
| Attribute | Type | Source | Description
|-|-|-|-
| **spotifyId** | string | `spotify` | Spotify ID assigned to the track
| **weekOf** | date | `billboard` | First date of the week the leaderboard was released
| **position** | number | `billboard` | A value between 1-100 representing where on the chart the track is 
| **changeSinceLastWeek** | number | `billboard` | Difference between the current week's position and last weeks position.
| **weeksOnChart** | number | `billboard` | The number of consecutive weeks the track has been on the Billboard Top 100 chart
