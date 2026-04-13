# iOS Shortcut: Auto-Log Workouts

When you finish a run or stair climbing session on your Apple Watch, an automation on your iPhone fires automatically. It reads the workout data from Health and sends it to GitHub in a single API call. GitHub does the rest — it appends the log line and commits it.

**You build two things:**
1. A **Shortcut** for each workout type (Log Run, Log Stair Climbing)
2. An **Automation** that fires each shortcut when the matching workout ends

---

## How it works

Your phone makes one POST request to the GitHub API:

```
POST https://api.github.com/repos/MathewO/health-advisor/dispatches
```

GitHub Actions receives it, formats the log line, and commits it to `phone-log.md`. No base64, no file reading on your phone.

---

## Before you start

Have these ready:
- Your GitHub Personal Access Token (same one in Health Logger Settings)
- The URL above with your actual username

---

## Part 1 — Build the "Log Run" Shortcut

Open the **Shortcuts** app → tap the **+** in the top right → tap the shortcut name at the top and rename it **"Log Run"**.

Now add each action below by tapping **"Add Action"** (or the search bar at the bottom) and searching for it by name.

---

### Action 1 — Find Health Samples

Search: `Find Health Samples`

Once added, configure it:
- Tap **"All"** (next to Health Samples) → choose **Workouts**
- Tap **"Add Filter"** → tap **Workout Type** → tap **is** → choose **Running**
- Tap **"Sort by"** → choose **Start Date** → tap **Newest First**
- Tap **"Limit"** and set it to **1**

This grabs your most recent run.

---

### Action 2 — Get Details of Health Sample (Start Date)

Search: `Get Details of Health Sample`

- Tap **"Detail"** → choose **Start Date**
- The input should automatically be the workout from Action 1 (shown as a blue token). If not, tap the input field and select it.

---

### Action 3 — Format Date

Search: `Format Date`

- The date field should auto-fill with the result of Action 2. If not, tap it and pick the magic variable.
- Tap **"Medium"** → tap **"Custom"**
- In the custom format field, type exactly: `yyyy-MM-dd`

This gives you the date as `2026-04-19`.

Now tap **"Add Action"** → search **Set Variable** → set name to **`logDate`**, value = the Format Date result (blue token from this step).

---

### Action 4 — Get Details of Health Sample (Duration)

Search: `Get Details of Health Sample` again

- Tap **"Detail"** → choose **Duration**
- Input = workout from Action 1

---

### Action 5 — Calculate (seconds → minutes)

Search: `Calculate`

- Tap the first number field → select the magic variable from Action 4 (the duration)
- Tap the operator → choose **÷**
- Type **60** in the second field

Then add a **Round Number** action:
- Search: `Round Number`
- Input: result of Calculate
- Round to: **1 Decimal Place**

Tap **Set Variable** → name: **`durationMins`**

---

### Action 6 — Get Details of Health Sample (Distance)

Search: `Get Details of Health Sample` again

- Detail: **Total Distance**
- Input = workout from Action 1

> **Note:** This comes back in km if your iPhone's Health app is set to metric (Region: UK). If it returns miles, add a **Convert Measurement** action → From: Miles → To: Kilometres.

Add **Round Number** → 2 Decimal Places → Set Variable **`distanceKm`**

---

### Action 7 — Get Details of Health Sample (Calories)

- Detail: **Total Energy Burned**
- Input = workout from Action 1

Add **Round Number** → 0 Decimal Places → Set Variable **`workoutKcal`**

---

### Action 8 — Get Contents of URL (the API call)

Search: `Get Contents of URL`

Set the fields as follows:

**URL:**
```
https://api.github.com/repos/MathewO/health-advisor/dispatches
```

**Method:** tap GET → change to **POST**

**Headers** — tap "Add new header" twice:

| Key | Value |
|---|---|
| `Authorization` | `Bearer YOUR_GITHUB_TOKEN` |
| `X-GitHub-Api-Version` | `2022-11-28` |

Replace `YOUR_GITHUB_TOKEN` with your actual token.

**Request Body:** tap **"Request Body"** → choose **JSON**

You'll see a dictionary editor. Add these keys by tapping **+**:

| Key | Type | Value |
|---|---|---|
| `event_type` | Text | `log-run` |
| `client_payload` | Dictionary | *(see below)* |

For `client_payload`, tap its value area → it should let you create a nested dictionary. Add:

| Key | Type | Value |
|---|---|---|
| `date` | Text | [tap and insert magic variable `logDate`] |
| `duration` | Text | [tap and insert magic variable `durationMins`] |
| `km` | Text | [tap and insert magic variable `distanceKm`] |
| `kcal` | Text | [tap and insert magic variable `workoutKcal`] |

---

### Action 9 — Show Notification (optional)

Search: `Show Notification`

- **Title:** `Run Logged ✓`
- **Body:** tap and insert `durationMins`, type ` min · `, insert `distanceKm`, type ` km · `, insert `workoutKcal`, type ` kcal`

---

## Part 2 — Set Up the Automation

This makes the shortcut fire automatically every time you finish a run.

1. In the Shortcuts app, tap **Automation** (bottom tab)
2. Tap **+** in the top right
3. Tap **Personal Automation**
4. Scroll down to find **Workout** (under Health) → tap it
5. Set: **"Ends"** (not Starts)
6. Tap **Workout Type** → choose **Running**
7. Tap **Next**
8. Tap **Add Action** → search for **Run Shortcut** → select your **"Log Run"** shortcut
9. Tap **Next** → tap **Done**

**To run silently (no confirmation tap):**
On the final screen, turn off **"Ask Before Running"**. With this off, the shortcut fires automatically in the background — no notification to tap. Leave it ON if you want a confirmation tap first.

---

## Part 3 — Build the "Log Stair Climbing" Shortcut

Follow the exact same steps as above with these differences:

- **Shortcut name:** `Log Stair Climbing`
- **Action 1 filter:** Workout Type → **Stair Climbing** (not Running)
- **Skip Action 6** — stair climbing doesn't track distance, so you don't need `distanceKm`
- **Action 8 — event_type value:** `log-stair` (not `log-run`)
- **Action 8 — client_payload:** only 3 keys: `date`, `duration`, `kcal` (no `km`)
- **Automation trigger:** Workout Type → **Stair Climbing**
- **Run Shortcut in automation:** `Log Stair Climbing`

---

## What gets logged

After a 15-minute run, `logs/phone-log.md` will receive a new line:

```
2026-04-19 | run | 15.0 min | 2.32 km | 176 kcal
```

The Health Logger app shows this in the Phase Log with a Run badge, and counts the calories burned as a positive outlier in the Weekly Deficit card.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Nothing happens after workout | Check automation has "Run Shortcut" configured, not "Open App" |
| GitHub returns 401 | Token is wrong or expired — check it in Settings |
| GitHub returns 403 | Token doesn't have Contents: Read+Write for this repo |
| Distance comes back in miles | Add a **Convert Measurement** action after Action 6: From Miles, To Kilometres |
| Duration looks wrong | Check the Calculate step — duration from Health is in seconds, divide by 60 |
| Automation fires but shortcut fails silently | Open the shortcut manually (tap it in the Shortcuts tab) to see any error |

---

## Security

Your GitHub token is stored inside the shortcut as plain text in the Get Contents of URL action. Don't share this shortcut via iCloud link without removing the token first.
