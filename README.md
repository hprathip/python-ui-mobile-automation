# python-ui-mobile-automation

![tests](https://github.com/hprathip/python-ui-mobile-automation/actions/workflows/tests.yml/badge.svg)

Test automation framework in **Python + PyTest** covering web UI, API and (in progress) mobile.

| Layer | Tooling | Practice target |
|---|---|---|
| Web UI | Playwright, Page Object Model | Sauce Demo, The Internet |
| Network | Playwright route mocking, tracing | Playwright API-mocking demo |
| API | requests, JSON Schema | Restful Booker |
| Mobile | Appium 2 (UiAutomator2) | *in progress* |

## Highlights
- Page objects with lazy, role-based locators; chained fixtures (browser → context → page → page objects)
- API client layer, session-scoped auth, factory fixtures that clean up created test data
- Network mocking: mocked, modified and failing (HTTP 500) responses
- Known defects documented as `xfail(strict=True)` tests
- CI on every pull request (GitHub Actions); Playwright traces uploaded as artifacts on failure

## Run locally
```bash
python -m venv .venv
.venv\Scripts\activate            # macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m playwright install chromium

pytest tests/api -v               # API tests
pytest tests/web -v               # web tests (headless)
pytest -m smoke -v                # smoke suite only
pytest tests/web --headed --slowmo 300   # watch the browser
```

## Project structure
```
api/        BookingClient, payload builder, JSON schemas
config/     URLs and environment settings
data/       Test users (frozen dataclasses)
pages/      Page objects (Sauce Demo)
tests/
  api/      CRUD, negative and schema tests
  web/      UI, network and resource-blocking tests
```