import streamlit as st
import time
# Create a Streamlit app with a slider that doesn't require re-rendering
st.title('Streamlit Slider Example')

# Use st.session_state to store the slider value
if 'slider_value' not in st.session_state:
    st.session_state.slider_value = 0

# Create a slider and update the session state
st.session_state.slider_value = st.slider('Adjust the slider:', 0, 100, st.session_state.slider_value)

# Display the current value of the slider
st.write('Current slider value:', st.session_state.slider_value)


# Use st.session_state to store the text input value


# Create a text input and update the session state
st.session_state.text_input = st.text_input('Enter some text:', st.session_state.text_input)

# Display the current value of the text input


while True:

    st.write('Current text input:', st.session_state.text_input)

    time.sleep(2)