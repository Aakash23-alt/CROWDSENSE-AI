# CrowdSense AI API Documentation

## AI → Backend

POST /api/crowd

Example:

{
  "people_count": 150,
  "risk_level": "High",
  "timestamp": "2026-07-12T15:00:00"
}

---

## Backend → Frontend

GET /api/dashboard

Example Response

{
  "people_count":150,
  "risk_level":"High",
  "alerts":[
      "Zone A is overcrowded"
  ]
}

---

## Alert API

GET /api/alerts