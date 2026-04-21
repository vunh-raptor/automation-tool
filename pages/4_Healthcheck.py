from Common.supporting import (
    login_status_check,
    logout_render,
    request_to_automate_button
)
from Request.healthcheck import (
    healthcheck_request,
    load_homee_api_list,
    save_homee_api_list,
)
from datetime import datetime
from pathlib import Path
import csv
import threading
import time
import pandas as pd
import streamlit as st

# This is to jump the user back to login if their are not authenticated
login_status_check()
logout_render()
request_to_automate_button()

ROOT_DIR = Path(__file__).resolve().parents[1]
HOMEE_API_LIST_FILE = str(ROOT_DIR / "Common" / "data" / "homee_healthcheck_api_list.txt")
HOMEE_RESULT_FILE = str(ROOT_DIR / "Common" / "data" / "homee_healthcheck_results.csv")


def append_healthcheck_results(result_file: str, rows: list[dict]) -> None:
    if not rows:
        return
    result_path = Path(result_file)
    result_path.parent.mkdir(parents=True, exist_ok=True)
    file_exists = result_path.exists()
    with result_path.open("a", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=["api", "status", "status_code", "response_ms", "error", "checked_at"],
        )
        if not file_exists:
            writer.writeheader()
        writer.writerows(rows)


def run_homee_healthcheck_once() -> list[dict]:
    api_urls = load_homee_api_list(HOMEE_API_LIST_FILE)
    if not api_urls:
        return []
    delete_old_results(days=0)
    request_client = healthcheck_request()
    results = request_client.run_homee_healthcheck(api_urls)
    append_healthcheck_results(HOMEE_RESULT_FILE, results)
    return results


def scheduler_loop() -> None:
    last_run_date = None
    while True:
        now = datetime.now()
        if now.hour == 6 and now.minute == 30 and last_run_date != now.date():
            run_homee_healthcheck_once()
            last_run_date = now.date()
        time.sleep(20)


@st.cache_resource
def start_daily_scheduler():
    scheduler_thread = threading.Thread(target=scheduler_loop, daemon=True)
    scheduler_thread.start()
    return scheduler_thread


def load_recent_results() -> pd.DataFrame:
    result_path = Path(HOMEE_RESULT_FILE)
    if not result_path.exists():
        return pd.DataFrame(columns=["api", "status", "status_code", "response_ms", "error", "checked_at"])
    result_df = pd.read_csv(result_path)
    return result_df.tail(200)

def delete_old_results(days: int) -> bool:
    result_path = Path(HOMEE_RESULT_FILE)
    if not result_path.exists():
        return False
    result_df = pd.read_csv(result_path)
    cutoff_date = datetime.now() - pd.Timedelta(days=days)
    result_df["checked_at"] = pd.to_datetime(result_df["checked_at"], errors="coerce")
    filtered_df = result_df[result_df["checked_at"] >= cutoff_date]
    filtered_df.to_csv(result_path, index=False)
    return True


def main():
    start_daily_scheduler()
    st.title("Health Check")
    tab1, tab2, tab3 = st.tabs(["Overview", "HomeX", "HomeE"])
    
    with tab1:
        st.header("System Health Check Overview")
        st.text("This tab provides an overview of the health status of all connected platforms. It displays the results of health checks for HomeX, HomeE, and HOSEL SSO in a consolidated manner. Users can quickly assess the overall system health and identify any issues that may require attention.")

    with tab2:
        st.header("HomeX Health Check")
        st.text("This tab focuses on the health check of the HomeX platform. It performs various checks to ensure that HomeX is functioning correctly, including connectivity tests, API response checks, and performance metrics. Users can view detailed results and logs related to HomeX's health status.")
    with tab3:
        st.header("HomeE Health Check")
        st.caption("Daily scheduler is active and runs HomeE API checks at 06:30 AM.")

        api_list_default = "\n".join(load_homee_api_list(HOMEE_API_LIST_FILE))
        api_list_input = st.text_area(
            "HomeE API list (one URL per line)",
            value=api_list_default,
            height=180,
        )

        save_col, run_col = st.columns(2)
        save_btn = save_col.button("Save API list", type="secondary")
        run_btn = run_col.button("Run HomeE healthcheck now", type="primary")

        if save_btn:
            api_list = [line.strip() for line in api_list_input.splitlines() if line.strip() != ""]
            save_homee_api_list(HOMEE_API_LIST_FILE, api_list)
            st.success(f"Saved {len(api_list)} API URL(s).")

        if run_btn:
            with st.spinner("Running HomeE healthcheck..."):
                api_list = [line.strip() for line in api_list_input.splitlines() if line.strip() != ""]
                save_homee_api_list(HOMEE_API_LIST_FILE, api_list)
                run_results = run_homee_healthcheck_once()
            if not run_results:
                st.warning("No API URLs found. Please add and save API list first.")
            else:
                st.success(f"Completed healthcheck for {len(run_results)} API URL(s).")

        st.subheader("Recent HomeE healthcheck results")
        st.dataframe(load_recent_results(), width='stretch')
        

if __name__ == "__main__":
    main()

