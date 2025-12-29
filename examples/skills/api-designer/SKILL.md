---
name: api-designer
description: Design RESTful APIs with proper endpoints, request/response schemas, and documentation. Use when the user wants to "design an API", "create endpoints", "add API routes", or discusses REST API structure.
allowed-tools: Read, Write, Glob, Grep
---

# API Designer

## RESTful Endpoint Conventions

### URL Structure
```
/api/v1/{resource}              # Collection
/api/v1/{resource}/{id}         # Single item
/api/v1/{resource}/{id}/{sub}   # Nested resource
```

### HTTP Methods

| Method | Purpose | Example | Response |
|--------|---------|---------|----------|
| GET | Read | `GET /users` | 200 + data |
| POST | Create | `POST /users` | 201 + created item |
| PUT | Replace | `PUT /users/123` | 200 + updated item |
| PATCH | Partial update | `PATCH /users/123` | 200 + updated item |
| DELETE | Remove | `DELETE /users/123` | 204 No Content |

### Naming Rules

- Use plural nouns: `/users` not `/user`
- Use kebab-case: `/user-profiles` not `/userProfiles`
- Avoid verbs in URLs: `/users/123/activate` → `POST /users/123/activation`
- Use query params for filtering: `/users?status=active&role=admin`

## Request/Response Design

### Standard Response Envelope
```json
{
  "data": { ... },
  "meta": {
    "timestamp": "2024-01-15T10:30:00Z",
    "requestId": "abc-123"
  }
}
```

### Collection Response (with pagination)
```json
{
  "data": [
    { "id": 1, "name": "Item 1" },
    { "id": 2, "name": "Item 2" }
  ],
  "meta": {
    "total": 100,
    "page": 1,
    "perPage": 20,
    "totalPages": 5
  },
  "links": {
    "self": "/api/v1/items?page=1",
    "next": "/api/v1/items?page=2",
    "last": "/api/v1/items?page=5"
  }
}
```

### Error Response
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Must be a valid email address"
      }
    ]
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00Z",
    "requestId": "abc-123"
  }
}
```

## HTTP Status Codes

### Success
| Code | When to Use |
|------|-------------|
| 200 | Successful GET, PUT, PATCH |
| 201 | Successful POST (resource created) |
| 204 | Successful DELETE (no content) |

### Client Errors
| Code | When to Use |
|------|-------------|
| 400 | Invalid request body/params |
| 401 | Not authenticated |
| 403 | Authenticated but not authorized |
| 404 | Resource not found |
| 409 | Conflict (duplicate, state conflict) |
| 422 | Validation error |
| 429 | Rate limit exceeded |

### Server Errors
| Code | When to Use |
|------|-------------|
| 500 | Unexpected server error |
| 502 | Bad gateway (upstream failed) |
| 503 | Service unavailable |

## API Documentation Template

For each endpoint, document:

```markdown
## Create User

Creates a new user account.

**Endpoint:** `POST /api/v1/users`

**Authentication:** Required (Bearer token)

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email | string | Yes | Valid email address |
| name | string | Yes | 2-100 characters |
| role | string | No | One of: user, admin. Default: user |

**Example Request:**
```json
{
  "email": "john@example.com",
  "name": "John Doe",
  "role": "user"
}
```

**Success Response:** `201 Created`
```json
{
  "data": {
    "id": 123,
    "email": "john@example.com",
    "name": "John Doe",
    "role": "user",
    "createdAt": "2024-01-15T10:30:00Z"
  }
}
```

**Error Responses:**
- `400 Bad Request` - Invalid JSON
- `401 Unauthorized` - Missing/invalid token
- `409 Conflict` - Email already exists
- `422 Unprocessable Entity` - Validation failed
```

## OpenAPI/Swagger Spec

```yaml
openapi: 3.0.3
info:
  title: User API
  version: 1.0.0

paths:
  /users:
    get:
      summary: List users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: status
          in: query
          schema:
            type: string
            enum: [active, inactive]
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'

    post:
      summary: Create user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          description: Created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
        email:
          type: string
          format: email
        name:
          type: string
        createdAt:
          type: string
          format: date-time
```

## Security Considerations

### Authentication
- Use Bearer tokens in Authorization header
- Implement token refresh mechanism
- Set appropriate token expiry

### Input Validation
- Validate all input on server side
- Sanitize strings to prevent injection
- Limit request body size

### Rate Limiting
- Return `429` with `Retry-After` header
- Different limits for authenticated/anonymous

### CORS
- Whitelist specific origins in production
- Limit allowed methods and headers

## Versioning Strategy

### URL Versioning (Recommended)
```
/api/v1/users
/api/v2/users
```

### Header Versioning
```
Accept: application/vnd.myapi.v1+json
```

When to create new version:
- Breaking changes to response structure
- Removing fields
- Changing field types
- Changing authentication method
