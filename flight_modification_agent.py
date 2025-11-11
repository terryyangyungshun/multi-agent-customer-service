from agents import Agent, Runner
from dotenv import load_dotenv
import asyncio
# from flight_cancel_agent import flight_cancel
# from flight_change_agent import flight_change

load_dotenv(override=True)

flight_modification = Agent (
    name="Flight Modification Agent",  # 航班修改代理人
    instructions=""" 你是航空公司客服中的航班修改代理人。
        你是一名客戶服務專家，負責判斷使用者的請求是取消航班還是更改航班。
        你已經知道使用者的意圖與航班修改相關。首先，請檢視訊息歷史，判斷能否確定使用者希望取消還是更改航班。
        每次你都可以透過詢問釐清性問題來獲取更多資訊，直到能確定是取消還是更改航班。一旦確定，請呼叫相應的轉移函式。""",  # 協助代理人處理航班修改的請求
    # handoffs=[flight_cancel, flight_change],  # 可轉移的代理人：航班取消與航班更改
    model='gpt-5'
)

async def main():
    result = await Runner.run(flight_modification, "你好")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())