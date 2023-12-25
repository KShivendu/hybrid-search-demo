import streamlit as st
from streamlit_tags import st_tags
from query import run_search

from constants import LABELS


def main():
    st.title("Qdrant Hackathon Demo")

    if 'filter_text' not in st.session_state:
        st.session_state.filter_text = 'Filter: None'

    st.write(st.session_state.filter_text)

    def handle_query():
        state_query = st.session_state.query
        # state_tags = st.session_state.tags
        state_expression = st.session_state.expression

        if state_query or state_expression:  # checking if the query is not empty
            images, filters = run_search(state_query, state_expression, [], 5)

            print(filters)
            st.session_state.filter_text = str(filters)

            # Create a single row of 5 columns for images
            cols = st.columns(5)  # create 5 columns
            for col, img in zip(
                cols, images
            ):  # iterating over columns and respective images
                with col:  # specifies which column to put the image in
                    caption = f"Payload: {img.payload}"

                    if state_query != "":
                        caption += f" | Score: {img.score}"

                    st.image(
                        img.payload["image_path"],
                        caption=caption,
                        use_column_width=True,
                    )

            # # Display each image using Streamlit's `st.image`
            # for img in images:
            #     st.image(img.payload['image_path'], caption=f"Score: {img.score} | Payload: '{img.payload}'")
        else:
            st.warning("Please enter a query to fetch images.")

    query = st.text_input("Enter your query:", key="query", on_change=handle_query)
    expression = st.text_input("Enter your expression:", key="expression", on_change=handle_query)

    # keywords = st_tags(
    #     label='### Enter tags and press fetch images:',
    #     text='Press enter to add more',
    #     value=['person'],
    #     suggestions=LABELS,
    #     maxtags=3,
    #     key="tags",
    #     # on_change=handle_query,
    # )

    # filters = st.text_input("Enter your filters:", key="filters", on_change=handle_query)
    st.button("Fetch Images", on_click=handle_query)

if __name__ == '__main__':
    main()
