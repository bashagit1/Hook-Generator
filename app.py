import os
import json
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client with API key
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Define the hook generator prompt template
hook_generator_prompt = """
as an expert copywriter specialized in hook generation, your task is to 
analyze the [Provided_Hook_Examples].

Use the templates that fit most to generate 3 new Hooks 
for the following topic: {user_input} and Usage in: {usage}. 

The output should be ONLY valid JSON as follows:
[
  {{
    "hook_type": "The chosen hook type",
    "hook": "the generated hook"
  }},
  {{
    "hook_type": "The chosen hook type",
    "hook": "the generated hook"
  }},
  {{
    "hook_type": "The chosen hook type",
    "hook": "the generated hook"
  }}
]

[Provided_Hook_Examples]:
"Hook Type,Template,Use In
Strong sentence,"[Topic] won’t prepare you for [specific aspect].",Social posts, email headlines, short content
The Intriguing Question,"What’s the [adjective describing difference] difference between [Subject 1] and [Subject 2]?",Video intros, email headlines, social posts
Fact,"Did you know that [Interesting Fact about a Topic]?",Video intros, email headlines, social posts, short content
Metaphor,"[Subject] is like [Metaphor]; [Explanation of Metaphor].",Video intros, email headlines, short content
Story,"[Time Frame], [I/We/Subject] was/were [Situation]. Now, [Current Situation].",Video intros, short content
Statistical,"Nearly 70% of [Population] experience [Phenomenon] at least once in their lives.",Blog posts, reports, presentations
Quotation,"[Famous Person] once said, '[Quotation related to Topic]'.",Speeches, essays, social posts
Challenge,"Most people believe [Common Belief], but [Contradictory Statement].",Debates, persuasive content, op-eds
Visual Imagery,"Imagine [Vivid Description of a Scenario].",Creative writing, advertising, storytelling
Call-to-Action,"If you’ve ever [Experience/Desire], then [Action to take].",Marketing content, motivational speeches, campaigns
Historical Reference,"Back in [Year/Period], [Historical Event] changed the way we think about [Topic].",Educational content, documentaries, historical analyses
Anecdotal,"Once, [Short Anecdote related to Topic].",Personal blogs, speeches, narrative content
Humorous,"Why did [Topic] cross the road? To [Punchline].",Social media, entertaining content, ice-breakers
Controversial Statement,"[Controversial Statement about a Topic].",Debates, opinion pieces, discussion forums
Rhetorical Question,"Have you ever stopped to think about [Thought-Provoking Question]? ",Speeches, persuasive essays, social posts
"
The JSON object:\n\n"""

# Streamlit app UI
st.set_page_config(page_title="Hook Generator", page_icon="✍️", layout="centered")

# Add custom CSS for styling and animation
st.markdown(
    """
    <style>
    .main {
        background-color: #f9f9f9;
        color: #333;
    }
    .header {
        background-color: #4CAF50;
        color: white;
        padding: 10px;
        text-align: center;
        border-radius: 5px;
    }
    .stTextInput, .stSelectbox, .stButton {
        border-radius: 5px;
        border: 1px solid #ccc;
        padding: 10px;
        margin-bottom: 15px;
        background-color: #fff;
    }
    .stTextArea {
        background-color: #e7f4e4;
        border: 1px solid #4CAF50;
    }

    /* Animation Styles */
    @keyframes dance {
        0% { transform: translateY(0); }
        25% { transform: translateY(-10px); }
        50% { transform: translateY(0); }
        75% { transform: translateY(10px); }
        100% { transform: translateY(0); }
    }
    
    .dancer {
        width: 100px;
        animation: dance 1s infinite;
        display: none; /* Initially hidden */
        margin: 20px auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Add title and header
st.title("✨ Hook Generator")
st.header("Generate Engaging Hooks for Your Content")

# User inputs for topic
input_topic = st.text_input("Enter the Topic:", "AI tools")

# User inputs for usage with multiple choice options
usage_options = [
    "short video",
    "social media post",
    "email marketing",
    "blog article",
    "podcast intro",
    "other (please specify)"
]
input_usage = st.selectbox("Select Usage:", usage_options)

# Option for custom usage input if "other" is selected
if input_usage == "other (please specify)":
    input_usage = st.text_input("Please specify usage:")

# Button to generate hooks
if st.button("Generate Hooks"):
    # Display the dancing cartoon animation
    st.markdown('<img class="dancer" src="https://cdn2.iconfinder.com/data/icons/animated-icons/512/dancing-girl.gif" />', unsafe_allow_html=True)
    st.markdown("<script>document.querySelector('.dancer').style.display = 'block';</script>", unsafe_allow_html=True)

    # Format the prompt with user inputs
    input_prompt = hook_generator_prompt.format(user_input=input_topic, usage=input_usage)

    # Generate response from the OpenAI model
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": input_prompt,
                }
            ],
            model="gpt-3.5-turbo",
        )
        
        # Extract the generated text from the response
        generated_text = response.choices[0].message.content
        
        # Try to parse the JSON output
        hooks = json.loads(generated_text)
        st.success("Hooks Generated:")

        for hook in hooks:
            st.markdown(f"### Hook Type: {hook['hook_type']}")
            st.markdown(f"**Hook:** {hook['hook']}")
            
            # Display the generated hook in a text area for easy copying
            hook_text_area = st.text_area(f"Copy Hook:", value=hook['hook'], height=100, key=hook['hook'])
            
            # Provide instructions for copying
            st.markdown("Press Ctrl+C to copy the text above.")

        # Button to copy all hooks
        all_hooks_text = "\n".join(f"{hook['hook_type']}: {hook['hook']}" for hook in hooks)
        all_hooks_text_area = st.text_area("All Hooks (copy all):", value=all_hooks_text, height=300)

    except json.JSONDecodeError:
        st.error("Failed to parse JSON. Please ensure the response is in the correct format.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
