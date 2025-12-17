import streamlit as st
import pandas as pd
import plotly.express as px

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score

st.title("🤖 Content Duration Prediction (Linear Regression)")

df = pd.read_csv("data/netflix_titles.csv")

# Feature engineering
df['duration_value'] = df['duration'].str.extract('(\d+)')
df['duration_value'] = pd.to_numeric(df['duration_value'], errors='coerce')

ml_df = df[['release_year', 'rating', 'duration_value']].dropna()

le = LabelEncoder()
ml_df['rating'] = le.fit_transform(ml_df['rating'])

X = ml_df[['release_year', 'rating']]
y = ml_df['duration_value']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

# Evaluation
st.metric("R² Score", round(r2_score(y_test, y_pred), 2))
st.metric("MAE (minutes)", int(mean_absolute_error(y_test, y_pred)))

# Explainability
coeff_df = pd.DataFrame({
    "Feature": X.columns,
    "Impact": model.coef_
})

fig = px.bar(
    coeff_df,
    x="Feature",
    y="Impact",
    title="Feature Impact on Duration Prediction"
)
st.plotly_chart(fig, use_container_width=True)

# What-if analysis
st.subheader("🔮 What-If Scenario")

year = st.slider("Release Year", 1980, 2024, 2020)
rating = st.selectbox("Rating", le.classes_)
rating_enc = le.transform([rating])[0]

prediction = model.predict([[year, rating_enc]])[0]

st.success(f"🎬 Predicted Duration: **{int(prediction)} minutes**")

