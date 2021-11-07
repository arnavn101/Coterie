# Coterie
Coterie is a social media app that promotes in-person socialization. Based on shared interests, it smartly matches people using ML models. Using peripheral data such as location and bluetooth, we build a deep understanding of an individual’s interests beyond what is noticeable.

![Coterie](backEnd/docs/Project-Banner.png)

## What it does
Coterie offers a way to analyze and store interests of an individual. Over time, the application ascertains the major interests of users, connecting them more deeply to others based on their frequent locations and similar interests.

## Technologies we used:
- HTML/CSS
- Javascript
- React
- SQL
- Python
- Django
- AI/Machine Learning

## Tech Stack:
- Backend: Digital Ocean, Google Places API (Cloud), Django, PostgreSQL, Facebook Faiss, fastText

- Frontend: React Native with Expo Framework

## How to Run
____
### Frontend

Steps:
```bash
cd frontEnd/
npm install expo-cli
npm install .
expo start
```
____
### Backend
Steps:
```bash
cd backEnd/
pip3 install -r requirements.txt
./django_start.sh
```
## API Spec Sneak Peak
![Coterie](/docs/endpoints_sneak_peak.png)

Full version at: [endpoints.md](/backEnd/docs/endpoints.md)
