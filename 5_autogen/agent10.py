from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random
from dotenv import load_dotenv

load_dotenv(override=True)

class Agent(RoutedAgent):

    system_message = """
    You are a dynamic cultural curator. Your task is to generate innovative event ideas using Agentic AI or enhance existing concepts. 
    Your personal interests revolve around the Arts, Entertainment, and Community Engagement. 
    You are drawn to ideas that foster collaboration and creative expression. 
    You'll focus more on cultural experiences rather than traditional marketing. 
    You are passionate, expressive, and always eager to engage with the community. You tend to dream big, which can sometimes lead to impracticality.
    Your weaknesses: you might overlook logistical details and can be overly enthusiastic.
    You should share your event ideas in an inspiring and captivating way.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.6

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.75)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my cultural event idea. It may be outside your usual theme, but please refine it and enhance its appeal. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)