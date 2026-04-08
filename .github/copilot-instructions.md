# Copilot Instructions for SD Automation Hub

## Big picture architecture
- This is a **Streamlit + Selenium operations hub** for Service Desk automation (`main_site.py` + `pages/*.py`).
- Flow is layered: **UI page** (`pages/*`) -> **activity orchestration** (`Activity/*_actions.py`) -> **site/request wrappers** (`Sites/*`, `Common/request_object.py`).
- `Sites/*.py` contains concrete Selenium XPath interactions and domain-specific page methods (e.g., `Sites/homesis.py`, `Sites/umc.py`).
- `Activity/*.py` functions are the business workflow boundary; keep UI logic out of `Sites/*` and locator logic out of `pages/*`.
- `Common/page_object.py` is the Selenium base wrapper used across all site classes.
- `api/` currently exists as scaffold folders only (no active implementation).

## Authentication and session patterns
- `main_site.py` performs LDAP auth through `Common/user_object.py::login` and stores `st.session_state["authenticated"]`.
- In Streamlit pages, gate access with `login_status_check()` (or the equivalent `st.switch_page("main_site.py")`) and render `logout_render()`.
- UMC API requests use `authen_get_UMC_session()` pattern from `pages/1_UMC Automation Scripts.py`:
  - validate SSO with `authenticate_HOSELSSO()`
  - build Basic auth token via `authenticate_swagger()`
  - create request client via `umc_start_session()`.

## Conventions used in this repo
- Decorate page `main()` with `@app_logic_exception.app_logic_exception_handler` for user-facing Streamlit error handling.
- CSV/Excel readers usually force string types (e.g., `{"HR Code": str, "ID number": str}`) to preserve leading zeros.
- For batch actions, iterate uploaded rows and reset page state between users (example in `pages/3_Homesis_Automation.py`: `get_homesis_url(); access_user_managerment()`).
- Error aggregation pattern: action functions return `list_of_error`; UI builds a dataframe and filters out success messages.
- Keep naming and style consistent with existing modules (`login_to_site`, `add_role_*`, `update_*`, `check_*`).

## Critical workflows (Windows/PowerShell)
- Initial setup: run `./setup.ps1` (creates `venv`, installs `requirements.txt`).
- Start app: run `./run_script.ps1` (activates venv, runs `streamlit run main_site.py`).
- Update local + deps: run `./update_script.ps1`.
- Targeted tests: `pytest Tests/General_Automation_unit_test.py` or `pytest Tests/UMC_Automation_unit_test.py`.

## Integration points and external dependencies
- Core libs: `streamlit`, `selenium`, `pandas`, `ldap3`, `requests`, `pyotp`, `msteamsapi` (`requirements.txt`).
- External systems: UMC, Homesis, BSL web UIs (Selenium), HOSEL SSO, LDAP, and Teams webhooks (`Common/supporting.py`).
- Credentials helpers include CyberArk script integration (`Common/data/CBAAccess.ps1` via `cyberark_get_credential_password()`).

## When adding or changing automation
- Put selectors/page actions in `Sites/*`; put multi-step use cases in `Activity/*`; keep `pages/*` as Streamlit orchestration/UI only.
- Reuse existing session/auth helpers and error constants (`Common/constant/*`) instead of introducing duplicate messages.
- Match existing tab-driven UI patterns in `pages/1_UMC Automation Scripts.py` and `pages/3_Homesis_Automation.py`.
