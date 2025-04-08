# 🎬 Movie Recommender System

This is a **Content-Based Movie Recommendation System** that suggests similar movies based on their descriptions using **TF-IDF vectorization** and **cosine similarity**. The backend is powered by **Flask**, and the frontend is built using **HTML, CSS, and JavaScript**.

---

## 🚀 Features

- 🤝 Recommend similar movies based on plot/overview
- 🧠 Uses **TF-IDF Vectorizer** to convert text to numeric features
- 📐 Calculates **cosine similarity** to find related movies
- 🌐 Clean and responsive frontend interface using HTML, CSS, and JS
- ⚙️ Backend API built with Flask to serve real-time recommendations

---

## 📦 Tech Stack

- **Python**
- **Flask**
- **Pandas**
- **NumPy**
- **Scikit-learn (TF-IDF & Cosine Similarity)**
- **HTML, CSS, JavaScript**
- **Pickle** (for serialized model and similarity matrix)

---

## 📁 Dataset Used

The recommender system uses a movie metadata dataset:

- `movies.csv`: Contains movie titles and overview descriptions


---

## 🧠 How It Works

### 🤝 Content-Based Filtering
1. **TF-IDF Vectorization**:
   - Applies TF-IDF to the `overview` column to convert text into vectors.
2. **Cosine Similarity**:
   - Measures similarity between movie vectors.
3. **Recommendation Logic**:
   - Given a movie, it returns the top N most similar movies based on cosine distance.

---

## 🛠️ How to Run

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/movie-recommendation-system.git
   cd movie-recommendation-system
   ```

2. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the Flask server**
   ```bash
   python app.py
   ```

4. **Open your browser and go to**
   ```
   http://localhost:5000
   ```

---

## 🖼️ Output Example

**Input Movie**: `Inception`

**Recommended Movies**:
- Interstellar
- The Prestige
- The Matrix
- Memento
- Shutter Island

Recommendations are displayed along with poster images in the frontend UI.

---

## 📌 To-Do / Improvements

- 🔍 Add autocomplete search bar
- 🖼️ Display movie posters dynamically via an API (like TMDb)
- 💾 Add user login for personalized recommendations
- ☁️ Deploy using **Render**, **Heroku**, or **Vercel**

---


If you found this project helpful, please consider giving it a ⭐️ on GitHub!

---
```

