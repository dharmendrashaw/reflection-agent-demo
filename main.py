from dotenv import load_dotenv
from typing import TypedDict, Annotated, Literal

load_dotenv()

from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages
from langgraph.graph import END, StateGraph



from chains import generation_chain, reflection_chain

class MessageGraph(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

REFLECT = "reflect"
GENERATE = "generate"

def generate_node(state: MessageGraph):
    response = generation_chain.invoke({"messages": state["messages"]})
    return {"messages": [response]}

def reflect_node(state: MessageGraph):
    response = reflection_chain.invoke(
        {
            "messages": [
                *state["messages"],
                HumanMessage(content="Please critique the latest draft and recommend improvements."),
            ]
        }
    )
    return {"messages": [HumanMessage(content=response.content)]}

builder = StateGraph(state_schema=MessageGraph)
builder.add_node(GENERATE, generate_node)
builder.add_node(REFLECT, reflect_node)

builder.set_entry_point(GENERATE)

# Decide whether to continue generating or reflecting based on the number of messages
# Can be modified to include more complex logic based on the content of the messages, user feedback, etc.
def should_continue(state: MessageGraph) -> Literal["reflect", "__end__"]:
    if len(state["messages"]) > 3:  # Arbitrary limit for demonstration; can be adjusted
        return END
    return REFLECT

builder.add_conditional_edges(
    GENERATE,
    should_continue,
    {REFLECT: REFLECT, END: END},
)

builder.add_edge(REFLECT, GENERATE)

graph = builder.compile()

print(graph.get_graph().draw_mermaid())
graph.get_graph().print_ascii()
graph.get_graph().draw_mermaid_png(output_file_path="flow.png")

if __name__ == "__main__":
    print("Starting the reflection-agent execution...")
    inputs = {
        "messages": [
            HumanMessage(
                content="""Make this tweet better:"
                                    @LangChainAI
            — newly Tool Calling feature is seriously underrated.

            After a long wait, it's  here- making the implementation of agents across different models with function calling - super easy.

            Made a video covering their newest blog post

                                  """
            )
        ]
    }
    response = graph.invoke(inputs)
    print(response)
