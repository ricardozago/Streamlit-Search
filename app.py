# Baseado em https://betterprogramming.pub/build-a-search-engine-for-medium-stories-using-streamlit-and-elasticsearch-b6e717819448

import streamlit as st
import urllib.parse
import templates
from dados import get_textos
from utils import count_ocurrences

PAGE_SIZE = 10


def set_session_state():
    # set default values
    if "search" not in st.session_state:
        st.session_state.search = None
    if "tags" not in st.session_state:
        st.session_state.tags = None
    if "page" not in st.session_state:
        st.session_state.page = 1

    # get parameters in url
    para = st.experimental_get_query_params()
    if "search" in para:
        st.experimental_set_query_params()
        # decode url
        new_search = urllib.parse.unquote(para["search"][0])
        st.session_state.search = new_search
    if "tags" in para:
        st.experimental_set_query_params()
        st.session_state.search = para["tags"][0]
    if "page" in para:
        st.experimental_set_query_params()
        st.session_state.page = int(para["page"][0])


def main():
    set_session_state()
    st.write(templates.load_css(), unsafe_allow_html=True)
    st.title("Wikipedia Nano Search")

    if st.session_state.search is None:
        search = st.text_input("Entre com os termos a serem buscados:")
    else:
        search = st.text_input(
            "Entre com os termos a serem buscados:", st.session_state.search
        )

    if search:
        from_i = (st.session_state.page - 1) * PAGE_SIZE
        st.session_state.tags = search
        textos, total_hits, tempo = get_textos(search)

        st.write(templates.number_of_results(total_hits, tempo), unsafe_allow_html=True)

        for i in range(min([total_hits, PAGE_SIZE])):
            texto_trat = textos.iloc[i + from_i]["text"][
                : min([300, len(textos.iloc[i + from_i]["text"])])
            ]
            texto_trat = texto_trat.replace(search, "<b>" + search + "</b>")
            search_trat = list(search)
            search_trat[0] = search_trat[0].upper()
            search_trat = "".join(search_trat)
            texto_trat = texto_trat.replace(search_trat, "<b>" + search_trat + "</b>")

            st.write(
                templates.search_result(
                    i + from_i,
                    textos.iloc[i + from_i]["url"],
                    textos.iloc[i + from_i]["title"],
                    texto_trat + "...",
                    textos.iloc[i + from_i]["title"],
                    str(len(textos.iloc[i + from_i]["text"].split())) + " palavras",
                ),
                unsafe_allow_html=True,
            )

            st.write(
                templates.tag_boxes(
                    search,
                    count_ocurrences(textos.iloc[i + from_i]["text"]),
                    st.session_state.tags,
                ),
                unsafe_allow_html=True,
            )

        # pagination
        if total_hits > PAGE_SIZE:
            total_pages = (total_hits + PAGE_SIZE - 1) // PAGE_SIZE
            pagination_html = templates.pagination(
                total_pages, search, st.session_state.page, st.session_state.tags
            )
            st.write(pagination_html, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
