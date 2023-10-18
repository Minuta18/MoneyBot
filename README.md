# MoneyBot

MoneyBot is a simple economy telegram bot. I am creating this project to learn some technologies:

- [ ] Write microservices:
  - [X] Auth service
  - [ ] Balance service
  - [ ] Telegram bot service
- [X] Unit tests for at least 80% of code
- [X] Documentation of all methods using docstrings
- [X] Start using linters
- [X] Correctly configure Nginx
- [X] Docker compose
- [ ] Swagger
- [X] Asynchronous services
- [X] Restful API
- [ ] Logging
- [X] Test-driven development
- [ ] HTTPS
  
## API method list

### Create user `/api/v2/users/create`

Request body:

```json
{
    "email": string,
    "password": string
}
```

Response body:

```json
{
    "error": bool,
    "id": int,
    "email": string,
    "hashed_password": string,
    "balance": int,
}
```

Possible errors are:

```json
User with this email already exists.

```

> [!WARNING]
> This method has not been written yet

P. S. I will add more descriptions soon.
