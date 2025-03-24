from RAW import Agent, Tool, TextColor, BackgroundColor, Hook, HookTriggers
from typing import List, Dict
import re
import shlex

class ModeAgent(Agent):
    def __init__(
        self,
        llm,
        name: str = "",
        tool_name: str = "",
        personality: str = "",
        role: str = "",
        tools: List[Tool] = [],
        subordinates: List[Agent] = [],
        textColor: TextColor = TextColor.WHITE,
        backgroundColor: BackgroundColor = BackgroundColor.BLACK,
        modes: Dict[str, dict] = None,
        default_mode: str = "normal",
        hooks: List[Hook] = []
    ):
        self.shared_messages = [{"role": "system", "content": ""}]
        self.modes = modes or {
            "normal": {
                "description": "Provides quick and direct answers with minimal tools and your available action are rag_tool and reply",
                "example_session": """Question: What is the log of 500

Thought: I need to use the calculator tool to find the log of 500

Action: calculate: "math.log(500)"
PAUSE

Observation: 6.214608098422191

Thought: I now have the answer

Answer: The log of 500 is 6.214608098422191

Question: Tumhara naam kya hai

Thought: I need to give my name
Answer: reply: "My name is LOM"
PAUSE

Question: Virat Kholi kon he pata he tumhe?

Thought: I need to find information about Virat Kohli. This requires a web search to get current and accurate details about him.
Action: web_search: "who is virat kohli"
PAUSE

Observation: Virat Kohli is an Indian international cricketer and serves as captain of the Indian national team in all formats. He is considered one of the greatest players of all time, and is often referred to as the 'King of Chase'. He has many records including most centuries in both Test and One Day International cricket. He is a right-handed batsman and occasional right-arm medium-fast bowler. He currently plays for Royal Challengers Bangalore in the Indian Premier League and for the Indian national team.

Thought: I now have the information about Virat Kohli.

Answer: Virat Kohli is a leading international cricketer for India, widely regarded as one of the best players of all time. He is captain of the Indian national team and plays for Royal Challengers Bangalore in the Indian Premier League.
The tool web_search is not available in think mode
""",
                "tool_filter": lambda t: t.name in ["rag_tool", "reply","web_search_tool"],
                "text_color": TextColor.WHITE
            },
            "think": {
                "description": "Uses detailed reasoning with all available tools.",
                "example_session":"""

    Question: I want to extract text from a PDF file

    Thought: I need to ask for the file path

    Follow Up: Please provide the file path

    Through: Now I have the file path, I should use the pdf_extractor_tool to extract the text

    Action: pdf_extractor_tool('example.pdf')
    PAUSE

    Observation: Ok I have the text extracted from the PDF file

    Thought: Now I have the extracted text, I should display it to the user 

    Answer: Here is the text extracted from the PDF file:
    """,
                "tool_filter": lambda t: True,
                "text_color": TextColor.GREEN
            }
        }
        self.current_mode = default_mode
        example_session = self.modes[self.current_mode]["example_session"]

        super().__init__(
            llm=llm,
            name=name,
            tool_name=tool_name,
            exampleSession=example_session,
            role=role,
            tools=tools,
            textColor=textColor,
            backgroundColor=backgroundColor,
            personality=personality,
            hooks=hooks
        )
        self.messages = self.shared_messages
        self.all_tools = tools.copy()
        self.update_tools_and_prompt()

    def update_tools_and_prompt(self):
        mode_config = self.modes.get(self.current_mode, self.modes["normal"])
        self.tools = [tool for tool in self.all_tools if mode_config["tool_filter"](tool)]
        self.exampleSession = mode_config["example_session"]
        self.shared_messages[0] = {"role": "system", "content": self.makePrompt()}
        self.messages = self.shared_messages
        self.textColor = mode_config["text_color"]

    def set_mode(self, mode: str):
        if mode in self.modes:
            if self.current_mode != mode:
                # print(f"switching mode from {self.current_mode} to {mode}")
                self.current_mode = mode
                self.update_tools_and_prompt()
        else:
            raise ValueError(f"Mode '{mode}' is not supported. Available modes: {list(self.modes.keys())}")

    def makePrompt(self) -> str:
        mode_config = self.modes[self.current_mode]
        return f"""
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.
You are {self.name}, your role is {self.role}.

Your available actions are:
{"".join(tool.get_description() for tool in self.tools)}

Example Session:
{self.exampleSession}

Now it's your turn:
""".strip()

    async def __call__(self, message: str, mode: str = None):
        if mode:
            self.set_mode(mode)
        
        self.shared_messages.append({"role": "user", "content": message})
        
        if message:
            print("\n---------")
            print(self._color_text(self.name, TextColor.UNDERLINE, BackgroundColor.BLACK))
            print("---------\n")
            
            iterator = self.execute()
            while True:
                try:
                    show, result = await anext(iterator, (False, None))
                    if(show):
                        print(self._color_text(result, self.textColor, self.backgroundColor))
                    yield result
                except StopAsyncIteration as e:
                    print(e)
                    return
                except Exception as e:
                    return

    async def execute(self, max_iterations: int = 15):
        i: int = 0
        while i < max_iterations:
            result = self.llm.execute(messages=self.messages)
            yield True, result
            self.messages.append({"role": "assistant", "content": result})
            
            if "PAUSE" in result and "Action" in result:
                action = re.findall(r"Action: ([a-z_]+): (.+)", result, re.IGNORECASE)
                try:
                    if(len(action[0]) > 1):
                        chosen_tool = action[0][0]
                        args = action[0][1]
                    else:
                        chosen_tool = action[0][0]
                        args = ""
                    tool_found = False
                    for tool in self.tools:
                        if tool.name == chosen_tool:
                            try:
                                async for res in tool(*shlex.split(args)):
                                    show, result = (False, res[0]) if isinstance(res, (list, tuple)) and len(res) == 1 else (res if res else (False, None))
                                    try:
                                        if isinstance(result, dict) and "message" in result and "mode" in result:
                                            message = result["message"]
                                            mode = result["mode"]
                                            if mode in self.modes:
                                                self.set_mode(mode)
                                            yield show, f"Observation: {message}"
                                            self.messages.append({"role": "user", "content": message})
                                        else:
                                            yield show, result
                                            self.messages.append({"role": "user", "content": result})
                                    except Exception as e:
                                        yield True, f"Error processing result: {e}"
                                        self.messages.append({"role": "user", "content": f"Error processing result: {e}"})
                            except StopAsyncIteration:
                                return
                            except Exception as e:
                                print(f"Error executing tool: {e}")
                                yield True, f"Error executing tool: {e}"
                                self.messages.append({"role": "user", "content": f"Error executing tool: {e}"})
                                return
                            tool_found = True
                            break
                    if(not tool_found):
                        yield True, f"The tool {chosen_tool} is not available in {self.current_mode} mode"
                        self.messages.append({"role": "user", "content": f"The tool {chosen_tool} is not available in {self.current_mode} mode"})
                except Exception as e:
                    yield True, f"Failed to execute the chosen tool with the following error: {e}"
                    self.messages.append({"role": "user", "content": f"Failed to execute the chosen tool with the following error: {e}"})
            elif "Answer" in result:
                self.messages.append({"role": "assistant", "content": result})
                answer = re.search(r'Answer:\s*(.*)', result, re.IGNORECASE)
                for hook in self.hooks:
                    if hook.trigger == HookTriggers.ANSWER_MADE:
                        try:
                            async for hook_response in hook(self.messages):
                                print(f"hook response: {hook_response}")
                        except Exception as e:
                            print(f"error executing hook: {e}")
                yield True, answer.group(0)
                raise StopAsyncIteration(answer.group(0))
            
            i += 1