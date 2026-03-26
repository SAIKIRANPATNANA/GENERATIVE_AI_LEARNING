import streamlit as st
import time
from preprocessing import *
from streamlit_extras.let_it_rain import rain
from aider import *

t = 0

@st.cache_data
def get_preprocessed_data(uploaded_file):
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    person1, person2, chat = preprocess1(data)
    df = preprocess2(data)
    if len(chat)>500: 
        chat = chat[:500]
    return person1,person2,chat,df

@st.cache_data
def get_insights_from_chat(person1,person2,chat):
    try:
      rel,a,b,aoc,soc = get_response(person1,person2,chat)
      return rel,a,b,aoc,soc
    except Exception as e:
        print(e)
        st.error("Sorry, there is something wrong in your input chat!")
        st.info("You can either wait for sometime or try again later.")
        exit(1)
        
def hearts():
    rain(
        emoji="❣️",
        font_size=40,
        falling_speed=5,
        animation_length="infinite",
    )

def set_bg_hack_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url("https://www.itl.cat/pngfile/big/219-2195851_wallpapers-id-black-and-red-heart.png");
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
    
def set_sidebar_background():
    sidebar_style = f"""
    <style>
    .sidebar .sidebar-content {{
        background-image: url(https://w0.peakpx.com/wallpaper/263/438/HD-wallpaper-splash-black-heart-purple.jpg");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
    }}
    </style>
    """
    st.markdown(sidebar_style, unsafe_allow_html=True)

st.set_page_config(
        page_title="RADHALOVESRAJU",
        page_icon="❤️",
        layout="centered",
        initial_sidebar_state="collapsed",
    )

set_bg_hack_url()
hearts()

st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #ff000050;
    }
</style>
""", unsafe_allow_html=True)

def main():
    li = 30 * [None]
    output_area = st.empty() 
    li[28] = st.markdown("<h1 style='text-align: center; color: blue;'> <span style='color: #FF1493;'>Project:</span> Radha ❤️ Raju </h1>",unsafe_allow_html=True)
    li[15] = st.markdown("<h3 style='text-align:center; font-size:20px; text-align:center;'>Ideated & Developed By <span style='color:#8200E1  ;font-size:25px;'>Sai Kiran Patnana</span></h3>",unsafe_allow_html=True)
    li[0] =  st.markdown("<h2 style='text-align: center; color: Orange;'>Purpose of Using WhatsApp Chat Analyser</h2>", unsafe_allow_html=True)
    li[1] = st.markdown("This app is designed for fun, interest, and curiosity. "
            "Explore the insights, analyze relationships, characters, and sentiments, and enjoy the statistical breakdown "
            "of your WhatsApp chat. It's all about discovering interesting patterns and information in a playful manner.")
    li[2] = st.markdown("<h2 style='text-align: center; color: Green;'>Your Privacy is My Priority!</h2>", unsafe_allow_html=True)
    li[3] = st.markdown("I understand the importance of your privacy. Rest assured, your chat data is processed securely and locally on your device. "
            "No data is stored or sent to external servers. Feel free to use this app without any fear of loss or leakage of your chat information.")
    li[4] = st.markdown("<h2 style='text-align: center; color: Red;'>Encountered an Issue?</h2>", unsafe_allow_html=True)
    li[5] = st.markdown("In case you encounter any unexpected errors or issues, don't worry! You can try refreshing the page. "
            "If the problem persists, feel free to reach out for support.I' am here to assist you!")
    st.empty()
    # st.info('Hello Comrade, If you encountered any error when trying RadhaLovesRaju. Please report the error @6300006765 on WhatsApp!!! ⚠️')

    set_sidebar_background()
    st.sidebar.markdown("<span style='color: Blue;font-size:30px;'><b><i>:rainbow[Whatsapp Chat Analyser]</i></b></span>", unsafe_allow_html=True)
    uploaded_file = st.sidebar.file_uploader('Pick a Chat File: ')
    # st.sidebar.info('Hello Comrade, If you encountered any error when trying RadhaLovesRaju. Please report the error @6300006765 on WhatsApp!!! ⚠️')

    if uploaded_file is not None:

        person1,person2,chat,df = get_preprocessed_data(uploaded_file)
        rel,a,b,aoc,soc = get_insights_from_chat(person1,person2,chat)
        num_messages,num_words,num_media,num_urls,num_emojis,messages,emojis = fetch_chat_stats(df)
        wordcloud_plotpath = fetch_wordcloud(messages)
        activechatter_plotpath = fetch_activechatter(df)
        topchatwords_plotpath = fetch_topchatwords(df,emojis)
        df1,topchatemojis_plotpath = fetch_topchatemojis(emojis)
        chatactivitybymonth_plotpath = fetch_chatactivitybymonth(df)
        chatactivitybyday_plotpath = fetch_chatactivitybyday(df)
            
        options = [

            f'Relationship',
            f'Character of {person1}',
            f'Character of {person2}',
            'Sentiment Analysis of Conversation',
            'Summary of Conversation',
            'Basic Chat Statistics',
            'Word Cloud',
            'Most Active Chatter',
            'Top Chat Words',
            'Top Chat Emojis',
            'Chat Activity By Month',
            'Chat Activity By Day',
            'Exit',
        ]

        selected_option = st.sidebar.selectbox('Try Out Your Desired Feature ', options)

        if selected_option == 'Exit':
            st.sidebar.warning('You selected Exit. Analysis completed, Thanks 🙏 for trying!')

        else:
            output_area.empty() 
            st.empty()
            for i in li:
                if i is not None:
                    i.empty()
            if selected_option == f"Relationship":
                # output_area.markdown(f"<h1 style='text-align: center; color: Blue;'>:rainbow[Relationship Between {person1} and {person2}]</h1>", unsafe_allow_html=True)
                output_area.title(f":rainbow[Relationship Between {person1} and {person2}]")
                for i in rel:
                    if ':' in i:
                        st.header(i[:i.index(':')])
                        st.markdown(f"<span style='font-size:20px;'><i>{i[i.index(':')+1:]}</i></span>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<span style='font-size:25px;'><i>{i}</i></span>", unsafe_allow_html=True)

            elif selected_option == f"Character of {person1}":
                output_area.markdown(f"<h1 style='text-align: center; color: Blue;'>:rainbow[Character Analysis Of {person1}]</h1>", unsafe_allow_html=True)
                output_area.title(f":rainbow[Character Analysis Of {person1}]")
                for i in a:
                    if ':' in i:
                        st.header(i[:i.index(':')])
                        st.markdown(f"<span style='font-size:20px;'><i>{i[i.index(':')+1:]}</i></span>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<span style='font-size:25px;'><i>{i}</i></span>", unsafe_allow_html=True)

            elif selected_option == f'Character of {person2}':
                # output_area.markdown(f"<h1 style='text-align: center; color: Blue;'>:rainbow[Character Analysis Of {person2}]</h1>", unsafe_allow_html=True)
                output_area.title(f":rainbow[Character Analysis Of {person2}]")
                for i in b:
                    if ':' in i:
                        st.header(i[:i.index(':')])
                        st.markdown(f"<span style='font-size:20px;'><i>{i[i.index(':')+1:]}</i></span>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<span style='font-size:25px;'><i>{i}</i></span>", unsafe_allow_html=True)

            elif selected_option == 'Sentiment Analysis of Conversation':
                # output_area.markdown("<h1 style='text-align: center; color: Blue;'>:rainbow[Sentiment Analysis Of The Conversation]</h1>", unsafe_allow_html=True)
                output_area.title(f":rainbow[Sentiment Analysis Of The Conversation]")
                for i in aoc:
                    if ':' in i:
                        st.header(i[:i.index(':')])
                        st.markdown(f"<span style='font-size:20px;'><i>{i[i.index(':')+1:]}</i></span>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<span style='font-size:25px;'><i>{i}</i></span>", unsafe_allow_html=True)

            elif selected_option == 'Summary of Conversation':
                # output_area.markdown("<h1 style='text-align: center; color: Blue;'>:rainbow[Summary Of The Conversation]</h1>", unsafe_allow_html=True)
                output_area.title(f":rainbow[Summary Of The Conversation]")
                for i in soc:
                    if ':' in i:
                        st.header(i[:i.index(':')])
                        st.markdown(f"<span style='font-size:20px;'><i>{i[i.index(':')+1:]}</i></span>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<span style='font-size:25px;'><i>{i}</i></span>", unsafe_allow_html=True)

            elif selected_option == 'Basic Chat Statistics':
                # output_area.markdown("<h1 style='text-align: center; color: Blue;'>:rainbow[Basic Chat Statistics]</h1>", unsafe_allow_html=True)
                output_area.title(f":rainbow[Basic Chat Statistics]")
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.title('Total Texts')
                    st.header(num_messages)
                with col2:
                    st.title('Total Words')
                    st.header(num_words)
                with col3:
                    st.title('Total Media')
                    st.header(num_media)
                with col4:
                    st.title('Total Urls')
                    st.header(num_urls)
                with col5:
                    st.title('Total Emojis')
                    st.header(num_emojis)

            elif selected_option == 'Word Cloud':
                # output_area.markdown("<h1 style='text-align: center; color: Blue;'>:rainbow[Word Cloud]</h1>", unsafe_allow_html=True)
                output_area.title(f":rainbow[Word Cloud]")
                st.image(wordcloud_plotpath,width=700)
            
            elif selected_option == 'Most Active Chatter':
                # output_area.markdown("<h1 style='text-align: center; color: Blue;'>:rainbow[Most Active Chatter]</h1>", unsafe_allow_html=True)
                output_area.title(f":rainbow[Most Active Chatter]")
                st.image(activechatter_plotpath)
            
            elif selected_option == 'Top Chat Words':
                # output_area.markdown("<h1 style='text-align: center; color: Blue;'>:rainbow[Top Chat Words]</h1>", unsafe_allow_html=True)
                output_area.title(f":rainbow[Top Chat Words]")
                st.image(topchatwords_plotpath)
            
            elif selected_option == 'Top Chat Emojis':
                # output_area.markdown("<h1 style='text-align: center; color: Blue;'>:rainbow[Top Chat Emojis]</h1>", unsafe_allow_html=True)
                output_area.title(f":rainbow[Top Chat Emojis]")
                st.dataframe(df1)

            elif selected_option == 'Chat Activity By Month':
                # output_area.markdown("<h1 style='text-align: center; color: Blue;'>:rainbow[Chat Activity By Month]</h1>", unsafe_allow_html=True)
                output_area.title(f":rainbow[Chat Activity By Month]")
                st.image(chatactivitybymonth_plotpath)
            
            elif selected_option == 'Chat Activity By Day':
                # output_area.markdown("<h1 style='text-align: center; color: Blue;'>:rainbow[Chat Activity By Day]</h1>", unsafe_allow_html=True)
                output_area.title(f":rainbow[Chat Activity By Day]")
                st.image(chatactivitybyday_plotpath)

    st.sidebar.markdown("<span style='font-size:25px; color:blue;'><b><i>:rainbow[- Ideated & Developed by] <br> <span style='color:white'>:rainbow[Sai Kiran Patnana]</span></i></b></span>", unsafe_allow_html=True)

    button_col1, button_col2, button_col3 = st.sidebar.columns(3)
    if button_col1.button(':rainbow[Help]'):
        output_area.empty()
        st.empty()
        for i in li:
            if i is not None:
                i.empty()
        # li[6] = output_area.markdown(f"<h1 style='text-align: center; color: Blue;'>:rainbow[Welcome to WhatsApp Chat Analyser!]</h1>", unsafe_allow_html=True)
        li[6] = output_area.title(":rainbow[Welcome to WhatsApp Chat Analyser!]")
        li[7] = st.markdown("### :rainbow[How to Use:]")
        li[8] = st.markdown('1. Export your desired WhatsApp chat.')
        li[9] = st.image('trash/export-whatsapp.jpg', width=500)
        li[9] = st.markdown("2. Upload your WhatsApp chat file.")
        li[10] = st.image('trash/puttingchat.jpg', width=500)
        li[11] = st.markdown("3. Select the desired feature from the sidebar.")
        li[12] = st.markdown("4. Explore insights and statistics about the chat.")
        li[13] = st.markdown("5. You can view Relationship Analysis, Character Analysis, Sentiment Analysis, "
                    "Word Cloud, and more!")
        

    if button_col2.button(':rainbow[Contact]'):
        output_area.empty()
        st.empty()
        for i in li:
            if i is not None:
                i.empty()
        # li[14] = st.markdown("<h1 style='text-align: center; color: Blue;'>Contact Information</h1>", unsafe_allow_html=True)
        li[14] = st.markdown(":rainbow[Contact Information]")
        # li[15] = st.markdown("<span style='font-size:20px'>:rainbow[Ideated & Developed By] <span style='color:green;font-size:25px;'>Sai Kiran Patnana</span></span>",unsafe_allow_html=True)
        li[15] = st.markdown(":rainbow[Ideated & Developed By Sai Kiran Patnana]")
        li[16] = st.header(':rainbow[Contact Details:]')
        li[17] = st.write("- **WhatsApp:** 6300006765")
        li[18] = st.write("- **Email:** saikiranpatnana5143@gmail.com")
        li[19] = st.header('Connect on Social Media:')
        li[20] = st.markdown("[LinkedIn Profile](https://www.linkedin.com/in/sai-kiran-patnana-55170a25b/)")
        li[21] = st.markdown("[GitHub Profile](https://github.com/SAIKIRANPATNANA)")
        li[22] = st.markdown("<span style='font-size:25px; color:blue;'><b><i>Feel free to reach out for any queries or collaborations!</i></b></span>",
                    unsafe_allow_html=True)
    
    if button_col3.button(':rainbow[Feedback]'):
        output_area.empty()
        st.empty()
        for i in li:
            if i is not None:
                i.empty()
        # li[23] = st.markdown("<h1 style='text-align: center; color: Blue;'>Feedback Section</h1>", unsafe_allow_html=True)
        li[23] = st.markdown(":rainbow[Feedback Section]")
        li[24] = feedback_form = st.form(key="feedback_form")
        li[25] = user_name = feedback_form.text_input("Your Name", help="Enter your name")
        li[26] = feedback_message = feedback_form.text_area("Feedback", help="Share your thoughts and suggestions")
        li[27] = submit_feedback = feedback_form.form_submit_button("Submit Feedback")


if __name__ == "__main__":
    main()