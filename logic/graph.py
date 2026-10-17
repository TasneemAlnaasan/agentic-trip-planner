import time
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from config import settings
from logic.planner import run_planner
from logic.evaluator import evaluate


class TripState(TypedDict):
    user_query: str
    itinerary_text: str
    collected_data: dict
    evaluation: dict
    attempt_count: int


def planner_node(state: TripState):
    itinerary_text, collected_data = run_planner(state["user_query"])

    return {
        "itinerary_text": itinerary_text,
        "collected_data": collected_data
    }


def evaluator_node(state: TripState):
    evaluation = evaluate(
        state["collected_data"],
        state["itinerary_text"]
    )

    return {
        "evaluation": evaluation
    }


def replanner_node(state: TripState):
    return {
        "attempt_count": state["attempt_count"] + 1
    }


def final_composer_node(state: TripState):
    if state["evaluation"]["is_sufficient"]:
        final_output = state["itinerary_text"]
    else:
        reason = state["evaluation"]["reason"]
        final_output = (
            f"{state['itinerary_text']}\n\n"
            f"⚠️ Note: This is the best itinerary we could generate after "
            f"{state['attempt_count']} attempts. {reason}"
        )

    return {
        "itinerary_text": final_output
    }


def route_after_evaluation(state: TripState):
    if state["evaluation"]["is_sufficient"]:
        return "sufficient"
    elif state["attempt_count"] < settings.max_attempts:
        return "retry"
    else:
        return "give_up"


graph_builder = StateGraph(TripState)

graph_builder.add_node("planner", planner_node)
graph_builder.add_node("evaluator", evaluator_node)
graph_builder.add_node("replanner", replanner_node)
graph_builder.add_node("final_composer", final_composer_node)

graph_builder.add_edge(START, "planner")
graph_builder.add_edge("planner", "evaluator")

graph_builder.add_conditional_edges(
    "evaluator",
    route_after_evaluation,
    {
        "sufficient": "final_composer",
        "retry": "replanner",
        "give_up": "final_composer"
    }
)

graph_builder.add_edge("replanner", "planner")
graph_builder.add_edge("final_composer", END)

graph = graph_builder.compile()


def plan_trip_streaming(user_query):
   
    initial_state = {
        "user_query": user_query,
        "itinerary_text": "",
        "collected_data": {},
        "evaluation": {},
        "attempt_count": 0
    }

    for step in graph.stream(initial_state):
        node_name = list(step.keys())[0]
        print(f"[{time.strftime('%H:%M:%S')}] Node finished: {node_name}")
        yield step


if __name__ == "__main__":
    for step in plan_trip_streaming("Plan a 3-day trip to Petra"):
        print(step)
