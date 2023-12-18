# Base Requirements:

Website:

- Frontend should be done using vanilla Javascript.

- Website should be a single-page application.

- Must be compatible with latest version of Google Chrome.

- No errors.

- Everything must be launched with a single command (i.e.: docker compose up --build -d).


Game:

- Users should be able to play the game with eachother in the same keyboard.

- Implement a tournament.

- Tournament registration (each user must input an alias name). (can be modified using the Standard User Management module.)

- There must be a matchmaking system: the tournament system organizes the matchmaking of the participants, and announce the next game.

- Both playes and AI must have identical paddle speed.

- Game should be developed according to the frontend rules above(Vanilla JS), this may be overwritten by Frontend Module or Graphics module.


Security:

- Passwords must be hashed in the DB (password.field in Django).

- Must be protected against SQL injections/XSS.

- If you have a backend or any other features, it is mandatory to enable an HTTPS connection for all aspects (Utilize wss instead of ws).

- Implemente form validators in the backend.


# Modules:

To get 100% on the project we are required to complete a minimum of 7 Major modules (2 Minor modules = 1 Major module).

- Web:
    - Major module - Use Backend Framework (Djando) - 1 point.
    - Minor module - Use Frontend Framework or toolkit(Bootstrap) - 0.5 points.
    - Minor module - Use backend Database (Postgres)  - 0.5 points.
    - Major module - store tournament results in the Blockchain - 1 point.

- User Managemente:
    - Major module - Standard user management, auth, users across tournaments - 1 point.
    - Major module - Implement remote auth - 1 point.


- Gameplay and user experience:
    - Major module - Remote players - 1 point.
    - Major module - Multiplayers (more than 2 in the same game) - 1 point.
    - Major module - Add Another Game with User History and Matchmaking - 1 point.
    - Minor module- Game Customization Options - 0.5 points.
    - Major module - Live chat - 1 point.

- AI-Algo:
    - Major module -  Introduce an AI Opponent - 1 point.
    - Minor module -  User and Game Stats Dashboards - 0.5 points.

- Cybersecurity:
    - Major module - Implement WAF/ModSecurity with Hardened Configuration and HashiCorp Vault for Secrets Management - 1 point.
    - Minor module - GDPR Compliance Options with User Anonymization, Local Data Management, and Account Deletion - 0.5 point.
    - Major module - Implement Two-Factor Authentication (2FA) and JWT - 1 point.

- Devops:
    - Major module - Infrastructure Setup for Log Management - 1 point. 
    - Minor module - Monitoring system - 0.5 point.
    - Major module - Designing the Backend as Microservices - 1 point.

- Graphics:
    - Major module - Use of advanced 3D techniques - 1 point.

- Accessibility:
    - Minor module - Support on all devices - 0.5 point.
    - Minor module - Expanding Browser Compatibility - 0.5 point.
    - Minor module - Multiple language supports - 0.5 point.
    - Minor module - Add accessibility for Visually Impaired Users - 0.5 point.
    - Minor module - Server-Side Rendering (SSR) Integration - 0.5 point.

- Server-Side Pong:
    - Major module - Replacing Basic Pong with Server-Side Pong and Implementing an API - 1 point.
    - Major module - Enabling Pong Gameplay via CLI against Web Users with API Integration - 1 point.


# Chosen Modules

Module points count 5 / 7

## Web

- Use Framework as backend (Django). 1 point

- Use a Front-end framework or toolkit (Bootstrap). 0.5 points.

- Use database for backend (Postgres).  0.5 points.

## User Management

- OAuth 2.0 authentication with 42 (?). 1 point

## Gameplay and user experience

## Cybersecurity

- Implement Two-Factor Authentication (2FA) and JWT. (?). 1 point

## Devops

- Infrastructure Setup with ELK. 1 point.

- Monitoring System (grafana/prometheus) 0.5 points.

- Designing the Backend as Microservices (multiple apps / REST api). 1 point.

## Graphics

-  Implementing Advanced 3D Techniques(ThreeJS/WebGL) 1point

## Accessability

- Expanding Browser Compatibility. (brave or firefox). 0.5points.