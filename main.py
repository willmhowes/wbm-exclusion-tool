import streamlit as st
import datetime
from generate_urls import generate_urls
from download_whois import download_whois_creationdate
from download_ia import download_iacdx_earliestdate
from compare_urls import was_created_before_earliest_archive

TITLE = "WBM Exclusion Tool"
ICON = "https://archive.org/offshoot_assets/favicon.ico"
st.set_page_config(page_title=TITLE, page_icon=ICON)
st.title(TITLE)

# Import parameters from query
# qp = st.experimental_get_query_params()
# if "urls" not in st.session_state and qp.get("urls"):
#     st.session_state.urls = qp.get("urls")[0]
# if "output_style" not in st.session_state and qp.get("output_style"):
#     st.session_state.output_style = qp.get("output_style")[0]
# if "group" not in st.session_state and qp.get("group"):
#     st.session_state.group = bool(qp.get("group")[0])

option = st.selectbox(
    "URL Quantity",
    ("Individual", "Bulk"),
    index=None,
    placeholder="Select quantity type...",
)

if option == "Bulk":
    st.text_area(
        "Text to analyze",
        help="URLs are extracted from the text block, so formatting does not matter",
        placeholder="Example: archive.org wikipedia.org ...",
        key="urls",
    )
    st.write(f"{len(st.session_state.urls)} characters.")

    st.radio(
        "Output Style",
        ["Internal Note", "Date Comparison"],
        horizontal=True,
        key="output_style",
    )

    if st.session_state.output_style == "Internal Note":
        with st.expander("Configurations", True):
            st.toggle("Group notes into single block?", key="group")

    # st.experimental_set_query_params(urls=st.session_state.urls)

    if st.session_state.output_style == "Internal Note":
        notes = []
        urls = generate_urls(st.session_state.urls, True)
        for url in urls:
            whois_creationdate = download_whois_creationdate(url)
            ia_earliestdate = download_iacdx_earliestdate(url)
            created_before_earliest_archive = (
                was_created_before_earliest_archive(whois_creationdate, ia_earliestdate)
                if isinstance(whois_creationdate, datetime.date)
                and isinstance(ia_earliestdate, datetime.date)
                else "Manual Check required"
            )
            notes.append(
                f"Domain                         : {url}\n"
                + f"WHOIS Creation Date            : {whois_creationdate}\n"
                + f"Earliest WBM Archive           : {ia_earliestdate}\n"
                + f"created_before_earliest_archive: {created_before_earliest_archive}"
            )
        if st.session_state.group:
            st.code("\n\n".join(notes))
            st.divider()
        else:
            for note in notes:
                st.code(note)
                st.divider()

    elif st.session_state.output_style == "Date Comparison":
        before_earliest_archive = []
        after_earliest_archive = []
        unknown = []
        # Creation date is before earliest WBM date
        urls = generate_urls(st.session_state.urls, True)
        for url in urls:
            whois_creationdate = download_whois_creationdate(url)
            ia_earliestdate = download_iacdx_earliestdate(url)
            created_before_earliest_archive = (
                was_created_before_earliest_archive(whois_creationdate, ia_earliestdate)
                if isinstance(whois_creationdate, datetime.date)
                and isinstance(ia_earliestdate, datetime.date)
                else "Manual Check required"
            )
            if created_before_earliest_archive and isinstance(
                created_before_earliest_archive, bool
            ):
                before_earliest_archive.append(url)
            elif not created_before_earliest_archive and isinstance(
                created_before_earliest_archive, bool
            ):
                after_earliest_archive.append(url)
            else:
                unknown.append(
                    f"Domain                         : {url}\n"
                    + f"WHOIS Creation Date            : {whois_creationdate}\n"
                    + f"Earliest WBM Archive           : {ia_earliestdate}"
                )

        st.header("Creation date is before earliest WBM date")
        st.code("\n".join(before_earliest_archive))
        st.divider()
        st.header("Creation date is after earliest WBM date")
        st.code("\n".join(after_earliest_archive))
        st.divider()
        st.header("Manual Verification Required")
        st.code("\n\n".join(unknown))
        st.divider()
