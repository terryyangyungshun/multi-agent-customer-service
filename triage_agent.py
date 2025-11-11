from agents import Agent, Runner, function_tool
from dotenv import load_dotenv
import asyncio
from flight_modification_agent import flight_modification
from lost_baggage_agent import lost_baggage
load_dotenv(override=True)


# 定義分派代理人的指令，產生一個包含上下文的訊息，協助代理人根據客戶請求進行轉移
def triage_instructions(context_variables):
    customer_context = context_variables.get("customer_context", None)  # 取得客戶的上下文資訊
    flight_context = context_variables.get("flight_context", None)  # 取得航班的上下文資訊
    return f"""你的任務是對使用者的請求進行分派，並呼叫工具將請求轉移到正確的意圖。
                一旦你準備好將請求轉移到正確的意圖，請呼叫工具進行轉移。
                你不需要知道具體的細節，只需了解請求的主題。
                當你需要更多資訊以分派請求至合適的代理人時，請直接提出問題，而不需要解釋你為什麼要問這個問題。
                不要與使用者分享你的思考過程！不要擅自替使用者做出不合理的假設。
                這裡是客戶的上下文資訊: {customer_context}，航班的上下文資訊在這裡: {flight_context}"""

context_variables = {
    "customer_context": """這是你已知的客戶詳細資訊：
                            1. 客戶編號（CUSTOMER_ID）：customer_67890
                            2. 姓名（NAME）：陳明
                            3. 電話號碼（PHONE_NUMBER）：138-1234-5678
                            4. 電子郵件（EMAIL）：chenming@example.com
                            5. 身份狀態（STATUS）：白金會員
                            6. 帳戶狀態（ACCOUNT_STATUS）：活躍
                            7. 帳戶餘額（BALANCE）：¥0.00
                            8. 位置（LOCATION）：北京市朝陽區建國路88號，郵遞區號：100022
                            """,
    "flight_context": """客戶有一趟即將出發的航班，航班從北京首都國際機場（PEK）飛往上海浦東國際機場（PVG）。
                            航班號為 CA1234。航班的起飛時間為 2025 年 4 月 1 日，北京時間下午 3 點。""",
}

prompt_temp = triage_instructions(context_variables)

triage_agent = Agent(
    name="Triage Agent",  # 代理人名稱：分類代理人
    instructions=prompt_temp,  # 呼叫分派指令，根據上下文協助處理
    handoffs=[flight_modification, lost_baggage],
    model='gpt-5'
)

async def main():
    result = await Runner.run(triage_agent, "我的航班延誤了，我該怎麼辦？")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())