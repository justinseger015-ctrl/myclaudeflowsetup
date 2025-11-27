# 02. API Design

## Overview
Complete API design specifications for the DAA autonomous learning system, including REST endpoints, GraphQL schema, request/response formats, authentication, versioning, and API contracts.

## Technical Requirements

### API Architecture (REQ-T051 - REQ-T060)

**REQ-T051**: RESTful API Design
**Priority**: CRITICAL
**Description**: APIs MUST follow REST principles and HTTP semantics
**Standards**: OpenAPI 3.0, JSON:API specification
**Acceptance**: All endpoints documented in OpenAPI spec

**REQ-T052**: API Versioning
**Priority**: CRITICAL
**Description**: URL-based versioning (e.g., /v1/, /v2/)
**Rationale**: Clear version boundaries, parallel versions
**Acceptance**: Multiple API versions deployable simultaneously

**REQ-T053**: Content Negotiation
**Priority**: HIGH
**Description**: Support JSON and MessagePack formats
**Headers**: Accept, Content-Type
**Acceptance**: Clients can request preferred format

**REQ-T054**: HATEOAS Links
**Priority**: MEDIUM
**Description**: Responses include navigational links
**Rationale**: API discoverability
**Acceptance**: Link relations in responses

**REQ-T055**: Pagination
**Priority**: CRITICAL
**Description**: Cursor-based pagination for collections
**Parameters**: limit (max 100), cursor
**Acceptance**: All list endpoints support pagination

**REQ-T056**: Filtering
**Priority**: HIGH
**Description**: Query parameters for resource filtering
**Format**: ?filter[field]=value
**Acceptance**: Common fields filterable

**REQ-T057**: Sorting
**Priority**: HIGH
**Description**: Multi-field sorting support
**Format**: ?sort=field1,-field2
**Acceptance**: Sort by multiple fields

**REQ-T058**: Field Selection
**Priority**: MEDIUM
**Description**: Sparse fieldsets for bandwidth optimization
**Format**: ?fields=field1,field2
**Acceptance**: Clients can select response fields

**REQ-T059**: Batch Operations
**Priority**: HIGH
**Description**: Batch create/update/delete endpoints
**Limits**: Max 100 items per batch
**Acceptance**: Atomic batch operations

**REQ-T060**: Bulk Export
**Priority**: MEDIUM
**Description**: Export large datasets asynchronously
**Formats**: JSON, CSV, Parquet
**Acceptance**: Export jobs with status tracking

### Authentication & Authorization API (REQ-T061 - REQ-T070)

**REQ-T061**: JWT Authentication
**Priority**: CRITICAL
**Description**: JWT bearer tokens for authentication
**Algorithm**: RS256 with public key verification
**Acceptance**: All protected endpoints require valid JWT

**REQ-T062**: Token Endpoint
**Priority**: CRITICAL
**Endpoint**: POST /v1/auth/token
**Grant Types**: password, refresh_token, client_credentials
**Acceptance**: Issues access and refresh tokens

**REQ-T063**: Token Refresh
**Priority**: CRITICAL
**Endpoint**: POST /v1/auth/refresh
**Description**: Exchange refresh token for new access token
**Acceptance**: Refresh without re-authentication

**REQ-T064**: Token Revocation
**Priority**: HIGH
**Endpoint**: POST /v1/auth/revoke
**Description**: Invalidate access or refresh tokens
**Acceptance**: Revoked tokens immediately invalid

**REQ-T065**: OAuth2 Integration
**Priority**: HIGH
**Providers**: Google, GitHub, Microsoft
**Flow**: Authorization Code with PKCE
**Acceptance**: Social login supported

**REQ-T066**: MFA Enrollment
**Priority**: HIGH
**Endpoint**: POST /v1/auth/mfa/enroll
**Methods**: TOTP, SMS
**Acceptance**: Users can enable MFA

**REQ-T067**: MFA Verification
**Priority**: HIGH
**Endpoint**: POST /v1/auth/mfa/verify
**Description**: Verify MFA code during login
**Acceptance**: MFA required for admin roles

**REQ-T068**: API Key Management
**Priority**: HIGH
**Endpoints**: POST/DELETE /v1/auth/api-keys
**Description**: Create and manage API keys
**Acceptance**: API keys for service accounts

**REQ-T069**: Permission Check
**Priority**: HIGH
**Endpoint**: POST /v1/auth/check-permission
**Description**: Verify user permissions
**Acceptance**: Sub-10ms permission checks

**REQ-T070**: Session Management
**Priority**: MEDIUM
**Endpoint**: GET /v1/auth/sessions
**Description**: List and revoke active sessions
**Acceptance**: Users can view/revoke sessions

### Agent Management API (REQ-T071 - REQ-T080)

**REQ-T071**: Create Agent
**Priority**: CRITICAL
**Endpoint**: POST /v1/agents
**Request**: Agent configuration (type, capabilities, cognitive pattern)
**Response**: 201 Created with agent resource
**Acceptance**: Agent created in <500ms

**REQ-T072**: Get Agent
**Priority**: CRITICAL
**Endpoint**: GET /v1/agents/{agentId}
**Response**: Agent resource with full state
**Acceptance**: Sub-100ms response time

**REQ-T073**: List Agents
**Priority**: HIGH
**Endpoint**: GET /v1/agents
**Query Params**: filter, sort, pagination
**Acceptance**: Returns paginated agent list

**REQ-T074**: Update Agent
**Priority**: HIGH
**Endpoint**: PATCH /v1/agents/{agentId}
**Request**: Partial agent updates
**Response**: 200 OK with updated resource
**Acceptance**: Optimistic locking support

**REQ-T075**: Delete Agent
**Priority**: HIGH
**Endpoint**: DELETE /v1/agents/{agentId}
**Description**: Soft delete with cleanup job
**Response**: 204 No Content
**Acceptance**: Cascade delete related resources

**REQ-T076**: Adapt Agent
**Priority**: HIGH
**Endpoint**: POST /v1/agents/{agentId}/adapt
**Request**: Feedback and performance score
**Response**: Adaptation result
**Acceptance**: Updates cognitive pattern

**REQ-T077**: Get Agent Metrics
**Priority**: HIGH
**Endpoint**: GET /v1/agents/{agentId}/metrics
**Response**: Performance metrics and learning progress
**Acceptance**: Real-time metrics <5s lag

**REQ-T078**: Agent Health Check
**Priority**: MEDIUM
**Endpoint**: GET /v1/agents/{agentId}/health
**Response**: Health status and diagnostics
**Acceptance**: Health status in <100ms

**REQ-T079**: Clone Agent
**Priority**: MEDIUM
**Endpoint**: POST /v1/agents/{agentId}/clone
**Description**: Create agent copy with same configuration
**Acceptance**: Clones in <1 second

**REQ-T080**: Export Agent
**Priority**: MEDIUM
**Endpoint**: GET /v1/agents/{agentId}/export
**Format**: JSON with full state
**Acceptance**: Exportable and importable

### Knowledge Sharing API (REQ-T081 - REQ-T090)

**REQ-T081**: Share Knowledge
**Priority**: CRITICAL
**Endpoint**: POST /v1/knowledge/share
**Request**: Source agent, target agents, knowledge content
**Response**: 202 Accepted with job ID
**Acceptance**: Asynchronous knowledge transfer

**REQ-T082**: Get Knowledge
**Priority**: HIGH
**Endpoint**: GET /v1/knowledge/{knowledgeId}
**Response**: Knowledge item with metadata
**Acceptance**: Sub-50ms retrieval

**REQ-T083**: Search Knowledge
**Priority**: HIGH
**Endpoint**: GET /v1/knowledge/search
**Query Params**: q (query), domain, agent_id
**Response**: Ranked search results
**Acceptance**: Full-text search <200ms

**REQ-T084**: List Agent Knowledge
**Priority**: HIGH
**Endpoint**: GET /v1/agents/{agentId}/knowledge
**Response**: Paginated knowledge items
**Acceptance**: Lists all agent knowledge

**REQ-T085**: Delete Knowledge
**Priority**: MEDIUM
**Endpoint**: DELETE /v1/knowledge/{knowledgeId}
**Description**: Remove knowledge item
**Acceptance**: Soft delete with audit trail

**REQ-T086**: Knowledge Suggestions
**Priority**: MEDIUM
**Endpoint**: GET /v1/knowledge/suggestions
**Query Params**: agent_id, context
**Response**: Recommended knowledge items
**Acceptance**: ML-based recommendations

**REQ-T087**: Knowledge Graph
**Priority**: LOW
**Endpoint**: GET /v1/knowledge/graph
**Response**: Knowledge relationship graph
**Acceptance**: GraphQL alternative

**REQ-T088**: Knowledge Versioning
**Priority**: MEDIUM
**Endpoint**: GET /v1/knowledge/{knowledgeId}/versions
**Response**: Version history
**Acceptance**: Immutable version tracking

**REQ-T089**: Bulk Import Knowledge
**Priority**: MEDIUM
**Endpoint**: POST /v1/knowledge/import
**Request**: Array of knowledge items
**Acceptance**: Batch import with validation

**REQ-T090**: Knowledge Analytics
**Priority**: LOW
**Endpoint**: GET /v1/knowledge/analytics
**Response**: Usage statistics and trends
**Acceptance**: Aggregated analytics

### Pattern Learning API (REQ-T091 - REQ-T100)

**REQ-T091**: Analyze Pattern
**Priority**: HIGH
**Endpoint**: POST /v1/patterns/analyze
**Request**: Agent ID, operation data
**Response**: Pattern analysis results
**Acceptance**: Pattern detection <500ms

**REQ-T092**: Get Pattern
**Priority**: HIGH
**Endpoint**: GET /v1/patterns/{patternId}
**Response**: Pattern details and statistics
**Acceptance**: Returns pattern metadata

**REQ-T093**: List Patterns
**Priority**: HIGH
**Endpoint**: GET /v1/patterns
**Query Params**: type, agent_id, domain
**Acceptance**: Filtered pattern listing

**REQ-T094**: Learn Pattern
**Priority**: HIGH
**Endpoint**: POST /v1/patterns/learn
**Request**: Pattern data and training examples
**Response**: Learning job ID
**Acceptance**: Async pattern learning

**REQ-T095**: Update Cognitive Pattern
**Priority**: HIGH
**Endpoint**: PATCH /v1/agents/{agentId}/cognitive-pattern
**Request**: New pattern type
**Response**: Updated agent
**Acceptance**: Pattern switch validated

**REQ-T096**: Pattern Performance
**Priority**: MEDIUM
**Endpoint**: GET /v1/patterns/{patternId}/performance
**Response**: Performance metrics
**Acceptance**: Pattern effectiveness metrics

**REQ-T097**: Export Pattern
**Priority**: MEDIUM
**Endpoint**: GET /v1/patterns/{patternId}/export
**Format**: JSON or binary model
**Acceptance**: Portable pattern export

**REQ-T098**: Import Pattern
**Priority**: MEDIUM
**Endpoint**: POST /v1/patterns/import
**Request**: Pattern file upload
**Acceptance**: Validates before import

**REQ-T099**: Pattern Comparison
**Priority**: LOW
**Endpoint**: POST /v1/patterns/compare
**Request**: Array of pattern IDs
**Response**: Comparison metrics
**Acceptance**: Side-by-side comparison

**REQ-T100**: Pattern Recommendations
**Priority**: MEDIUM
**Endpoint**: GET /v1/patterns/recommendations
**Query Params**: agent_id, task_type
**Response**: Recommended patterns
**Acceptance**: Context-aware suggestions

## OpenAPI Specification

```yaml
openapi: 3.0.3
info:
  title: DAA Autonomous Learning API
  description: |
    API for managing decentralized autonomous agents with adaptive learning capabilities.

    Features:
    - Agent lifecycle management
    - Knowledge sharing network
    - Pattern learning and recognition
    - Meta-learning across domains
    - Performance monitoring
  version: 1.0.0
  contact:
    name: DAA API Support
    email: api-support@example.com
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: https://api.daa.example.com/v1
    description: Production
  - url: https://staging-api.daa.example.com/v1
    description: Staging
  - url: http://localhost:3000/v1
    description: Local Development

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: JWT access token

    apiKey:
      type: apiKey
      in: header
      name: X-API-Key
      description: API key for service accounts

    oauth2:
      type: oauth2
      flows:
        authorizationCode:
          authorizationUrl: https://api.daa.example.com/v1/oauth/authorize
          tokenUrl: https://api.daa.example.com/v1/oauth/token
          scopes:
            agents:read: Read agent data
            agents:write: Create and modify agents
            knowledge:read: Read knowledge base
            knowledge:write: Share knowledge
            patterns:read: Read patterns
            patterns:write: Learn patterns
            admin: Administrative access

  schemas:
    Agent:
      type: object
      required: [id, type, status, created_at]
      properties:
        id:
          type: string
          format: uuid
          description: Unique agent identifier
        type:
          type: string
          description: Agent specialization
          example: researcher
        status:
          type: string
          enum: [active, paused, stopped, learning]
          description: Current agent status
        cognitive_pattern:
          type: string
          enum: [convergent, divergent, lateral, systems, critical, adaptive]
          description: Thinking pattern
        capabilities:
          type: array
          items:
            type: string
          description: Agent capabilities
        learning_rate:
          type: number
          format: float
          minimum: 0
          maximum: 1
          description: Learning rate (0-1)
        performance_score:
          type: number
          format: float
          minimum: 0
          maximum: 1
          description: Overall performance
        metadata:
          type: object
          additionalProperties: true
          description: Custom metadata
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time
      example:
        id: "550e8400-e29b-41d4-a716-446655440000"
        type: "researcher"
        status: "active"
        cognitive_pattern: "systems"
        capabilities: ["analysis", "synthesis"]
        learning_rate: 0.8
        performance_score: 0.92
        created_at: "2024-01-15T10:30:00Z"
        updated_at: "2024-01-15T14:25:00Z"

    Knowledge:
      type: object
      required: [id, domain, content, source_agent_id]
      properties:
        id:
          type: string
          format: uuid
        domain:
          type: string
          description: Knowledge domain
        content:
          type: object
          description: Knowledge data
        source_agent_id:
          type: string
          format: uuid
          description: Agent that created knowledge
        confidence:
          type: number
          format: float
          minimum: 0
          maximum: 1
        tags:
          type: array
          items:
            type: string
        version:
          type: integer
          description: Version number
        created_at:
          type: string
          format: date-time

    Pattern:
      type: object
      required: [id, type, pattern_data]
      properties:
        id:
          type: string
          format: uuid
        type:
          type: string
          enum: [convergent, divergent, lateral, systems, critical, adaptive]
        pattern_data:
          type: object
          description: Pattern model data
        accuracy:
          type: number
          format: float
        usage_count:
          type: integer
        created_at:
          type: string
          format: date-time

    Error:
      type: object
      required: [code, message]
      properties:
        code:
          type: string
          description: Error code
          example: VALIDATION_ERROR
        message:
          type: string
          description: Human-readable error message
          example: Invalid agent type
        details:
          type: array
          items:
            type: object
            properties:
              field:
                type: string
              message:
                type: string
        trace_id:
          type: string
          format: uuid
          description: Request trace ID

    PaginatedResponse:
      type: object
      required: [data, meta]
      properties:
        data:
          type: array
          items: {}
        meta:
          type: object
          properties:
            total:
              type: integer
            limit:
              type: integer
            cursor:
              type: string
            has_more:
              type: boolean
        links:
          type: object
          properties:
            self:
              type: string
              format: uri
            next:
              type: string
              format: uri
            prev:
              type: string
              format: uri

security:
  - bearerAuth: []
  - apiKey: []

paths:
  /auth/token:
    post:
      summary: Obtain access token
      tags: [Authentication]
      security: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [grant_type]
              properties:
                grant_type:
                  type: string
                  enum: [password, refresh_token, client_credentials]
                username:
                  type: string
                password:
                  type: string
                  format: password
                refresh_token:
                  type: string
                client_id:
                  type: string
                client_secret:
                  type: string
      responses:
        200:
          description: Token issued
          content:
            application/json:
              schema:
                type: object
                properties:
                  access_token:
                    type: string
                  refresh_token:
                    type: string
                  token_type:
                    type: string
                    example: Bearer
                  expires_in:
                    type: integer
                    example: 3600
        401:
          description: Authentication failed
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

  /agents:
    get:
      summary: List agents
      tags: [Agents]
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
            maximum: 100
            default: 20
        - name: cursor
          in: query
          schema:
            type: string
        - name: filter[type]
          in: query
          schema:
            type: string
        - name: filter[status]
          in: query
          schema:
            type: string
        - name: sort
          in: query
          schema:
            type: string
            example: -created_at
      responses:
        200:
          description: Agent list
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedResponse'

    post:
      summary: Create agent
      tags: [Agents]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [type]
              properties:
                type:
                  type: string
                cognitive_pattern:
                  type: string
                capabilities:
                  type: array
                  items:
                    type: string
                learning_rate:
                  type: number
                  format: float
                metadata:
                  type: object
      responses:
        201:
          description: Agent created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Agent'
        400:
          description: Validation error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

  /agents/{agentId}:
    get:
      summary: Get agent
      tags: [Agents]
      parameters:
        - name: agentId
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        200:
          description: Agent details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Agent'
        404:
          description: Agent not found

    patch:
      summary: Update agent
      tags: [Agents]
      parameters:
        - name: agentId
          in: path
          required: true
          schema:
            type: string
            format: uuid
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                status:
                  type: string
                cognitive_pattern:
                  type: string
                learning_rate:
                  type: number
      responses:
        200:
          description: Agent updated
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Agent'

    delete:
      summary: Delete agent
      tags: [Agents]
      parameters:
        - name: agentId
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        204:
          description: Agent deleted

  /knowledge/share:
    post:
      summary: Share knowledge between agents
      tags: [Knowledge]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [source_agent_id, target_agent_ids, knowledge_content]
              properties:
                source_agent_id:
                  type: string
                  format: uuid
                target_agent_ids:
                  type: array
                  items:
                    type: string
                    format: uuid
                knowledge_domain:
                  type: string
                knowledge_content:
                  type: object
      responses:
        202:
          description: Knowledge sharing initiated
          content:
            application/json:
              schema:
                type: object
                properties:
                  job_id:
                    type: string
                    format: uuid
                  status:
                    type: string
                    example: pending

  /patterns/analyze:
    post:
      summary: Analyze cognitive patterns
      tags: [Patterns]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [agent_id, operation_data]
              properties:
                agent_id:
                  type: string
                  format: uuid
                operation_data:
                  type: object
      responses:
        200:
          description: Pattern analysis
          content:
            application/json:
              schema:
                type: object
                properties:
                  detected_patterns:
                    type: array
                    items:
                      $ref: '#/components/schemas/Pattern'
                  recommendations:
                    type: array
                    items:
                      type: string
```

## GraphQL Schema

```graphql
type Query {
  agent(id: ID!): Agent
  agents(
    filter: AgentFilter
    sort: [AgentSort!]
    limit: Int = 20
    cursor: String
  ): AgentConnection!

  knowledge(id: ID!): Knowledge
  searchKnowledge(
    query: String!
    domain: String
    limit: Int = 20
  ): [Knowledge!]!

  pattern(id: ID!): Pattern
  patterns(
    type: PatternType
    agentId: ID
  ): [Pattern!]!
}

type Mutation {
  createAgent(input: CreateAgentInput!): Agent!
  updateAgent(id: ID!, input: UpdateAgentInput!): Agent!
  deleteAgent(id: ID!): Boolean!
  adaptAgent(id: ID!, feedback: String!, score: Float!): AdaptationResult!

  shareKnowledge(input: ShareKnowledgeInput!): KnowledgeShareJob!

  learnPattern(input: LearnPatternInput!): PatternLearningJob!
  updateCognitivePattern(agentId: ID!, pattern: PatternType!): Agent!
}

type Subscription {
  agentUpdated(agentId: ID!): Agent!
  knowledgeShared(agentId: ID!): Knowledge!
  patternLearned(agentId: ID!): Pattern!
}

type Agent {
  id: ID!
  type: String!
  status: AgentStatus!
  cognitivePattern: PatternType!
  capabilities: [String!]!
  learningRate: Float!
  performanceScore: Float!
  metadata: JSON
  createdAt: DateTime!
  updatedAt: DateTime!

  # Relationships
  knowledge: [Knowledge!]!
  patterns: [Pattern!]!
  metrics: AgentMetrics!
}

type Knowledge {
  id: ID!
  domain: String!
  content: JSON!
  sourceAgent: Agent!
  confidence: Float!
  tags: [String!]!
  version: Int!
  createdAt: DateTime!
}

type Pattern {
  id: ID!
  type: PatternType!
  patternData: JSON!
  accuracy: Float!
  usageCount: Int!
  createdAt: DateTime!
}

enum AgentStatus {
  ACTIVE
  PAUSED
  STOPPED
  LEARNING
}

enum PatternType {
  CONVERGENT
  DIVERGENT
  LATERAL
  SYSTEMS
  CRITICAL
  ADAPTIVE
}

input CreateAgentInput {
  type: String!
  cognitivePattern: PatternType
  capabilities: [String!]
  learningRate: Float
  metadata: JSON
}

scalar JSON
scalar DateTime
```

## API Response Examples

### Success Response
```json
{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "type": "researcher",
    "status": "active",
    "cognitive_pattern": "systems",
    "performance_score": 0.92
  },
  "meta": {
    "request_id": "req_abc123",
    "timestamp": "2024-01-15T10:30:00Z"
  },
  "links": {
    "self": "/v1/agents/550e8400-e29b-41d4-a716-446655440000"
  }
}
```

### Error Response
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid agent type",
    "details": [
      {
        "field": "type",
        "message": "Must be one of: researcher, coder, analyst"
      }
    ],
    "trace_id": "trace_xyz789"
  }
}
```

## Rate Limiting

| Tier | Requests/Minute | Burst | Concurrency |
|------|-----------------|-------|-------------|
| Free | 60 | 10 | 5 |
| Pro | 600 | 100 | 50 |
| Enterprise | 6000 | 1000 | 500 |

**Headers**:
- `X-RateLimit-Limit`: Total requests allowed
- `X-RateLimit-Remaining`: Remaining requests
- `X-RateLimit-Reset`: Reset timestamp

## Webhooks

Events pushed to configured webhook endpoints:

```json
{
  "event": "agent.created",
  "data": {
    "agent_id": "550e8400-e29b-41d4-a716-446655440000"
  },
  "timestamp": "2024-01-15T10:30:00Z",
  "signature": "sha256=..."
}
```

**Supported Events**:
- `agent.created`, `agent.updated`, `agent.deleted`
- `knowledge.shared`, `knowledge.updated`
- `pattern.learned`, `pattern.updated`

---

**Requirements**: REQ-T051 to REQ-T100 (50 requirements)
**Endpoints**: 52 REST endpoints
**Status**: ✅ Complete
**Version**: 1.0.0
