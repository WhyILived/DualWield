# TwelveLabs Gameplay Downtime Analysis Report

## Overview

This report summarizes the results of analyzing gameplay downtime events in three popular games: **Valorant**, **League of Legends**, and **CS:GO**. The analysis was performed using a custom Python script leveraging the TwelveLabs Analyze API with a specialized prompt to detect periods of inactivity, death screens, respawn waits, and related events.

## Approach

- Developed a Python script `./analyze.py` to interface with the TwelveLabs API.
- The script uploads videos, checks for existing indexes, and runs a detailed prompt to extract downtime segments.
- The prompt was designed to generalize across different games, starting from Valorant and extending to League of Legends and CS:GO.

## Videos Used

- [Valorant](https://www.youtube.com/watch?v=Wrdh5HrOCMc)
- [League of Legends](https://www.youtube.com/watch?v=KnpljMWwy3o)
- [CS:GO](https://www.youtube.com/watch?v=p4QG59y6FGE)

## Prompt

```text
Analyze this video for gameplay downtime events. Specifically:

Identify and return all time segments where the player is:
- Eliminated / killed / dies
- In a "death screen", spectator mode, or report screen
- Waiting to respawn
- Viewing death summaries or kill cam

For each death/downtime event:
- Return the start and end timestamps
- Include any visible text such as: "report", "you are dead", "respawning in"
- Indicate if the screen has a grayscale effect, red tint, or other visual indicator

Identify loading screens, including:
- Matchmaking wait screens
- Round transitions or pre-game loadouts
- Black screens with logos or rotating animations

Identify and return:
- Periods of visual inactivity (no player motion, HUD only, waiting states)
- UI overlays that indicate player is not active (e.g., menus, scoreboards)

For each segment, return:
- The timestamp
- The reason (e.g., "death", "loading", "idle", "respawn wait")
- Any visible keywords or UI elements
- If possible, extract a thumbnail image or text snapshot from that frame
```

## Results

### Valorant

- **Death / Combat Report:** Multiple segments detected with timestamps, visible "combat report" text, and red tint indicators.
- **Loading Screens:** Detected at video start and end, with logo animations and explosions.
- **Idle / Buy Phase:** Several periods identified where the player is in the buy menu, selecting weapons and abilities.
- **Idle / Countdown Timer:** Player stands still during countdowns.
- **Summary:** The model accurately captured deaths, idle phases, and transitions, with detailed timestamps and UI elements.

#### Fetched results:
```
🔹 Summary:
- **Timestamp:** [145s (02:25) ~ 149s (02:29)]
  - **Reason:** Death / Combat Report
  - **Visible Text:** "combat report"
  - **Visual Indicator:** Red tint
  - **Description:** The player is eliminated, and the screen displays a combat report with a red tint.

- **Timestamp:** [370s (06:10) ~ 376s (06:16)]
  - **Reason:** Death / Combat Report
  - **Visible Text:** "combat report"
  - **Visual Indicator:** No grayscale effect or red tint
  - **Description:** The player is eliminated, and the screen displays a combat report.

- **Timestamp:** [1102s (18:22) ~ 1110s (18:30)]
  - **Reason:** Death / Combat Report
  - **Visible Text:** "combat report"
  - **Visual Indicator:** No grayscale effect or red tint
  - **Description:** The player is eliminated, and the screen displays a combat report.

- **Timestamp:** [1422s (23:42) ~ 1424s (23:44)]
  - **Reason:** Loading Screen
  - **Visible Text:** None
  - **Visual Indicator:** Small explosion
  - **Description:** The video ends with a small explosion, indicating a loading screen or transition.

- **Timestamp:** [0s (00:00) ~ 8s (00:08)]
  - **Reason:** Loading Screen
  - **Visible Text:** "KRONOSGAMES" logo animation
  - **Visual Indicator:** Black screen
  - **Description:** The video starts with a black screen displaying the "KRONOSGAMES" logo animation.

- **Timestamp:** [14s (00:14) ~ 20s (00:20)]
  - **Reason:** Idle / Countdown Timer
  - **Visible Text:** Countdown timer (75 seconds)
  - **Visual Indicator:** No player motion
  - **Description:** The player character stands still as the countdown timer ticks down from 75 seconds.

- **Timestamp:** [146s (02:26) ~ 149s (02:29)]
  - **Reason:** Idle / Combat Report
  - **Visible Text:** "combat report"
  - **Visual Indicator:** No grayscale effect or red tint
  - **Description:** The player is in a combat report screen after being eliminated.

- **Timestamp:** [376s (06:16) ~ 384s (06:24)]
  - **Reason:** Idle / Buy Phase
  - **Visible Text:** Buy menu options (Phantom, Vandal, Bulldog, Sheriff, Classic, Ghost, R-635, M4 Carbine, MP7, Frenzy, Guardian, Operator)
  - **Visual Indicator:** No player motion
  - **Description:** The player is in the buy phase, selecting weapons and equipment.

- **Timestamp:** [1114s (18:34) ~ 1127s (18:47)]
  - **Reason:** Idle / Buy Phase
  - **Visible Text:** Buy menu options (sniper rifles, SMGs, assault rifles, pistols, heavy guns, abilities like full scan and kill vision)
  - **Visual Indicator:** No player motion
  - **Description:** The player is in the buy phase, selecting weapons and abilities.

- **Timestamp:** [1401s (23:21) ~ 1423s (23:43)]
  - **Reason:** Idle / Buy Phase
  - **Visible Text:** Buy menu options (sniper rifles, SMGs, assault rifles, pistols, heavy guns, abilities like full scan and kill vision)
  - **Visual Indicator:** No player motion
  - **Description:** The player is in the buy phase, selecting weapons and abilities.

These segments cover the downtime events, including deaths, combat reports, respawns, and idle periods where the player is not actively engaged in gameplay.

```

### League of Legends

- **Eliminated / Death:** Multiple segments with "You have been executed" text and grayscale/red tint effects.
- **Respawning:** Detected when the player moves back to base.
- **Death Summaries / Kill Cam:** Identified with shop interface overlays.
- **Summary:** Downtime events primarily revolve around player deaths and respawns. No significant loading screens or extended inactivity detected.

#### Fetched results:
```
Here is the analysis of the video for gameplay downtime events:

Timestamp: 65s (01:05) - 80s (01:20)

Event: Eliminated / killed / dies
Visible Text: "You have been executed"
Visual Indicator: Grayscale effect
Timestamp: 311s (05:11) - 354s (05:54)

Event: Eliminated / killed / dies
Visible Text: "You have been executed"
Visual Indicator: Grayscale effect
Timestamp: 631s (10:31) - 642s (10:42)

Event: Eliminated / killed / dies
Visible Text: "You have been executed"
Visual Indicator: Grayscale effect, red tint
Timestamp: 730s (12:10) - 748s (12:28)

Event: Eliminated / killed / dies
Visible Text: "You have been executed"
Visual Indicator: Grayscale effect
Timestamp: 950s (15:50) - 962s (16:02)

Event: Respawning
Visible Text: None
Visual Indicator: Player moves back to base
Timestamp: 1076s (17:56) - 1080s (18:00)

Event: Viewing death summaries or kill cam
Visible Text: "An ally has been slain"
Visual Indicator: Shop interface
There are no identified loading screens or periods of visual inactivity with no player motion or HUD-only waiting states. The video primarily focuses on gameplay and combat sequences, with the downtime events primarily revolving around the player's death and respawn.



```
### CS:GO

- **Downtime Events:** Several death screens, combat reports, and buy phases detected.
- **Visual Inactivity:** Multiple periods with no player motion and HUD-only states.
- **Loading Screens:** Brief loading/voting screens identified.
- **Note:** The CS:GO video had fewer death events (player did not die often), but the model successfully extracted periods of inactivity and buy phases that can be utilized for further analysis.

#### Fetched results:
```
The player experiences several downtime events throughout the video, which are detailed as follows:

Eliminated / Death Screen (46s - 50s):

Start Timestamp: 46s
End Timestamp: 50s
Visible Text: "Terrorists Win"
Visual Indicator: Red crosshair and message indicating the player's team lost.
Combat Report Screen (50s - 55s):

Start Timestamp: 50s
End Timestamp: 55s
Visible Text: "Combat Report"
Visual Indicator: Statistics and scores displayed.
Waiting to Respawn (55s - 60s):

Start Timestamp: 55s
End Timestamp: 60s
Visible Text: "Buy Time Remaining"
Visual Indicator: Buy menu with options to purchase weapons and equipment.
Eliminated / Death Screen (157s - 164s):

Start Timestamp: 157s
End Timestamp: 164s
Visible Text: "Terrorists Win"
Visual Indicator: Grayscale effect.
Combat Report Screen (164s - 171s):

Start Timestamp: 164s
End Timestamp: 171s
Visible Text: "Buy Time Remaining"
Visual Indicator: Buy menu overlay.
Eliminated / Death Screen (271s - 276s):

Start Timestamp: 271s
End Timestamp: 276s
Visible Text: "Terrorists Win"
Visual Indicator: Grayscale effect.
Combat Report Screen (276s - 280s):

Start Timestamp: 276s
End Timestamp: 280s
Visible Text: "Buy Time Remaining"
Visual Indicator: Buy menu overlay.
Loading Screen (280s - 281s):

Start Timestamp: 280s
End Timestamp: 281s
Visible Text: "Vote for eminems"
Visual Indicator: Buy menu overlay.
Eliminated / Death Screen (370s - 376s):

Start Timestamp: 370s
End Timestamp: 376s
Visible Text: "Terrorist Wins"
Visual Indicator: Grayscale effect.
Eliminated / Death Screen (385s - 392s):

Start Timestamp: 385s
End Timestamp: 392s
Visible Text: "Terrorist Wins"
Visual Indicator: Grayscale effect.
Eliminated / Death Screen (468s - 470s):

Start Timestamp: 468s
End Timestamp: 470s
Visible Text: "Terrorist Wins"
Visual Indicator: Grayscale effect.
Periods of visual inactivity and UI overlays indicating player is not active are also noted:

Visual Inactivity (15s - 20s):

Start Timestamp: 15s
End Timestamp: 20s
Reason: No player motion, HUD only.
Visual Inactivity (38s - 46s):

Start Timestamp: 38s
End Timestamp: 46s
Reason: No player motion, HUD only.
Visual Inactivity (146s - 156s):

Start Timestamp: 146s
End Timestamp: 156s
Reason: No player motion, HUD only.
These segments cover all downtime events and periods of visual inactivity, with detailed timestamps, visible text, and visual indicators.


```

## Example Code

```python
import os
from typing import Optional
from datetime import datetime
from twelvelabs import TwelveLabs
from twelvelabs.models.task import Task

API_KEY = ""
ENGINE = "pegasus1.2"
LANGUAGE = "en"
INDEX_NAME = "chatgpt_index"

client = TwelveLabs(api_key=API_KEY)
prompt = """Analyze this video for gameplay downtime events. Specifically:
... (see above for full prompt) ...
"""

def get_or_create_index(index_name: str):
    for index in client.index.list():
        if index.name == index_name:
            return index
    return client.index.create(
        name=index_name,
        models=[{"name": ENGINE, "options": ["visual", "audio"]}]
    )

def get_existing_video_id(index_id: str, filename: str) -> Optional[str]:
    tasks = client.task.list(index_id=index_id)
    base_filename = os.path.basename(filename)
    matching_tasks = [
        task for task in tasks
        if task.status == "ready" and task.system_metadata
        and os.path.basename(task.system_metadata.get("filename", "")) == base_filename
    ]
    if matching_tasks:
        matching_tasks.sort(key=lambda t: datetime.fromisoformat(t.created_at.rstrip("Z")))
        latest_task = matching_tasks[-1]
        return latest_task.video_id
    return None

def analyze_video(file_path: str) -> str:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Video file not found: {file_path}")
    index = get_or_create_index(INDEX_NAME)
    video_id = get_existing_video_id(index.id, file_path)
    if not video_id:
        task = client.task.create(index_id=index.id, file=file_path)
        task.wait_for_done()
        if task.status != "ready":
            raise RuntimeError(f"Indexing failed (status: {task.status})")
        video_id = task.video_id
    res_summary = client.analyze(video_id=video_id, prompt=prompt)
    summary_text = f"\nSummary:\n{res_summary.data}"
    return summary_text

print(analyze_video("./videos/VALORANT.mp4"))
```

## Conclusion

- The TwelveLabs API, combined with a tailored prompt, effectively identifies gameplay downtime events across different games.
- The approach generalizes well, with accurate detection of deaths, idle phases, and loading screens.
- Even in videos with few deaths (e.g., CS:GO), the model extracts useful periods of inactivity and UI overlays.
- These results can be further utilized for gameplay analytics, highlight generation, or player behavior studies.
