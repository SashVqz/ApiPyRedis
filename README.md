This project demonstrates the usage of Redis for user management, session handling, and priority queueing. The application manages user registration, login, session tokens, and simulates a priority-based help request system using Redis as the database.

## Features

- **User Management:**
  - Register new users with their SSN, name, password, and role.
  - Update user information.
  - Retrieve user information by SSN.

- **Authentication:**
  - Login users with SSN and password.
  - Generate and validate session tokens with expiration.
  - Role-based access using session tokens.

- **Priority Queue System:**
  - Register help requests with user priority.
  - Process and attend to the highest priority requests.

## Redis Data Structure Usage

- **Hashes:** User data is stored in a Redis hash (`users`) with the SSN as the key.
- **Strings:** Session tokens are stored as strings with expiration.
- **Sorted Sets:** Help requests are stored in a sorted set (`requests`), prioritized by the `priority` score.

## Ensure the Redis server is running:
    ```bash
    redis-server
    ```    
Redis server running locally on localhost:6379
