# Authentication
This document will explain how the authentication flow will work.

## Endpoints
The authentication service has the following endpoints

| Method  | Endpoint          | Description                                                                   | Json Variables      |
| :-----: | :---------------- | :---------------------------------------------------------------------------- | :------------------ |
| `POST`  | `/login/`         | Allows logging in via username/email & password                               | `login`, `password` |
| `PATCH` | `/login/`         | Allows upgrading a temp session to an actual session if you have TOTP enabled | -                   |
| `POST`  | `/totp/`           | Creates a `session_totp`, requires at least a temp session                    | `totp_token`        |
|  `GET`  | `/oauth/callback` | The callback URL for 42 OAUTH                                                 |                     |

Current there are also 2 test endpoints (`/login/test/`, `/oauth/test`) which will show a page for testing the login features. But these should be removed once authentication pages have been made and users can authenticate via that.

## Authentication flow
For a user to authenticate they must either log in via OAUTH or using username/password. If they have TOTP enabled, they will get a session with type 'temp'. They can upgrade this to an actual session by calling `PATCH /login/` if they have a `session_totp` cookie. to obtain a `session_totp` cookie they can create a request to `POST /totp/` if they have a `session` cookie. If successful this will return a 200 OK response with a set_cookie for a new session cookie.