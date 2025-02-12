import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar
st.sidebar.title("📊 WhatsApp Chat Analyzer")
st.sidebar.markdown("Upload your WhatsApp chat file (.txt) for analysis.")

uploaded_file = st.sidebar.file_uploader("Choose a file", type=["txt"])
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # Fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('Group Notification')
    user_list.sort()
    user_list.insert(0, 'Overall')

    selected_user = st.sidebar.selectbox("Select a user for analysis", user_list)

    if st.sidebar.button("Show Analysis"):
        # Main container for analysis
        st.title("WhatsApp Chat Analysis")
        st.markdown("---")

        # Chat statistics
        st.subheader("📋 Chat Statistics")
        no_of_messages, words, no_of_media_messages, no_of_links = helper.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Messages", no_of_messages, delta=None, help="Total number of messages sent")
        col2.metric("Total Words", words)
        col3.metric("Media Shared", no_of_media_messages)
        col4.metric("Links Shared", no_of_links)

        st.markdown("---")

        # Monthly timeline
        st.subheader("📅 Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig = px.line(
            timeline, x="time", y="message",
            title="Messages Over Time",
            labels={"time": "Month", "message": "Message Count"},
            template="plotly_white"
        )
        fig.update_traces(line_color="#228B22")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # Daily Timeline with Month-Year Dropdown
        st.subheader("📅 Daily Timeline")
        dailytimeline = helper.daily_timeline(selected_user, df)  

        # Plot the daily timeline
        if 1:
            fig = px.line(
                dailytimeline,
                x="online_date",
                y="message",
                title=f"Messages Over Time ",
                labels={"online_date": "Date", "message": "Message Count"},
                template="plotly_white"
            )

        fig.update_traces(line_color="#DC143C")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")


        # Most active users
        if selected_user == "Overall":
            st.subheader("👥 Active Users")
            x, per_df = helper.most_active_users(df)
            fig, ax = plt.subplots(figsize = (8,6))

            col1, col2 = st.columns([1, 1])
            
            with col1:
            # Creating a bar chart with Plotly
                fig = px.bar(
                    x=x.index,  
                    y=x.values,  
                    orientation="v",
                    title="Most Active Users",
                    labels={"x": "User", "y": "Message Count"},  
                    template="plotly_white",
                )

                fig.update_layout(
                    title_x=0.5,  
                    title_font=dict(size=18, family="Arial", color="white"),
                    xaxis_title="Most Active User",
                    yaxis_title="Number of Messages",
                    xaxis=dict(tickangle=45),  
                    bargap=0.5,  
                    bargroupgap=0.1 
                )

                fig.update_traces(marker_color='#7FFFD4')
                fig.update_layout(xaxis_title="User", yaxis_title="Message Count")
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.dataframe(per_df)

        st.markdown("---")

        # Word cloud
        st.subheader("🌥 Word Cloud")
        df_wc_fig = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots(figsize = (8,6))
        ax.imshow(df_wc_fig)
        st.pyplot(fig)


        st.markdown("---")

        # Most common words
        st.subheader("📚 Most Common Words")
        common_word_df = helper.most_common_words(selected_user, df)

        fig = px.bar(
            common_word_df,
            x='Word', y='Frequency',
            orientation="v",
            title="Top 20 Used Words",
            labels={0: "Words", 1: "Frequency"},
            template="plotly_white"
        )
        fig.update_traces(marker_color='#40E0D0')
        fig.update_layout(yaxis=dict())
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # Emoji analysis
        st.subheader("😀 Emoji Analysis")
        emoji_df = helper.emoji_count(selected_user, df)

        col1, col2 = st.columns([1, 1])

        with col1:
            st.dataframe(emoji_df)
        with col2:
            # Using Plotly for the pie chart to better render emojis
            top_emoji = emoji_df.head(8)
            fig = px.pie(top_emoji, names='Emoji', values='Count', title='Top Emojis')
            fig.update_layout(width=800, height=600)  
            st.plotly_chart(fig)

        #Activity map
        st.subheader("⛅ Weekly Activity")
        col1, col2 = st.columns([1,1])

        with col1:
            active_day = helper.week_activity(selected_user, df)
            fig = px.bar(
                active_day,
                x='Day', y='No. of Messages',
                orientation="v",
                title="Most Active Days",
                labels={0: "Day", 1: "No. of Messages"},
                template="plotly_white"
            )

            # Simple styling updates
            fig.update_layout(
                title_x=0.5,  
                title_font=dict(size=18, family="Arial", color="white"),
                xaxis_title="Day of the Week",
                yaxis_title="Number of Messages",
                xaxis=dict(tickangle=45),  
                bargap=0.5,  
                bargroupgap=0.1 
            )

            fig.update_traces(marker_color='teal')

            st.plotly_chart(fig, use_container_width=True)

        with col2:
            active_month = helper.month_activity(selected_user, df)
            fig = px.bar(
                active_month,
                x='Month', y='No. of Messages',
                orientation="v",
                title="Most Active Months",
                labels={0: "Month", 1: "No. of Messages"},
                template="plotly_white"
            )

            # Simple styling updates
            fig.update_layout(
                title_x=0.5,  
                title_font=dict(size=18, family="Arial", color="white"),
                xaxis_title="Month of the Year",
                yaxis_title="Number of Messages",
                xaxis=dict(tickangle=45),  
                bargap=0.5,  
                bargroupgap=0.1 
            )

            fig.update_traces(marker_color='coral')

            st.plotly_chart(fig, use_container_width=True)
            