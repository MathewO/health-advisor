# iOS Shortcut: Auto-Log Workouts to Health Logger

This guide walks you through creating two iOS Shortcuts — one for **Running**, one for **Stair Climbing** — that automatically log workout data to your GitHub-backed phone log whenever you finish a session on your Apple Watch.

When you end a workout on your watch, a notification appears on your iPhone. Tap it, confirm once, and the log entry is written to GitHub within seconds.

---

## Prerequisites

- iPhone with Shortcuts app (iOS 16+)
- Apple Watch with workouts tracked in the Health app
- Your GitHub Personal Access Token (same one in the Health Logger app settings)
- Your GitHub username and repo name (e.g. `mathew-ohalloran` / `health-advisor`)

---

## Log Entry Formats

**Run:**
```
YYYY-MM-DD | run | 15.0 min | 2.32 km | 176 kcal | 162 bpm
```

**Stair Climbing:**
```
YYYY-MM-DD | stair | 25.0 min | 230 kcal | 145 bpm
```

---

## Shortcut 1: Log Run

### Create the Shortcut

1. Open **Shortcuts** app → tap **+** to create a new shortcut
2. Tap the shortcut name at the top and rename it to **"Log Run"**

### Add these actions in order:

---

**Action 1 — Find Health Samples**

- Search for action: `Find Health Samples`
- **Type:** Workouts
- **Filter:** Workout Type is Running
- **Sort:** Start Date — Latest First
- **Limit:** 1

---

**Action 2 — Get Details of Health Sample**

- Search for action: `Get Details of Health Sample`
- **Detail:** Start Date
- Set variable: name it `workoutStart`

---

**Action 3 — Get Details of Health Sample** *(repeat, different detail)*

- Same action again
- **Detail:** Duration
- Set variable: name it `workoutDuration`
- *(Duration is returned in seconds — we'll convert below)*

---

**Action 4 — Get Details of Health Sample**

- **Detail:** Total Distance
- Set variable: name it `workoutDistance`
- *(Value is in metres — we'll convert below)*

---

**Action 5 — Get Details of Health Sample**

- **Detail:** Total Energy Burned
- Set variable: name it `workoutKcal`

---

**Action 6 — Calculate**

This converts duration from seconds to minutes (rounded to 1 decimal):

- Search for action: `Calculate`
- Expression: `workoutDuration / 60`
- Round result to **1 decimal place** (use a `Round Number` action after if needed, or use `Format Number` with 1 decimal)
- Set result variable: `durationMins`

---

**Action 7 — Calculate** *(distance: metres to km)*

- Expression: `workoutDistance / 1000`
- Round to **2 decimal places**
- Set variable: `distanceKm`

---

**Action 8 — Format Date**

- **Date:** `workoutStart`
- **Format:** Custom — `yyyy-MM-dd`
- Set variable: `logDate`

---

**Action 9 — Text** *(build the log line)*

- Add a **Text** action
- Content:
  ```
  [logDate] | run | [durationMins] min | [distanceKm] km | [workoutKcal] kcal
  ```
- Replace `[logDate]`, `[durationMins]`, `[distanceKm]`, `[workoutKcal]` with the Magic Variables you set above (tap the variable name in the text field to insert them)
- Set variable: `newLogLine`

> Note: Heart rate average isn't directly available from workout samples in Shortcuts. The kcal field alone is sufficient for deficit tracking.

---

**Action 10 — Get Contents of URL** *(fetch current file from GitHub)*

- URL: `https://api.github.com/repos/YOUR_USERNAME/health-advisor/contents/logs/phone-log.md`
  - Replace `YOUR_USERNAME` with your GitHub username
- **Method:** GET
- **Headers:**
  - `Authorization` : `Bearer YOUR_GITHUB_TOKEN`
  - `X-GitHub-Api-Version` : `2022-11-28`
- Set variable: `githubResponse`

---

**Action 11 — Get Dictionary Value**

- **Dictionary:** `githubResponse`
- **Key:** `content`
- Set variable: `encodedContent`

---

**Action 12 — Get Dictionary Value**

- **Dictionary:** `githubResponse`
- **Key:** `sha`
- Set variable: `fileSha`

---

**Action 13 — Decode Base64** *(not directly available — use a workaround)*

> **Tip:** Shortcuts doesn't have a native Base64 decode action. Use this URL trick:
> - Add a **URL** action: `data:text/plain;base64,[encodedContent]`
> - Then add **Get Contents of URL** on that URL
> - This returns the decoded file text
> - Set variable: `currentFileText`

---

**Action 14 — Text** *(append new line)*

- Content:
  ```
  [currentFileText]
  [newLogLine]
  ```
- (Put `currentFileText` on line 1, `newLogLine` on line 2 — a newline in between)
- Set variable: `updatedFileText`

---

**Action 15 — Encode Base64** *(encode updated content)*

> Similarly, use a reverse URL trick or a dedicated base64 encode action:
> - **Base64 Encode** action (if available on your iOS version)
> - **Input:** `updatedFileText`
> - Set variable: `encodedUpdated`

---

**Action 16 — Dictionary** *(build the request body)*

- Add a **Dictionary** action with these key-value pairs:
  - `message` (Text): `log: run entry`
  - `content` (Text): `[encodedUpdated]` (the Magic Variable)
  - `sha` (Text): `[fileSha]` (the Magic Variable)

- Set variable: `requestBody`

---

**Action 17 — Get Contents of URL** *(PUT to GitHub API)*

- URL: `https://api.github.com/repos/YOUR_USERNAME/health-advisor/contents/logs/phone-log.md`
- **Method:** PUT
- **Headers:**
  - `Authorization` : `Bearer YOUR_GITHUB_TOKEN`
  - `Content-Type` : `application/json`
  - `X-GitHub-Api-Version` : `2022-11-28`
- **Request Body:** JSON — use `requestBody` dictionary
- (No need to store the result)

---

**Action 18 — Show Notification** *(optional confirmation)*

- **Title:** Run Logged
- **Body:** `[durationMins] min · [distanceKm] km · [workoutKcal] kcal`

---

### Set the Automation Trigger

1. Go to **Automation** tab in Shortcuts
2. Tap **+** → **App** → Choose **Workout** (or search "Workout ends")
3. **Trigger:** When **Apple Watch Workout** ends → **Workout Type:** Running
4. **Run:** Immediately (ask before running = off for automation, or leave it on for one-tap confirmation)
5. Select your **"Log Run"** shortcut

---

## Shortcut 2: Log Stair Climbing

Follow the same steps as above with these differences:

- **Shortcut name:** "Log Stair Climbing"
- **Action 1 — Workout Type filter:** Stair Climbing (not Running)
- **No distance field** — stair climbing doesn't track distance
- **Action 9 — Text (log line):**
  ```
  [logDate] | stair | [durationMins] min | [workoutKcal] kcal
  ```
- **Automation trigger:** Workout Type: **Stair Climbing**
- **Commit message:** `log: stair entry`
- **Notification body:** `[durationMins] min · [workoutKcal] kcal`

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `403` from GitHub | Check token has Contents: Read+Write permission for this repo |
| `409` conflict | Two writes at the same time — retry the shortcut |
| Notification doesn't appear | Check Shortcuts automation notifications are enabled in Settings > Notifications |
| Empty kcal value | Ensure workout was tracked with Apple Watch (not iPhone only) |
| Base64 decode fails | On older iOS, manually install a base64 decode shortcut from the Shortcuts Gallery |

---

## Security Note

Your GitHub token is stored in the **Text** action inside the shortcut. To keep it safe:
- Only share this shortcut via iCloud Shortcut links if you first remove the token
- Use a fine-grained token scoped **only** to the `health-advisor` repo with Contents: Read+Write

---

## What Gets Logged

After completing a 15-minute run, your log will receive a line like:

```
2026-04-19 | run | 15.0 min | 2.32 km | 176 kcal
```

The Health Logger app parses this and:
- Shows it in the **Phase Log** with a Run badge and stat chips
- Adds `+176 kcal` to the **Weekly Deficit** card as a positive outlier
- Includes it in the **Weekly Progress** overlay
