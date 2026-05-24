import streamlit as st
import httpx

st.set_page_config(page_title="GitHub Repo Summarizer", page_icon="🤖")
st.title("🤖 AI GitHub Repo Summarizer")
st.caption("Paste any public GitHub repo URL and get an instant AI summary.")

url = st.text_input("GitHub Repo URL", placeholder="https://github.com/owner/repo")
if st.button("Analyze Repo"):
    if not url:
        st.warning("Please enter a URL!")
    else:
        with st.spinner("Fetching repo and asking AI..."):
            try:
                response = httpx.post(
                    "http://localhost:8000/analyze",
                    json={"url": url},
                    timeout=60
                )

                # Check if backend returned an error
                if response.status_code != 200:
                    error_detail = response.json().get("detail", "Unknown error")
                    st.error(f"Backend error: {error_detail}")
                else:
                    data = response.json()
                    st.success(f"✅ Analyzed: `{data['repo']}`")

                    st.subheader("🧠 AI Summary")
                    st.markdown(data["summary"])

                    st.subheader("📁 File Structure")
                    def build_tree(paths: list) -> dict:
                        """Converts flat file paths into a nested dictionary tree."""
                        tree = {}
                        for path in paths:
                            parts = path.split("/")
                            node = tree
                            for part in parts:
                                node = node.setdefault(part, {})
                        return tree

                    def render_tree(tree: dict, indent: int = 0):
                        """Renders the nested tree with folder/file icons."""
                        for name, children in sorted(tree.items()):
                            is_folder = bool(children)
                            prefix = "　" * indent  # Japanese space for clean indentation

                            if is_folder:
                                st.markdown(f"{prefix}📂 **{name}**")
                                render_tree(children, indent + 1)
                            else:
                                # Pick icon based on file extension
                                ext = name.split(".")[-1].lower() if "." in name else ""
                                icon = {
                                    "py":   "🐍",
                                    "js":   "🟨",
                                    "ts":   "🔷",
                                    "md":   "📝",
                                    "txt":  "📄",
                                    "json": "🔧",
                                    "html": "🌐",
                                    "css":  "🎨",
                                    "yml":  "⚙️",
                                    "yaml": "⚙️",
                                    "env":  "🔒",
                                }.get(ext, "📄")

                                st.markdown(f"{prefix}{icon} {name}")

                    tree = build_tree(data["file_tree"])
                    render_tree(tree)

            except httpx.ConnectError:
                st.error("❌ Cannot reach backend. Is `uvicorn main:app --reload` running?")
            except Exception as e:
                st.error(f"Something went wrong: {e}")