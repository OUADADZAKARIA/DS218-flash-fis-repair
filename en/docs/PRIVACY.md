# Privacy: what must never be published

A NAS leaves identity traces everywhere. Before publishing a file, a screenshot or a photo, check:

| To hide / not to publish | Where it appears |
|---|---|
| NAS and disk serial numbers | Label, Synology Assistant, logs, SMART, flash dumps |
| MAC address | Label, Synology Assistant, logs, `ifconfig`, flash dumps |
| IP addresses (internal and public) | Network screenshots, `ipconfig`, logs |
| Server name and user names | `login:` prompt, logs, DSM screenshots |
| E-mail address, QuickConnect IDs | DSM, wizard |
| File paths on your machine | File explorer and command-prompt screenshots (they contain your user name) |
| Make and model of your router, city, region | Network screenshots, time zone |
| **Your git identity** | The name and e-mail stored in `git config` end up in every public commit |

## Never publish

- The `.bin` flash dump files: they contain the factory identity (MAC, serial number).
- Raw PuTTY `.log` / `.txt` logs.
- `.pat` files (Synology's property).

This repository's `.gitignore` blocks these extensions.

## Git identity

Before the first commit, set an identity that does not reveal your real name or e-mail address, for example the "noreply" address GitHub gives you (GitHub > Settings > Emails > "Keep my email addresses private"):

```sh
git config user.name  "your-pseudonym"
git config user.email "<id>+<pseudonym>@users.noreply.github.com"
```

Check with `git log --format='%an <%ae>'` before pushing. A commit already pushed keeps its author: changing it means rewriting the history.

## Photos and screenshots

1. Blur **before** saving the final file (a blur layered by an editor that keeps layers is not safe: export as a flattened image).
2. For a NAS label: do not publish the photo, or fully mask the area.
3. Reopen the exported image and check that nothing is readable, even when zooming.

## Automatic check before publishing

From the repository root (adapt the patterns to your case: your name, your server name, your addresses):

```sh
grep -rniE "[0-9A-F]{2}(:[0-9A-F]{2}){5}|192\.168\.|169\.254\.|@[a-z0-9.-]+\.[a-z]{2,}" . --include="*.md" --include="*.py" --include="*.sh"
grep -rniE "your_name|your_server|your_user" .
```

IP and MAC addresses must only appear as placeholders (`<NAS_IP>`, `<MAC>`, `169.254.x.x`).
