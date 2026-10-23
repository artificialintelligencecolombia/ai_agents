# # Crew AI Core Concepts

## Definitions

- **Agent**: an autonomous unit, with an LLM, a role, a goal, a backstory, memory and tools. (Role, Goal, Backstory)
- **Task**: a specific assignment to be carried out by an agent with description, expected output. Assigned to an agent
- **Crew**: a team of agents and tasks. Tasks are the most important part of a crew. (Sequential: run in order, Hierarchical: use a manager LLM to assign them)

## Yaml Configuration

Agents and tasks can be created by code, by using 2 YAML files, one for agents and one for tasks.

## Create a crewAI project

1. Create the project:

```bash
crewai create crew <my_project>
```

2. Define the Agents and Tasks

3. Set inputs in the Agents and Tasks definitions

4. Run the project

```bash
crewai run
```

## Tools

Equiping agents with capabilities

## Context

Information passed from one task to another

## CrewAI Tracing

1. Once per machine

crewai login
If you also see "Tool Repository… 401", ignore it. That's a separate tool store and doesn't affect tracing.

2. Once per project

Add this line to the project's .env:
CREWAI_TRACING_ENABLED=true

3. Every run

crewai run
When the run finishes, press t (or click View Traces) and the trace opens in your browser.

4. Turn it off

Delete the .env line, or change it to CREWAI_TRACING_ENABLED=false.