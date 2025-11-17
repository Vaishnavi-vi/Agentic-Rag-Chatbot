# import uuid
# from langsmith.evaluation import evaluate
# from src.workflow.pipeline import workflow
# from langchain_core.messages import HumanMessage

# # -------------------------------------------------------
# # UNIVERSAL QUERY EXTRACTOR
# # -------------------------------------------------------
# def extract_query(example):
#     """Extract query from the example object."""
#     try:
#         if "query" in example.inputs:
#             return example.inputs["query"]
#         if "input" in example.inputs and isinstance(example.inputs["input"], dict):
#             if "query" in example.inputs["input"]:
#                 return example.inputs["input"]["query"]
#         if "input" in example.inputs and isinstance(example.inputs["input"], str):
#             return example.inputs["input"]
#     except Exception:
#         return None
#     return None

# # -------------------------------------------------------
# # MODEL RUNNER
# # -------------------------------------------------------
# class DummyRun:
#     """Wraps outputs to mimic LangSmith Run object."""
#     def __init__(self, outputs):
#         self.outputs = outputs

# def run_agentic_rag(example, **kwargs):
#     query = extract_query(example)
#     if query is None:
#         return DummyRun({"output": ""})

#     result = workflow.invoke(
#         {"messages": [HumanMessage(content=query)]},
#         config={"configurable": {"thread_id": f"eval-{uuid.uuid4()}"}}
#     )

#     return DummyRun({"output": result["messages"][-1].content})

# # -------------------------------------------------------
# # CORRECTNESS EVALUATOR
# # -------------------------------------------------------
# def correctness_evaluator(example, run, **kwargs):
#     query = extract_query(example)
#     if query is None:
#         return {"score": 0}

#     model_answer = run.outputs.get("output", "")
#     reference = example.outputs.get("reference", "")

#     if not isinstance(model_answer, str):
#         return {"score": 0}

#     return {"score": 1 if reference.lower() in model_answer.lower() else 0}

# # -------------------------------------------------------
# # TOOL EVALUATOR
# # -------------------------------------------------------
# def tool_evaluator(example, run, **kwargs):
#     query = extract_query(example)
#     if query is None:
#         return {"score": 1}

#     model_answer = run.outputs.get("output", "")

#     tool_keywords = [
#         "bmi", "convert", "usd", "inr", "stock", "price",
#         "temperature", "weather", "sum", "add", "calculate"
#     ]

#     if not any(k in query.lower() for k in tool_keywords):
#         return {"score": 1}

#     return {"score": 1 if any(ch.isdigit() for ch in model_answer) else 0}

# # -------------------------------------------------------
# # QUALITY EVALUATOR
# # -------------------------------------------------------
# def quality_evaluator(example, run, **kwargs):
#     model_answer = run.outputs.get("output", "")
#     return {"score": 1 if isinstance(model_answer, str) and model_answer.strip() else 0}

# # -------------------------------------------------------
# # RUN EVALUATION
# # -------------------------------------------------------
# if __name__ == "__main__":
#     # Replace "YOUR_EXPERIMENT_NAME" with the name of your uploaded examples dataset in LangSmith
#     results = evaluate(
#     run_agentic_rag,                # <--- target function as first argument
#     experiment="Agentic Rag Chatbot",
#     data="Agentic Rag Chatbot Examples",    # your uploaded examples dataset in LangSmith
#     evaluators=[correctness_evaluator, tool_evaluator, quality_evaluator])


#     # Print results
#     print("\nEvaluation Complete!")
#     print("View detailed scores here:")
#     print(results.url)

#     # Print summary scores for each evaluator
#     print("\nScores per evaluator:")
#     for evaluator_name, score in results.scores.items():
#         print(f"{evaluator_name}: {score}")



import uuid
from langchain_core.messages import HumanMessage
from src.workflow.pipeline import workflow

class DummyRun:
    """Mimics LangSmith Run object."""
    def __init__(self, outputs):
        self.outputs = outputs

def run_agentic_rag_safe(example):
    query = example.get("inputs", {}).get("query", "")
    if not query:
        return DummyRun({"output": ""})
    
    try:
        result = workflow.invoke(
            {"messages": [HumanMessage(content=query)]},
            config={"configurable": {"thread_id": f"eval-{uuid.uuid4()}"}}
        )
        return DummyRun({"output": result["messages"][-1].content})
    except Exception as e:
        print(f"Workflow error for query '{query}': {e}")
        return DummyRun({"output": ""})

# Evaluators remain the same
def correctness_evaluator(example, run):
    model_answer = run.outputs.get("output", "")
    reference = example.get("outputs", {}).get("reference", "")
    return 1 if reference.lower() in model_answer.lower() else 0

def tool_evaluator(example, run):
    model_answer = run.outputs.get("output", "")
    query = example.get("inputs", {}).get("query", "")
    tool_keywords = ["bmi","convert","usd","inr","stock","price","temperature","weather","sum","add","calculate"]
    if not any(k in query.lower() for k in tool_keywords):
        return 1
    return 1 if any(ch.isdigit() for ch in model_answer) else 0

def quality_evaluator(example, run):
    model_answer = run.outputs.get("output", "")
    return 1 if model_answer.strip() else 0


import json

examples_file = "golden_dataset/golden_dataset.jsonl"
correctness_scores = []
tool_scores = []
quality_scores = []

with open(examples_file, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:  # skip empty lines
            continue
        example = json.loads(line)
        run = run_agentic_rag_safe(example)
        correctness_scores.append(correctness_evaluator(example, run))
        tool_scores.append(tool_evaluator(example, run))
        quality_scores.append(quality_evaluator(example, run))

print("=== Evaluation Scores ===")
print(f"Correctness: {sum(correctness_scores)/len(correctness_scores):.2f}")
print(f"Tool usage: {sum(tool_scores)/len(tool_scores):.2f}")
print(f"Quality: {sum(quality_scores)/len(quality_scores):.2f}")























