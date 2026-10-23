---
name: webapp-testing
description: Test and interact with local web applications through Python Playwright. Use to verify frontend behavior, debug UI problems, capture browser screenshots, and read browser console logs.
license: Complete terms in LICENSE.txt
---

# Web Application Testing

To test a local web application, write native Python Playwright scripts.

**Helper scripts**:
- `scripts/with_server.py` - Starts and stops one or more servers.

**Always run a script with `--help` first** to see its usage. Do not read the source until you run the script and find that a custom solution is necessary. These scripts can be very large, and their source fills your context window. Call them directly as black-box scripts. Do not read them into your context window.

## Decision Tree: Choose Your Approach

```
User task → Is it static HTML?
    ├─ Yes → Read HTML file directly to identify selectors
    │         ├─ Success → Write Playwright script using selectors
    │         └─ Fails/Incomplete → Treat as dynamic (below)
    │
    └─ No (dynamic webapp) → Is the server already running?
        ├─ No → Run: python scripts/with_server.py --help
        │        Then use the helper + write simplified Playwright script
        │
        └─ Yes → Reconnaissance-then-action:
            1. Navigate and wait for networkidle
            2. Take screenshot or inspect DOM
            3. Identify selectors from rendered state
            4. Execute actions with discovered selectors
```

## Example: Use with_server.py

To start a server, run `--help` first. Then use the helper.

**One server:**
```bash
python scripts/with_server.py --server "npm run dev" --port 5173 -- python your_automation.py
```

**More than one server (for example, backend and frontend):**
```bash
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python your_automation.py
```

An automation script must contain only Playwright logic. The helper starts and stops the servers.
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True) # Always launch chromium in headless mode
    page = browser.new_page()
    page.goto('http://localhost:5173') # Server already running and ready
    page.wait_for_load_state('networkidle') # CRITICAL: Wait for JS to execute
    # ... your automation logic
    browser.close()
```

## Reconnaissance-Then-Action Pattern

1. **Inspect the rendered DOM**:
   ```python
   page.screenshot(path='/tmp/inspect.png', full_page=True)
   content = page.content()
   page.locator('button').all()
   ```

2. **Identify the selectors** from the inspection results.

3. **Do the actions** with the selectors that you found.

## Common Error

❌ **Do not** inspect the DOM of a dynamic app before it reaches `networkidle`.
✅ **Do** call `page.wait_for_load_state('networkidle')` before you inspect.

## Best Practices

- **Use the bundled scripts as black boxes.** For each task, check if a script in `scripts/` can do it. These scripts do common, complex workflows reliably and keep the context window small. Use `--help` to see the usage, then run the script directly.
- Use `sync_playwright()` for synchronous scripts.
- Always close the browser when you are done.
- Use descriptive selectors: `text=`, `role=`, CSS selectors, or IDs.
- Add the necessary waits: `page.wait_for_selector()` or `page.wait_for_timeout()`.

## Reference Files

- **examples/** - Examples of common patterns:
  - `element_discovery.py` - Find the buttons, links, and inputs on a page.
  - `static_html_automation.py` - Use file:// URLs for local HTML.
  - `console_logging.py` - Capture console logs during automation.
