# Crew AI Core Concepts

## Definitions

- **Agent**: an autonomous unit, with an LLM, a role, a goal, a backstory, memory and tools. (Role, Goal, Backstory)
- **Task**: a specific assignment to be carried out by an agent with descrption, expected output
- **Crew**: a team of agents and tasks. Tasks are the most important part of a crew. (Sequential: run in order, Hierarchical: use a manager LLM to assign them)

## Yaml Configuration

Agents and tasks can be created by code, by using 2 YAML files, one for agents and one for tasks.

## Create a crewAI project

crewai create crew <my_project>