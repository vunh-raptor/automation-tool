import streamlit as st
import requests

from Common.constant import app_logic_exception

API_URL_DEFAULT = "http://sd-auto.homecredit.vn:1234/ask"



def _extract_answer(payload: object) -> str:
    if isinstance(payload, str):
        return payload

    if isinstance(payload, dict):
        output_items = payload.get("output")
        if isinstance(output_items, list):
            for item in output_items:
                if isinstance(item, dict):
                    content = item.get("content")
                    if isinstance(content, str) and content.strip() != "":
                        return content

        for key in ("answer", "response", "message", "content", "text"):
            value = payload.get(key)
            if isinstance(value, str) and value.strip() != "":
                return value

        choices = payload.get("choices")
        if isinstance(choices, list) and len(choices) > 0:
            first_choice = choices[0]
            if isinstance(first_choice, dict):
                message_obj = first_choice.get("message")
                if isinstance(message_obj, dict):
                    content = message_obj.get("content")
                    if isinstance(content, str) and content.strip() != "":
                        return content

                for key in ("text", "content"):
                    value = first_choice.get(key)
                    if isinstance(value, str) and value.strip() != "":
                        return value

    return str(payload)


def _call_chat_api(api_url: str, user_prompt: str, history: list[dict]) -> tuple[bool, str]:
    request_payload = {
        "question": user_prompt
    }

    try:
        response = requests.post(api_url, json=request_payload, timeout=120)
        response.raise_for_status()
    except requests.RequestException as exc:
        return False, f"Request failed: {exc}"

    try:
        body = response.json()
    except ValueError:
        return False, "Invalid JSON response from API."

    return True, _extract_answer(body)


@app_logic_exception.app_logic_exception_handler
def main():
    st.title("AI Prompt Chat")
    st.caption("Send prompt to local backend and get answers from API.")

    if "ai_chat_history" not in st.session_state:
        st.session_state["ai_chat_history"] = []

    clear_col, _ = st.columns([1, 4])
    if clear_col.button("Clear chat"):
        st.session_state["ai_chat_history"] = []
        st.rerun()

    for item in st.session_state["ai_chat_history"]:
        role = item.get("role", "assistant")
        content = item.get("content", "")
        with st.chat_message("user" if role == "user" else "assistant"):
            st.write(content)

    user_prompt = st.chat_input("Type your prompt...")

    if not user_prompt:
        return

    st.session_state["ai_chat_history"].append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.write(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            ok, answer = _call_chat_api(
                api_url=API_URL_DEFAULT,
                user_prompt=user_prompt,
                history=st.session_state["ai_chat_history"],
            )

        if not ok:
            st.error(answer)
            st.session_state["ai_chat_history"].append({"role": "assistant", "content": answer})
            return

        st.write(answer)
        st.session_state["ai_chat_history"].append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    main()
