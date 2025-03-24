from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from connection import ConnectionManager
from RAW.RAW import GroqLLM, Tool
from dotenv import load_dotenv
import os
import re
import json
import asyncio
from agent import file_formatting_agent

load_dotenv()
app = FastAPI()
manager = ConnectionManager()


@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await manager.connect(websocket, session_id)
    async def reply_def(reply: str):
        await manager.send_personal_message(reply, session_id)
        data = await manager.receive_message(session_id=session_id)
        json_data = json.loads(data)
        message = json_data.get('message', '')
        mode = json_data.get('mode', '')
        return json_data
    
    reply_tool = Tool(
        name='reply',
        description='use this tool to ask questions to the user or give replies between inverted commas ""',
        action=reply_def,
        example='reply:"My name is MARIA"',
        test_payloads=['"my name is maria"']
    )

    agent = file_formatting_agent.file_formatting_agent(tools=[reply_tool], subordinates=[])

    print(agent.system_prompt)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                json_data = json.loads(data)
                message = json_data.get('message', '') 
                mode = json_data.get('mode', '')

                # agent.set_mode(mode)                   
                
                async def process_agent_output():
                    try:
                        async for chunk in agent(message):
                            try:
                                # Try to parse as JSON first
                                json_chunk = json.loads(chunk)
                                json_output = json.dumps(json_chunk)
                            except:
                                # If not JSON, use regex to extract key-value pairs
                                pattern = r'(?P<key>Thought|Action|Observation|Answer):\s*"?([^"\n]+)"?'
                                matches = re.finditer(pattern, chunk)
                                result = {}
                                for match in matches:
                                    key = match.group("key")
                                    value = match.group(2)
                                    result[key] = value
                                json_output = json.dumps(result, indent=2) if result else json.dumps({})
                            
                            # Send the processed chunk immediately
                            response = {"message": chunk, "json": json_output}
                            await manager.send_personal_message(json.dumps(response), session_id)

                            try:
                                json_data = json.loads(json_output)
                                if 'Answer' in json_data:
                                    await manager.send_personal_message(json_data['Answer'], session_id)
                            except:
                                pass
                            
                            await asyncio.sleep(0.1)
                    except Exception as e:
                        print(f"Error in process_agent_output: {e}")
                        await manager.send_personal_message(json.dumps({"error": str(e)}), session_id)
               
                process_task = asyncio.create_task(process_agent_output())
       
                await process_task
                
            except WebSocketDisconnect:
                await manager.disconnect(session_id)
                break
            except Exception as e:
                print(f"Error processing message: {e}")
                error_response = {"error": str(e)}
                await manager.send_personal_message(json.dumps(error_response), session_id)
    except WebSocketDisconnect:
        await manager.disconnect(session_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8900, reload=False)