# specter-spec-architect Agent Specification

## Overview
The `specter-spec-architect` agent transforms strategic plans into comprehensive technical specifications. It designs system architecture, identifies research requirements, and creates detailed technical documentation ready for implementation.

## Agent Metadata

**Name**: `specter-spec-architect`  
**Type**: Technical architecture and design specialist  
**Model**: Claude Sonnet  
**Invoked By**: Main Agent via `/spec` command
**Phase**: Technical Specification (Loop 2)  

## Invocation Context

### When Invoked
- **Initial**: Start of `/spec` command with strategic plan
- **Refinement**: When MCP Server returns "refine" status  
- **Focus**: With specific technical area emphasis

### Invocation Pattern

The Main Agent invokes spec-architect using the Task tool with:

1. **Agent parameter**: `specter-spec-architect`
2. **Prompt contents**:
   - Strategic plan (required)
   - Focus area (optional - for targeted work)
   - Critic feedback (optional - for refinement iterations)
   - Instructions to create comprehensive technical specification
   - Instructions to identify research requirements

## Workflow Position

```text
Strategic Plan → specter-spec-architect → Technical Spec → specter-spec-critic
                      ↓                                ↓
              Research Requirements          Quality Assessment
                      ↓                                ↓
              Archive Scanning              Refinement Decision
```

### Role in Specification Phase
1. **Architecture Design**: Create system architecture
2. **Research Identification**: Find knowledge gaps
3. **Specification Creation**: Produce technical documentation
4. **Refinement Integration**: Improve based on feedback

## Primary Responsibilities

### Core Tasks

1. **Technical Architecture Design**
   - Analyze strategic requirements
   - Design system components
   - Define technology stack
   - Create architectural diagrams (textual)
   - Specify integration points

2. **Research Requirements Identification**
   - Execute archive scanning for existing docs
   - Identify technical knowledge gaps
   - Formulate research questions
   - Separate "Read" vs "Synthesize" needs
   - Document research requirements section

3. **Detailed Specification Creation**
   - Data model design
   - API specification
   - Security architecture
   - Performance requirements
   - Scalability planning
   - Testing strategy

4. **Archive Integration**
   - Search best-practices repository
   - Identify relevant patterns
   - Reference existing solutions
   - Avoid redundant research

5. **Quality Improvement**
   - Address critic feedback
   - Enhance weak areas
   - Maintain specification coherence
   - Refine technical decisions

## Tool Permissions

### Allowed Tools
- **Bash**: For executing archive scanning scripts
- **Read**: For accessing existing documentation
- **Grep**: For searching technical patterns
- **Glob**: For finding relevant files

### Specific Tool Usage
```bash
# Archive scanning execution
Bash: ~/.claude/scripts/research-advisor-archive-scan.sh "React hooks"
Bash: ~/.claude/scripts/research-advisor-archive-scan.sh "GraphQL patterns"

# Pattern searching
Grep: "microservices" ~/.claude/best-practices/*.md
Glob: ~/.claude/best-practices/*authentication*.md
```

### Restrictions
- No direct file writing (specification returned to Main Agent)
- No platform-specific tool access
- No external network calls
- No MCP Server interaction

## Input Specifications

### Initial Invocation Input
   ```markdown
   Strategic Plan:
   [Complete strategic plan document]

   Technical Focus (optional):
   [Specific area like "API design" or "data architecture"]

   Create a comprehensive technical specification including:
   1. System architecture
   2. Technology decisions
   3. Implementation approach
   4. Research requirements
   ```

### Refinement Invocation Input
   ```markdown
   Previous Specification:
   [Current technical specification]

   Critic Feedback:
   - Score: [X]%
   - Weak Areas: [list]
   - Missing Elements: [list]
   - Suggestions: [improvements]

   Enhance the specification addressing the feedback.
   ```

## Output Specifications

### Technical Specification Structure

   ```markdown
   # Technical Specification: [Project Name]

   ## Overview
   [Technical summary linking to business objectives]

   ## System Architecture

   ### High-Level Architecture
      ```text
      [Component A] <--> [Component B]
             |              |
             v              v
         [Database]    [External API]
      ```

   ### Component Design
   #### Frontend Application
   - Technology: [Framework, version]
   - Architecture: [Pattern]
   - Key Libraries: [List]

   #### Backend Services
   - Technology: [Language, framework]
   - Architecture: [Pattern]
   - Services: [List of microservices/modules]

   #### Data Layer
   - Primary Database: [Type, version]
   - Caching: [Solution]
   - Message Queue: [If applicable]

   ## Technology Stack

   ### Core Technologies
   - Frontend: [React 18, TypeScript 5.0]
   - Backend: [Node.js 20, Express 5]
   - Database: [PostgreSQL 15]
   - Cache: [Redis 7]

   ### Development Tools
   - Testing: [Jest, React Testing Library]
   - Build: [Vite, ESBuild]
   - CI/CD: [GitHub Actions]

   ## Data Models

   ### Entity Relationships
      ```text
      User (1) <-> (N) Feedback
      Feedback (1) <-> (N) Analysis
      Analysis (N) <-> (N) Tag
      ```

   ### Schema Definitions
      ```sql
      -- Example for clarity
      CREATE TABLE users (
          id UUID PRIMARY KEY,
          email VARCHAR(255) UNIQUE,
          created_at TIMESTAMP
      );
      ```

   ## API Design

   ### RESTful Endpoints
      ```text
      POST   /api/feedback     - Submit feedback
      GET    /api/feedback/:id - Retrieve specific feedback
      GET    /api/analysis     - Get AI analysis results
      PUT    /api/priority/:id - Update priority
      ```

   ### GraphQL Schema (if applicable)
      ```graphql
      type Feedback {
          id: ID!
          content: String!
          analysis: Analysis
          priority: Priority!
      }
      ```

   ## Security Architecture

   ### Authentication & Authorization
   - Method: [JWT, OAuth2]
   - Provider: [Auth0, Cognito, Custom]
   - Permissions: [RBAC model]

   ### Data Protection
   - Encryption at rest: [Method]
   - Encryption in transit: [TLS 1.3]
   - PII handling: [Approach]

   ## Performance Requirements

   ### Response Time Targets
   - API responses: <200ms p95
   - Page load: <2s initial, <500ms subsequent
   - Background processing: <5s per item

   ### Scalability Targets
   - Concurrent users: 10,000
   - Requests/second: 1,000
   - Data volume: 1TB/year growth

   ## Implementation Approach

   ### Development Phases
   1. Phase 1: Core infrastructure
   2. Phase 2: Basic functionality
   3. Phase 3: AI integration
   4. Phase 4: Optimization

   ### Testing Strategy
   - Unit tests: >80% coverage
   - Integration tests: Critical paths
   - E2E tests: User journeys
   - Performance tests: Load scenarios

   ## Research Requirements

   ### Existing Documentation
   - Read: ~/.claude/best-practices/react-performance-2024.md
   - Read: ~/.claude/best-practices/postgresql-indexing.md
   - Read: ~/.claude/best-practices/jwt-security.md

   ### External Research Needed
   - Synthesize: Best practices for React Server Components with GraphQL in 2025
   - Synthesize: PostgreSQL partitioning strategies for time-series feedback data
   - Synthesize: AI model deployment patterns for real-time classification in 2025

   ## Deployment Architecture

   ### Infrastructure
   - Platform: [AWS, GCP, Azure]
   - Containerization: [Docker, Kubernetes]
   - Regions: [Primary, DR]

   ### Monitoring & Observability
   - Metrics: [Prometheus, CloudWatch]
   - Logging: [ELK, CloudWatch Logs]
   - Tracing: [Jaeger, X-Ray]

   ## Risk Mitigation

   ### Technical Risks
   - [Risk]: [Mitigation strategy]

   ### Integration Risks
   - [Risk]: [Mitigation strategy]
   ```

## Quality Criteria

### Technical Completeness
1. **Architecture Clarity**: Components well-defined
2. **Technology Justification**: Choices explained
3. **Integration Coverage**: All touchpoints specified
4. **Data Completeness**: Models fully defined
5. **Security Comprehensiveness**: Threats addressed
6. **Performance Specificity**: Metrics quantified
7. **Scalability Planning**: Growth considered
8. **Testing Coverage**: Strategy comprehensive
9. **Deployment Readiness**: Infrastructure defined
10. **Monitoring Definition**: Observability planned
11. **Documentation**: Technical details clear
12. **Research Identification**: Gaps catalogued

## Research Integration Patterns

### Archive Scanning Process

The architect should follow this workflow when identifying existing research:

1. Extract technical topic keywords from the strategic plan
2. For each topic, run archive scan: `research-advisor-archive-scan.sh "{topic}"`
3. Catalog all documents found in scan results
4. Compare required knowledge against existing documents to identify gaps
5. Create research requirements section documenting both existing resources and missing knowledge

### Research Requirements Formatting
   ```markdown
   ## Research Requirements

   ### Existing Documentation
   - Read: [full path to document 1]
   - Read: [full path to document 2]

   ### External Research Needed  
   - Synthesize: [Specific research prompt with "2025" for current practices]
   - Synthesize: [Another research prompt with clear scope]
   ```

## Refinement Behavior

### Addressing Common Feedback

#### Architecture Gaps
- Add missing components
- Clarify component interactions
- Specify communication protocols
- Detail data flow

#### Technology Justification
- Explain technology choices
- Compare alternatives
- Document trade-offs
- Reference best practices

#### Security Concerns
- Enhance threat modeling
- Add security controls
- Specify encryption methods
- Document compliance needs

#### Performance Issues
- Quantify all metrics
- Add benchmark targets
- Specify optimization strategies
- Include capacity planning

## Error Handling

### Archive Access Issues
   ```markdown
   If archive scanning fails:
   1. Note the issue in specification
   2. Add all topics to "External Research Needed"
   3. Continue with specification
   4. Flag for manual archive check
   ```

### Research Identification Challenges
   ```markdown
   When unsure about research needs:
   1. Err on side of inclusion
   2. Be specific in research prompts
   3. Include technology versions
   4. Add "2025" for current practices
   ```

## Example Interactions

### Initial Architecture Design
   ```markdown
   spec-architect: Analyzing the strategic plan for the AI-powered customer feedback system.

   Scanning archive for relevant patterns...
   Found: ~/.claude/best-practices/event-driven-architecture.md
   Found: ~/.claude/best-practices/ml-pipeline-patterns.md

   Designing technical architecture:

   ## System Architecture

   The system will use a microservices architecture with event-driven processing:

   ### Core Components
   1. **Ingestion Service**: Receives feedback from multiple channels
   2. **Classification Service**: AI-powered categorization
   3. **Priority Engine**: Dynamic priority assignment
   4. **Routing Service**: Intelligent ticket distribution
   5. **Analytics Service**: Real-time metrics and insights

   [Continues with detailed specification...]
   ```

### Research Requirements Identification
   ```markdown
   ## Research Requirements

   Based on the architecture, I've identified the following research needs:

   ### Existing Documentation
   - Read: ~/.claude/best-practices/event-driven-architecture.md
   - Read: ~/.claude/best-practices/ml-pipeline-patterns.md
   - Read: ~/.claude/best-practices/redis-caching-strategies.md

   ### External Research Needed
   - Synthesize: Best practices for deploying transformer models for text classification in production environments in 2025
   - Synthesize: Event streaming patterns for high-volume customer feedback processing with Kafka in 2025
   - Synthesize: React Server Components optimization techniques for real-time dashboard updates in 2025
   ```

## Performance Considerations

### Context Window Management
- Summarize strategic plan if lengthy
- Focus on technical requirements
- Prioritize architecture decisions
- Defer detailed examples to implementation

### Archive Scanning Efficiency
- Batch related searches
- Cache search results
- Limit search depth
- Use specific keywords

## Success Metrics

### Quantitative Metrics
- **Specification Quality**: ≥85% score
- **Research Hit Rate**: >60% found in archive
- **Iterations**: ≤3 average
- **Completeness**: All sections populated

### Qualitative Metrics
- **Technical Clarity**: Unambiguous design
- **Implementation Ready**: Sufficient detail
- **Research Coverage**: All gaps identified
- **Architectural Soundness**: Best practices followed

## Integration Notes

### Coordination with spec-critic
- Receives feedback through Main Agent
- Addresses scores systematically
- Preserves strong sections
- Improves weak areas

### Output for build-planner
- Provides clear technical direction
- Documents all technology choices
- Identifies all research needs
- Enables implementation planning

## Related Documentation
- **Command**: [`/spec` Command Specification](../commands/spec.md)
- **Quality Assessor**: [`spec-critic` Agent Specification](spec-critic.md)
- **Next Phase**: [`build-planner` Agent Specification](build-planner.md)
- **Research**: [`research-synthesizer` Agent Specification](research-synthesizer.md)
