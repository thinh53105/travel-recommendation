# Travel Recommendations API
API for getting recommendations place to travel in a country with specific season.

## How to run the application
Create `.env` file at the root level of the project. Then fill your `OPENAI_API_KEY`. For example:

```
OPENAI_API_KEY=mock_key
```

Make sure you have `Docker` and `Docker Compose` installed. To start the application, run:
```
docker-compose up --build
```
Wait to all services completely start up. Then go to `http://localhost:3000/api/docs` to see the Swagger UI.