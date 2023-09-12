import streamlit as st
import sqlite3
from streamlit import SessionState

# Initialize the SQLite database for comments
conn_comments = sqlite3.connect('comments.db')
c_comments = conn_comments.cursor()

# Initialize the SQLite database for user data
conn_users = sqlite3.connect('user_data.db')
c_users = conn_users.cursor()

# Initialize session state for user authentication
session_state = SessionState.get(user_authenticated=False)

# Streamlit app title and layout
st.title("Trending News Summarizer & Fake News Detector")

# Function to fetch and summarize trending news
def fetch_and_summarize_news():
    st.header("Trending News")
    news_url = "https://example.com"  # Replace with your news source URL

    # Fetch news data from the URL
    response = requests.get(news_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract headlines and article URLs
    headlines = [headline.text for headline in soup.find_all('h2')]
    article_urls = [url.a['href'] for url in soup.find_all('div', class_='article')]

    # Display summarized news articles
    with st.beta_expander("Read More"):
        for i, headline in enumerate(headlines):
            st.subheader(headline)
            st.write(f"Source: {news_url}")
            st.write(f"URL: {article_urls[i]}")

# Function to display and add comments
def display_and_add_comments(article_url):
    st.header("Comments and Discussion")
    comments = c_comments.execute("SELECT * FROM comments WHERE article_url=?", (article_url,))
    
    for comment in comments:
        st.write(f"User: {comment[1]}")
        st.write(f"Comment: {comment[2]}")

    user_comment = st.text_input("Add your comment:")
    if st.button("Submit Comment"):
        c_comments.execute("INSERT INTO comments (article_url, user, comment) VALUES (?, ?, ?)", (article_url, 'User123', user_comment))
        conn_comments.commit()

# Function for user login
def user_login():
    st.header("User Authentication")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Retrieve user data from the database based on the username
        user_data = c_users.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        if user_data and check_password(password, user_data[1]):
            st.session_state.user_authenticated = True

# Function for email newsletter signup
def email_signup():
    st.header("Email Newsletter Signup")
    email = st.text_input("Email Address")
    if st.button("Subscribe"):
        # Add code to subscribe the email address to the newsletter
        st.success("Subscribed successfully! You'll receive our newsletter.")

# Function to detect fake news
def detect_fake_news():
    st.header("Fake News Detector")
    user_url = st.text_input("Enter a URL to check for fake news")
    if st.button("Check for Fake News"):
        # Load the fake news detection model (you may need to install transformers)
        fake_news_classifier = pipeline("text-classification", model="facebook/bart-large-mnli")
        result = fake_news_classifier(user_url)
        st.write(f"Fake News Detection Result: {result[0]['label']}")

def add_to_reading_list(user_id, article_url):
    c_users.execute("INSERT INTO reading_list (user_id, article_url) VALUES (?, ?)", (user_id, article_url))
    conn_users.commit()

# Function to display the reading list
def display_reading_list(user_id):
    st.header("Reading List")
    reading_list = c_users.execute("SELECT article_url FROM reading_list WHERE user_id=?", (user_id,))
    
    for row in reading_list:
        st.write(f"URL: {row[0]}")

# Function to add articles to bookmarks
def add_to_bookmarks(user_id, article_url):
    c_users.execute("INSERT INTO bookmarks (user_id, article_url) VALUES (?, ?)", (user_id, article_url))
    conn_users.commit()

# Function to display bookmarks
def display_bookmarks(user_id):
    st.header("Bookmarks")
    bookmarks = c_users.execute("SELECT article_url FROM bookmarks WHERE user_id=?", (user_id,))
    
    for row in bookmarks:
        st.write(f"URL: {row[0]}")

def search_articles(keyword):
    st.header("Search News Articles")
    keyword = st.text_input("Enter a keyword to search for articles")

    if st.button("Search"):
        # Perform a search for articles containing the keyword
        # You can implement this search logic based on your data source
        # and the structure of your news articles
        # For simplicity, we'll assume a list of articles for demonstration
        articles = [
            {"title": "Article 1", "url": "https://example.com/article1"},
            {"title": "Article 2", "url": "https://example.com/article2"},
            # Add more articles as needed
        ]

        # Display the search results
        for article in articles:
            st.subheader(article["title"])
            st.write(f"URL: {article['url']}")

# Main application
if __name__ == "__main__":
    fetch_and_summarize_news()
    user_login()
    email_signup()
    user_url = st.text_input("Enter a URL to check for fake news")
    if st.button("Check for Fake News"):
        detect_fake_news()
    if st.session_state.user_authenticated:  # Check authentication state using st.session_state
        display_and_add_comments(user_url)
        
        # Add to Reading List button
        if st.button("Add to Reading List"):
            add_to_reading_list("User123", user_url)
        
        # Display Reading List
        display_reading_list("User123")
        
        # Add to Bookmarks button
        if st.button("Add to Bookmarks"):
            add_to_bookmarks("User123", user_url)
        
        # Display Bookmarks
        display_bookmarks("User123")
        
        # Search for articles by keyword
        search_articles(user_url)
    else:
        st.warning("Please log in to leave comments or use the reading list, bookmarks, or search.")
