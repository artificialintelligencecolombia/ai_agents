# Agents Design Patterns

1. **Open ended**: Something that can keep going 
2. **Feedback loops**: It allows information to come back and be processed multiple times
3. **No fixed path**: there is no series of steps, its dynamic (more powerful but less predictable)

Reference:
                         ---- Action ---->
HUMAN ->  LLM Call                            ENVIRONMENT
                         <--- Feedback ----
             |
             v
           STOP

## Risk of Agent Frameworks

1. Unpredictable path
2. Unpredictable output
3. Unpredictable cost
4. Monitoring is a must
5. Guardrails: ensure the agents behave safely, consistently and within the intended boundaries