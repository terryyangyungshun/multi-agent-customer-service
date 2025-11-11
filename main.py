from agents import (
    HandoffOutputItem,
    ItemHelpers,
    MessageOutputItem,
    Runner,
    ToolCallItem,
    ToolCallOutputItem,
)

from dotenv import load_dotenv
import asyncio
load_dotenv(override=True)
from flight_modification_agent import flight_modification
from flight_cancel_agent import flight_cancel
from lost_baggage_agent import lost_baggage
from triage_agent import triage_agent
from flight_change_agent import flight_change

# 統一設定 handoffs
flight_modification.handoffs.extend([flight_cancel, flight_change])
flight_cancel.handoffs.append(triage_agent)
flight_change.handoffs.append(triage_agent)
lost_baggage.handoffs.append(triage_agent)

async def chat_assistant():
    
    input_items = []
    current_agent = triage_agent
    
    while True:
        user_input = input("💬 請輸入你的訊息：")
        if user_input.lower() in ["exit", "quit"]:
            print("✅ 對話已結束")
            break

        input_items.append({"content": user_input, "role": "user"})
        result = await Runner.run(current_agent, input_items)

        for new_item in result.new_items:
            agent_name = new_item.agent.name
            if isinstance(new_item, MessageOutputItem):
                print(f"🧠 {agent_name}: {ItemHelpers.text_message_output(new_item)}")
            elif isinstance(new_item, HandoffOutputItem):
                print(f"🔀 Handed off from {new_item.source_agent.name} to {new_item.target_agent.name}")
            elif isinstance(new_item, ToolCallItem):
                print(f"🔧 {agent_name}: Calling a tool...")
            elif isinstance(new_item, ToolCallOutputItem):
                print(f"📦 {agent_name}: Tool call output: {new_item.output}")

        input_items = result.to_input_list()
        current_agent = result.last_agent
if __name__ == "__main__":
    asyncio.run(chat_assistant())