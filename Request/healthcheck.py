from datetime import datetime
from Common.request_object import Session
from pathlib import Path
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class healthcheck_request:
	"""Request helper for HomeE healthcheck API execution."""

	DEFAULT_TIMEOUT = 15

	def __init__(self, timeout: int = DEFAULT_TIMEOUT):
		self.timeout = timeout

	def check_api(self, api_url: str) -> dict:
		"""Run healthcheck for one API URL."""
		target_url = api_url.strip()
		if target_url == "":
			return {
				"api": api_url,
				"status": "SKIPPED",
				"status_code": None,
				"response_ms": None,
				"error": "Empty URL",
				"checked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
			}

		started = datetime.now()
		try:
			response = requests.get(target_url, timeout=self.timeout, verify=False)
			elapsed_ms = int((datetime.now() - started).total_seconds() * 1000)
			return {
				"api": target_url,
				"status": "OK" if response.status_code < 400 else "FAIL",
				"status_code": response.status_code,
				"response_ms": elapsed_ms,
				"error": "",
				"checked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
			}
		except Exception as e:
			elapsed_ms = int((datetime.now() - started).total_seconds() * 1000)
			return {
				"api": target_url,
				"status": "NOK",
				"status_code": None,
				"response_ms": elapsed_ms,
				"error": str(e),
				"checked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
			}

	def run_homee_healthcheck(self, api_urls: list[str]) -> list[dict]:
		"""Run healthcheck against a list of HomeE APIs."""
		return [self.check_api(api_url=url) for url in api_urls if str(url).strip() != ""]


def load_homee_api_list(file_path: str) -> list[str]:
	path = Path(file_path)
	if not path.exists():
		return []
	return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip() != ""]


def save_homee_api_list(file_path: str, api_urls: list[str]) -> None:
	path = Path(file_path)
	path.parent.mkdir(parents=True, exist_ok=True)
	unique_urls = []
	seen = set()
	for url in api_urls:
		clean_url = str(url).strip()
		if clean_url != "" and clean_url not in seen:
			seen.add(clean_url)
			unique_urls.append(clean_url)
	path.write_text("\n".join(unique_urls), encoding="utf-8")
