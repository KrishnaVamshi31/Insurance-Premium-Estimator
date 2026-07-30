# 🏥 Insurance Premium Estimator

A Machine Learning-powered web application built with **FastAPI** that predicts an individual's insurance premium based on personal and health-related attributes. The project demonstrates how a trained ML model can be deployed as a REST API with input validation and automated testing.

---

## 📌 Features

* Predicts insurance premiums using a trained Machine Learning model.
* FastAPI-powered REST API.
* Input validation using **Pydantic**.
* Pre-trained model loaded for real-time predictions.
* Unit tests for API reliability.
* Lightweight and easy to deploy.

---

## 🛠️ Tech Stack

* **Python**
* **FastAPI**
* **Scikit-learn**
* **Pandas**
* **NumPy**
* **Pydantic**
* **Uvicorn**
* **Pytest**

---

## 📂 Project Structure

```text
Insurance-Premium-Estimator/
│── Model/
│   └── model.pkl          # Trained Machine Learning model
│
│── tests/                 # Unit tests
│
│── app.py                 # FastAPI application
│── requirements.txt       # Project dependencies
│── .gitignore
│── README.md
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/KrishnaVamshi31/Insurance-Premium-Estimator.git
cd Insurance-Premium-Estimator
```

Create a virtual environment:

```bash
python -m venv myenv
```

Activate the environment:

**Windows**

```bash
myenv\Scripts\activate
```

**Linux / macOS**

```bash
source myenv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

Start the FastAPI server:

```bash
uvicorn app:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

* Swagger UI: `http://127.0.0.1:8000/docs`
* ReDoc: `http://127.0.0.1:8000/redoc`

---

## 📥 Example Request

```json
{
  "age": 35,
  "sex": "male",
  "bmi": 28.5,
  "children": 2,
  "smoker": "no",
  "region": "southeast"
}
```

---

## 📤 Example Response

```json
{
  "predicted_premium": 12453.72
}
```

> The exact response depends on the trained model.

---

## 🧪 Running Tests

Execute the test suite using:

```bash
pytest
```

---

## 📈 Future Improvements

* Docker containerization
* Cloud deployment (Render, Railway, AWS, Azure)
* Model versioning
* CI/CD using GitHub Actions
* User-friendly frontend
* Improved feature engineering and model evaluation

---

## 🎯 Learning Outcomes

This project helped reinforce concepts such as:

* Building REST APIs with FastAPI
* Deploying Machine Learning models
* Request validation using Pydantic
* Loading serialized models
* API testing with Pytest
* Structuring production-ready Python projects

---

## 📜 License

This project is created for learning and educational purposes.
