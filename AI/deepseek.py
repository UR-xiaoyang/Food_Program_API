import requests
import json
from .deepseek_config import DeepSeekConfig

def call_deepseek_api(prompt: str):
    """
    使用 OpenRouter 调用 DeepSeek API。

    Args:
        prompt: 要发送给模型的用户提示。

    Returns:
        API 响应的 JSON 数据，如果出错则返回 None。
    """
    api_key = DeepSeekConfig.api_key
    model_name = DeepSeekConfig.model
    

    if not DeepSeekConfig.api_key:
        print(f"错误：DeepSeek配置中的api_key为空。")
        return None

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}" # 使用从配置中读取的 key
    }
    data = {
        "model": model_name, # 使用从配置中读取的 model
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status() # 如果状态码不是 2xx，则抛出 HTTPError
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求出错: {e}")
        # response 可能在 raise_for_status() 之前或之后为None或有值
        if 'response' in locals() and response is not None:
            try:
                print(f"响应状态码: {response.status_code}")
                print(f"响应内容: {response.text}") # 打印错误响应内容
            except Exception as print_e:
                print(f"打印响应时出错: {print_e}")
        return None

# 示例用法：
if __name__ == "__main__":
    user_prompt = "What is the meaning of life?"
    result = call_deepseek_api(user_prompt)
    if result:
        print("API 响应:")
        # 通常，聊天模型的响应在 result['choices'][0]['message']['content'] 中
        print(json.dumps(result, indent=2, ensure_ascii=False))
        # 打印模型回复的内容
        try:
            content = result['choices'][0]['message']['content']
            print("\n模型回复内容:")
            print(content)
        except (KeyError, IndexError) as e:
             print(f"\n无法从响应中提取内容: {e}")