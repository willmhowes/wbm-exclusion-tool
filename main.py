import streamlit as st
import datetime
from generate_urls import extract_urls_from_text
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

if option == "Individual":
    st.text_input(
        "Text to extract URL from",
        help="URL is extracted from the text, so formatting does not matter",
        placeholder="Example: archive.org",
        key="url",
    )
    st.radio(
        "Output Style",
        ["Internal Note"],
        horizontal=True,
        key="output_style",
    )

    with st.expander("Configurations", True):
        st.toggle("Strip www from url?", key="stripwww")

    if st.session_state.output_style == "Internal Note" and st.session_state.url != "":
        url = extract_urls_from_text(st.session_state.url, st.session_state.stripwww)[0]
        whois_creationdate = download_whois_creationdate(url)
        ia_earliestdate = download_iacdx_earliestdate(url)
        created_before_earliest_archive = (
            was_created_before_earliest_archive(whois_creationdate, ia_earliestdate)
            if isinstance(whois_creationdate, datetime.date)
            and isinstance(ia_earliestdate, datetime.date)
            else "Manual Check required"
        )
        st.code(
            f"Domain                         : {url}\n"
            + f"WHOIS Creation Date            : {whois_creationdate}\n"
            + f"Earliest WBM Archive           : {ia_earliestdate}\n"
            + f"created_before_earliest_archive: {created_before_earliest_archive}"
        )
        st.divider()

elif option == "Bulk":
    st.text_area(
        "Text to extract URLs from",
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

    # st.experimental_set_query_params(urls=st.session_state.urls)

    if st.session_state.output_style == "Internal Note":
        with st.expander("Configurations", True):
            st.toggle("Group notes into single block?", key="group")
            st.toggle("Strip www from url?", key="stripwww")
        notes = []
        urls = extract_urls_from_text(st.session_state.urls, st.session_state.stripwww)
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
        with st.expander("Configurations", True):
            st.toggle("Strip www from url?", key="stripwww")
        before_earliest_archive = []
        after_earliest_archive = []
        unknown = []
        # Creation date is before earliest WBM date
        urls = extract_urls_from_text(st.session_state.urls, st.session_state.stripwww)
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
        st.code(
            (
                "\n".join(before_earliest_archive)
                if len(before_earliest_archive) > 0
                else "None"
            )
        )
        st.divider()
        st.header("Creation date is after earliest WBM date")
        st.code(
            (
                "\n".join(after_earliest_archive)
                if len(after_earliest_archive) > 0
                else "None"
            )
        )
        st.divider()
        if len(unknown) > 0:
            st.header("Manual Verification Required", help="For some reason, the program was unable to automatically determine which date comes first (likely due to domain registrar formatting beyond our control). You'll have to manually inspect the dates and make your own conclusions.")
            st.code("\n\n".join(unknown))
            st.divider()
