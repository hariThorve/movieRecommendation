**Project Title:**  
Movie Recommendation Engine with User Sentiment & MLOps

---

## 1. Project Goal

Build an end‑to‑end production‑style system that:  
- Recommends movies to users based on their ratings and preferences.  
- Analyzes sentiment of user reviews using a transformer model.  
- Stores and serves all data via a database and REST APIs.  
- Includes basic MLOps: retraining, model versioning, and monitoring.

***

## 2. Core Functionality

### User-facing

- User registration/login.  
- Browse movies (from a public API + local DB).  
- Rate movies.  
- Get personalized movie recommendations.  
- Write text reviews for watched movies.

### Admin-facing

- View aggregated sentiment per movie (e.g., % positive/negative).  
- View top movies by rating and sentiment.  
- See basic usage stats (number of users, ratings, reviews, recommendations).

***

## 3. Data Sources

- **Movie metadata**:  
  - Ingest from TMDb API (or similar): title, genres, description/overview, cast, release year, poster path, popularity and vote stats.  
- **User interaction data** (stored in DB):  
  - Ratings: explicit 1–5 (or 0.5–5) stars.  
  - Reviews: free‑text comments for movies.  
  - Optional: clicks/views on recommended movies.

***

## 4. Database Schema (Relational, e.g., PostgreSQL)

- `users`  
  - `user_id` (PK), `name`, `email`, `created_at`, etc.

- `movies`  
  - `movie_id` (PK, TMDb ID or internal), `title`, `genres`, `description`, `cast`, `release_year`, `poster_url`, `popularity`, `vote_average`, `vote_count`, etc.

- `ratings`  
  - `user_id` (FK), `movie_id` (FK), `rating`, `timestamp`.  
  - Composite PK or unique constraint on (`user_id`, `movie_id`).

- `reviews`  
  - `review_id` (PK), `user_id` (FK), `movie_id` (FK), `review_text`, `sentiment_label`, `sentiment_score`, `timestamp`.

- `recommendations`  
  - `rec_id` (PK), `user_id` (FK), `movie_id` (FK), `score`, `model_version`, `timestamp`.

- Optional `model_metadata`  
  - `model_id`, `model_type` (recommender/sentiment), `model_version`, `train_date`, `metrics_json`, `is_production`.

***

## 5. Recommendation Module

### Inputs

- User–item interactions from `ratings`.  
- Movie content features from `movies` (genres, description, cast).

### Core methods

- **Collaborative filtering (main)**  
  - User–item rating matrix → matrix factorization (e.g., SVD/NMF/implicit ALS) to learn latent user and movie vectors.  
- **Content‑based (support/fallback)**  
  - Encode movies as vectors using:  
    - Multi‑hot genres.  
    - TF–IDF or embeddings of descriptions.  
  - Build a user profile as weighted average of liked movies’ vectors.  
  - Use cosine similarity to find similar movies.

### Cold‑start strategy

- No ratings yet:  
  - Recommend globally popular movies using dataset stats (vote_average + vote_count) and optionally filter by user‑selected genres.  
- Few ratings:  
  - Use content‑based (cosine similarity between user profile vector and movie vectors).  
- Many ratings:  
  - Collaborative filtering becomes dominant; optionally blend with content‑based.

### Scoring

- For each candidate movie \(i\) and user \(u\):  
  - \(s_{cf}(i)\) from collaborative filtering.  
  - \(s_{cb}(i)\) from content‑based similarity.  
  - Final score: \(s(i) = \alpha s_{cf}(i) + (1 - \alpha) s_{cb}(i)\), with \(\alpha\) depending on user data richness.  
- Filter out movies already rated by the user; return top‑N.

***

## 6. Sentiment Analysis Module

- Use a Transformer model (e.g., DistilBERT/BERT from Hugging Face).  
- Fine‑tune on movie‑review‑style sentiment data into 2 or 3 classes (e.g., positive/negative or positive/neutral/negative).  
- Wrap as function:  
  - `analyze_sentiment(review_text) -> (sentiment_label, sentiment_score)`  
- Store output in `reviews` table.  
- Aggregate for admin dashboard: per‑movie sentiment distribution and overall trends.

***

## 7. API Design (FastAPI Recommended)

### User APIs

- `POST /register_user`  
  - Create new user.

- `GET /movies`  
  - Paginated list of movies (with optional filters: genre, popularity).

- `POST /rate_movie`  
  - Body: `user_id`, `movie_id`, `rating`.  
  - Inserts into `ratings`.

- `GET /recommendations?user_id=...`  
  - Returns top‑N recommended movies and scores for that user.  
  - Logs results into `recommendations`.

- `POST /review`  
  - Body: `user_id`, `movie_id`, `review_text`.  
  - Runs sentiment model, stores text + label + score in `reviews`.

### Admin APIs

- `GET /sentiment_summary?movie_id=...`  
  - Returns sentiment breakdown for a movie.

- `GET /admin/top_movies`  
  - Top movies by rating and/or positive sentiment.

- `GET /admin/stats`  
  - Basic system stats: users, ratings, reviews, recommendations, model versions.

***

## 8. Pipelines & MLOps

### Training & retraining

- **Recommender training pipeline** (batch):  
  - Read `ratings` (and `movies`) from DB.  
  - Train collaborative filtering model.  
  - Evaluate (RMSE, precision@k, recall@k).  
  - Log run to MLflow (metrics, parameters, artifacts).  
  - Register new model version in model registry.

- **Sentiment model updates** (optional, less frequent):  
  - Use accumulated `reviews` + labels (or external data) to fine‑tune new sentiment model.  
  - Log and version as above.

### Scheduling

- Use cron/Airflow/Prefect to run recommender retraining weekly or when new ratings exceed a threshold.

### Serving & versioning

- API loads **current production model** based on model registry tag (e.g., `recommender:prod`).  
- Log `model_version` in `recommendations` table for each prediction.

### Monitoring & logging

- Log:  
  - Every recommendation call and movies returned.  
  - Every sentiment prediction.  
- Metrics (queried from DB or via dashboard):  
  - Number of recommendations/day, active users, ratings count.  
  - Average rating per movie; sentiment distribution per movie.  
- Basic health endpoints:  
  - `GET /health`  
  - `GET /metrics` (if using Prometheus-style metrics).

***

## 9. Tech Stack

- **Backend/API:** FastAPI (Python)  
- **Database:** PostgreSQL  
- **ML:**  
  - Recommender: scikit‑learn or implicit; optional PyTorch for advanced models.  
  - Sentiment: Hugging Face Transformers (BERT/DistilBERT).  
- **Data processing:** pandas, NumPy  
- **Experiment tracking / registry:** MLflow or Weights & Biases  
- **Containerization:** Docker (optionally Docker Compose)  
- **Orchestration (optional):** Airflow or Prefect for pipelines  
- **Monitoring (optional advanced):** Prometheus + Grafana

***
