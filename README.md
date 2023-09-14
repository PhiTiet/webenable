### GET /data
```json
{
  "daily_usage": {
    "goal": 15,
    "slope": 2,
    "history": [
      {
        "timestamp": "2023-09-14T00:00:00",
        "value": 3
      },
      {
        "timestamp": "2023-09-14T01:00:00",
        "value": 4
      }
    ],
    "unit": "Wh"
  },
  "daily_generation": {
    "goal": 10,
    "slope": 1,
    "history": [
      {
        "timestamp": "2023-09-14T13:28:28.256181",
        "value": 2.7
      },
      {
        "timestamp": "2023-09-14T14:28:28.256181",
        "value": 3.5
      }
    ],
    "unit": "Wh"
  },
  "monthly_total": {
    "goal": 70,
    "slope": 2,
    "history": [
      {
        "timestamp": "2023-09-01T00:00:00",
        "value": 3
      },
      {
        "timestamp": "2023-09-02T00:00:00",
        "value": 5
      }
    ],
    "unit": "kWh"
  }
}
```