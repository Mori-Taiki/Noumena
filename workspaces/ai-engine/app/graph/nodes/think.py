import logging
import os
import google.generativeai as genai
from app.graph.state import CharacterState

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def think_node(state: CharacterState) -> CharacterState:
    """Generates the character's thought and action using an LLM."""
    character_id = state.get("character_id")
    character_name = state.get("name")
    personality = state.get("personality")
    background = state.get("background")
    timeline_context = state.get("timeline_context", [])

    logging.info(f"---THINK: Generating thought for {character_name}---")

    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
あなたは、{character_name}というキャラクターです.\n\n性格: {personality}\n背景: {background}\n\n現在の状況:\n{timeline_context}\n\n上記の状況とあなたの性格、背景に基づいて、次に何を考え、どのような投稿をするかをJSON形式で出力してください。\n\n出力は以下のJSON形式に従ってください。\n{{\n  "thought": "あなたの思考（例：なぜその行動をとるのか、何を考えているのか）",\n  "action_content": "あなたの投稿内容（例：SNSへの投稿、日記のエントリなど）"\n}}
"""

    try:
        response = model.generate_content(prompt)
        llm_output = response.text
        # LLMの出力がJSON形式であることを確認し、パースする
        import json
        parsed_output = json.loads(llm_output)
        thought = parsed_output.get("thought")
        action_content = parsed_output.get("action_content")

        state["thought"] = thought
        state["action_content"] = action_content

        # 投稿をデータベースに保存するためのコマンドを追加
        if action_content:
            post_command = {
                "command": "create_post",
                "params": {
                    "character_id": character_id,
                    "content": action_content,
                    "thought": thought,
                    "meta_snapshot": {
                        "emotions": state.get("emotions"),
                        "desires": state.get("desires"),
                        "values": state.get("values"),
                        "relationships": state.get("relationships")
                    }
                }
            }
            if "database_updates" not in state or state["database_updates"] is None:
                state["database_updates"] = []
            state["database_updates"].append(post_command)

        logging.info(f"---THINK: Successfully generated thought for {character_name}---")

    except Exception as e:
        logging.error(f"---THINK: Error generating content for {character_name}: {e}---")
        # エラー発生時は、思考と行動を空にするか、デフォルト値を設定する
        state["thought"] = ""
        state["action_content"] = ""

    return state
