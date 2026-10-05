# Screen reader comparison: VoiceOver vs NVDA

Why this suite tests two readers, how they differ, and what each costs you.

## Why not just one

A screen reader does not read the page. It reads the **accessibility tree** that the
browser builds from the page, and each reader plus browser pair builds and speaks it a
little differently. A page can pass in one pair and fail in another. Testing with two,
on different operating systems, catches both bugs in the markup and bugs that only
appear where a reader is being generous.

You still cannot cover everything. Two readers is the practical minimum, not full
coverage. See the "What this does not cover" list at the end.

## At a glance

| | VoiceOver + Safari | NVDA + Firefox |
| --- | --- | --- |
| Platform | macOS (also iOS as a separate reader) | Windows |
| Cost | Free, built in | Free, open source |
| Setup effort | None, plus one Safari setting (Tab key) | Download and install |
| Learning curve | Steeper keystrokes (two-key `VO` prefix), the Web Rotor is powerful but unfamiliar | Gentler; single-letter navigation keys (`H`, `B`, `F`) are quick |
| Mode model | One model; you navigate item by item | **Two modes** (browse, focus) and the switch itself causes bugs |
| Primary navigation | `VO+Right`, Web Rotor | Arrow keys, quick keys, Elements list |
| Typical time for the 12 SR cases | 45 minutes | 45 minutes |
| Time if new to the reader | +15 minutes | +20 minutes |
| Speech wording | Terser; says "collapsed"/"expanded" | Often more explicit; announces required, invalid, pressed |
| Live regions | Polite messages are queued; assertive may interrupt | Alert messages usually interrupt immediately; polite are queued |
| Verification of output | Caption panel | Speech Viewer |

> Times are estimates for the 12 cases in these scripts. Record your own in the run sheet;
> the first pass is always slower.

## Where they differ in ways that matter to Testbook

| Behaviour | What to expect | What it tells you |
| --- | --- | --- |
| **Tab key in Safari** | Skips links and buttons unless the "Press Tab to highlight each item" option is on | Keyboard results in Safari are not representative unless you changed the setting. Use Chrome or Firefox for script 01 |
| **Toggle buttons (`aria-pressed`)** | Both announce pressed state, with different wording | Fine, as long as the state is spoken at all |
| **`aria-expanded`** | Both announce expanded/collapsed | Fine |
| **`role="alert"`** | NVDA speaks it at once; VoiceOver does too but timing varies | If one stays silent, check that the element was inserted *after* page load |
| **Polite live region** (`role="status"`) | NVDA may speak a second or two late | Wait before failing a case. Real users wait |
| **Articles** | VoiceOver names them; NVDA may only speak the name on entry | An article with a name is still valuable for navigation |
| **Emoji** | Read from the emoji dictionary, which differs per OS | This is why reactions have text labels. Never rely on emoji names |
| **Disabled buttons** | Both skip or announce "dimmed/unavailable" | Check the loading state of Login and Post |
| **Mode switching (NVDA)** | A custom widget that needs focus mode may not trigger it | A widget that works in VoiceOver but not NVDA often fails here |

## What manual screen reader testing can and cannot tell you

| | Automation (axe, tests) | Manual screen reader |
| --- | --- | --- |
| Name, role and state exist in the tree | Yes | Yes, as spoken |
| The live-region text is correct | Yes (we assert it) | Yes |
| The live region is actually *spoken* | **No** | **Yes** |
| The spoken wording is understandable | No | **Yes** |
| The reading order makes sense | Partly (DOM order) | **Yes** |
| Works in a specific reader and browser pair | No | **Yes**, only for that pair |
| Repeatable in CI | **Yes** | No |
| Cost per run | Seconds | About an hour per reader |

## Running the two scripts together

- Run the same case in both readers, back to back where you can (two machines or a
  Windows VM), so you remember what you heard.
- Record the result for each reader in the run sheet's two columns.
- If the results differ, investigate the markup. Do not pick the more flattering one.
- A pass in both is strong evidence. A pass in one is a pass for that pair only.

## What this does not cover

- **Mobile screen readers.** iOS VoiceOver and Android TalkBack behave differently again
  (gestures, no `Tab`, different rotor). Worth a smoke test before a real release.
- **Other readers.** JAWS (paid, widely used in workplaces) and Narrator have their own
  quirks. NVDA and JAWS often agree; VoiceOver is the outlier.
- **Other browser pairings.** NVDA + Chrome and VoiceOver + Chrome behave differently from
  the pairings above.
- **Real users.** Nothing in this suite replaces testing with people who use assistive
  technology daily. They find problems no checklist anticipates.

## Which to start with

- You are on a Mac: start with **VoiceOver**. It costs nothing and is already installed.
- You are on Windows: start with **NVDA**.
- You have both: run VoiceOver first, then NVDA, and compare. The differences are the most
  instructive part.
