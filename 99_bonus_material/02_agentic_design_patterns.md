# Agentic Design (Workflow) Patterns

## 1. Prompt Chaining

IN -> LLM1 -> Gate (Code) -> LLM2 -> LLM3 -> OUT

## 2. Routing

The LLM router decides which of the possible multiple models is selected to carry out the next step's function

IN -> LLM Router    -> LLM1
                    -> LLM2 -> OUT
                    -> LLM3

## 3. Parallelization

Braking down tasks and running multiple subtasks concurrently

IN -> Coordinator(Code)     -> LLM1 \
                            -> LLM2 -> Aggregator (Code) -> OUT
                            -> LLM3 /

## 4. Orchestrator-worker

Complex tasks are broken down dynamically and combined

                            -> LLM1 \
IN -> Orchestrator (LLM)    -> LLM2 -> Synthesizer (LLM) -> OUT
                            -> LLM3 /
                            -> ... /

## 5. Evalautor-Optimizer

LLM output is validate by another LLM

IN -> LLM Generator -> LLM Evaluator -> OU
                    <-
