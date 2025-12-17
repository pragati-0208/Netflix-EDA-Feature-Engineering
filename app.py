# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt

# # Load data
# df = pd.read_csv('data/netflix_titles.csv')

# # Preprocessing
# df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
# df['year_added'] = df['date_added'].dt.year

# # Year filter
# min_year = int(df['year_added'].min())
# max_year = int(df['year_added'].max())

# selected_year = st.sidebar.slider(
#     "Select Year Added",
#     min_year,
#     max_year,
#     (min_year, max_year)
# )

# df = df[
#     (df['year_added'] >= selected_year[0]) &
#     (df['year_added'] <= selected_year[1])
# ]


# st.title("📺 Netflix Content Dashboard")

# # Sidebar filters
# content_type = st.sidebar.selectbox("Select Type", ['All', 'Movie', 'TV Show'])

# if content_type != 'All':
#     df = df[df['type'] == content_type]

# # Metrics
# st.metric("Total Titles", len(df))

# # Movies vs TV Shows
# type_count = df['type'].value_counts()

# fig, ax = plt.subplots()
# type_count.plot(kind='bar', ax=ax)
# ax.set_title("Movies vs TV Shows")
# st.pyplot(fig)

# st.subheader("🌍 Top Countries")

# country_df = df['country'].dropna().str.split(', ').explode()
# top_countries = country_df.value_counts().head(10)

# fig2, ax2 = plt.subplots()
# top_countries.plot(kind='bar', ax=ax2)
# ax2.set_xlabel("Country")
# ax2.set_ylabel("Number of Titles")
# st.pyplot(fig2)



# st.subheader("🎭 Top Genres")

# genre_df = df['listed_in'].dropna().str.split(', ').explode()
# top_genres = genre_df.value_counts().head(10)

# fig3, ax3 = plt.subplots()
# top_genres.plot(kind='barh', ax=ax3)
# ax3.set_xlabel("Number of Titles")
# st.pyplot(fig3)




# import streamlit as st
# import pandas as pd
# import plotly.express as px

# from sklearn.linear_model import LinearRegression
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import LabelEncoder

# # ---------------- PAGE CONFIG ----------------
# st.set_page_config(
#     page_title="Netflix Content Intelligence",
#     layout="wide"
# )

# # ---------------- LOAD DATA ----------------
# @st.cache_data
# def load_data():
#     return pd.read_csv("data/netflix_titles.csv")

# df = load_data()

# # ---------------- FEATURE ENGINEERING ----------------
# df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
# df['year_added'] = df['date_added'].dt.year
# df = df.dropna(subset=['year_added'])
# df['year_added'] = df['year_added'].astype(int)

# # Extract duration value
# df['duration_value'] = df['duration'].str.extract('(\d+)')
# df['duration_value'] = pd.to_numeric(df['duration_value'], errors='coerce')

# # ---------------- SIDEBAR FILTERS ----------------
# st.sidebar.header("🎛️ Filters")

# content_type = st.sidebar.selectbox(
#     "Content Type",
#     ["All", "Movie", "TV Show"]
# )

# if content_type != "All":
#     df = df[df['type'] == content_type]

# min_year, max_year = int(df['year_added'].min()), int(df['year_added'].max())
# year_range = st.sidebar.slider(
#     "Year Added",
#     min_year, max_year, (min_year, max_year)
# )

# df = df[
#     (df['year_added'] >= year_range[0]) &
#     (df['year_added'] <= year_range[1])
# ]

# # ---------------- TITLE ----------------
# st.title("📺 Netflix Content Intelligence Dashboard")

# # ---------------- METRICS ----------------
# col1, col2, col3 = st.columns(3)

# col1.metric("Total Titles", len(df))
# col2.metric("Movies", (df['type'] == "Movie").sum())
# col3.metric("TV Shows", (df['type'] == "TV Show").sum())

# # ---------------- TABS ----------------
# tab1, tab2, tab3 = st.tabs(["📊 Analysis", "🌍 Insights", "🤖 ML Prediction"])

# # ================= TAB 1: ANALYSIS =================
# with tab1:
#     st.subheader("Movies vs TV Shows")
#     fig1 = px.bar(
#         df['type'].value_counts(),
#         labels={'index': 'Type', 'value': 'Count'},
#         title="Content Type Distribution"
#     )
#     st.plotly_chart(fig1, use_container_width=True)

#     st.subheader("Top Countries")
#     country_df = df['country'].dropna().str.split(', ').explode()
#     top_countries = country_df.value_counts().head(10)

#     fig2 = px.bar(
#         top_countries,
#         labels={'index': 'Country', 'value': 'Titles'},
#         title="Top 10 Countries"
#     )
#     st.plotly_chart(fig2, use_container_width=True)

#     st.subheader("Top Genres")
#     genre_df = df['listed_in'].dropna().str.split(', ').explode()
#     top_genres = genre_df.value_counts().head(10)

#     fig3 = px.bar(
#         top_genres,
#         orientation='h',
#         labels={'index': 'Genre', 'value': 'Titles'},
#         title="Top 10 Genres"
#     )
#     st.plotly_chart(fig3, use_container_width=True)

# # ================= TAB 2: INSIGHTS =================
# with tab2:
#     st.markdown("""
#     ### 📌 Key Insights
#     - Netflix content is dominated by Movies, but TV Shows have longer engagement.
#     - The United States and India are the largest content contributors.
#     - Drama-based and International genres dominate the catalog.
#     - Netflix has increasingly diversified its content globally over time.
#     """)

# # ================= TAB 3: ML PREDICTION =================
# with tab3:
#     st.subheader("🎯 Predict Content Duration (Linear Regression)")

#     ml_df = df[['release_year', 'rating', 'duration_value']].dropna()

#     # Encode rating
#     le = LabelEncoder()
#     ml_df['rating'] = le.fit_transform(ml_df['rating'])

#     X = ml_df[['release_year', 'rating']]
#     y = ml_df['duration_value']

#     X_train, X_test, y_train, y_test = train_test_split(
#         X, y, test_size=0.2, random_state=42
#     )

#     model = LinearRegression()
#     model.fit(X_train, y_train)

#     accuracy = model.score(X_test, y_test)

#     st.write(f"📈 Model R² Score: **{accuracy:.2f}**")

#     year_input = st.slider("Release Year", 1980, 2024, 2018)
#     rating_input = st.selectbox("Rating", le.classes_)

#     rating_encoded = le.transform([rating_input])[0]

#     prediction = model.predict([[year_input, rating_encoded]])[0]

#     st.success(f"🎬 Predicted Duration: **{int(prediction)} minutes**")




import streamlit as st

st.set_page_config(
    page_title="Netflix Content Intelligence",
    layout="wide"
)

st.title("🎬 Netflix Content Intelligence Platform")

st.markdown("""
### 📌 About This Project

This interactive analytics platform explores Netflix content using:
- Exploratory Data Analysis (EDA)
- Interactive visualizations
- Time-based trend analysis
- Machine Learning (Linear Regression)

Use the navigation menu on the **left sidebar** to explore:
- 📊 **Dashboard** – Content growth & trends
- 🌍 **Insights** – Business-focused conclusions
- 🤖 **ML Model** – Duration prediction with explainability
""")

st.info(
    "Built using Python, Pandas, Plotly, Streamlit, and Scikit-learn"
)
