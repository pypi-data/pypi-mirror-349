from autogen_core.memory import ListMemory


class ListMemory(ListMemory):
    """Simple chronological list-based memory implementation.

    This memory implementation stores contents in a list and retrieves them in
    chronological order. It has an `update_context` method that updates model contexts
    by appending all stored memories.

    The memory content can be directly accessed and modified through the content property,
    allowing external applications to manage memory contents directly.

    Example:

        .. code-block:: python

            import asyncio
            from saptiva_agents.memory import ListMemory, MemoryContent
            from saptiva_agents.core import BufferedChatCompletionContext


            async def main() -> None:
                # Initialize memory
                memory = ListMemory(name="chat_history")

                # Add memory content
                content = MemoryContent(content="User prefers formal language", mime_type="text/plain")
                await memory.add(content)

                # Directly modify memory contents
                memory.content = [MemoryContent(content="New preference", mime_type="text/plain")]

                # Create a model context
                model_context = BufferedChatCompletionContext(buffer_size=10)

                # Update a model context with memory
                await memory.update_context(model_context)

                # See the updated model context
                print(await model_context.get_messages())


            asyncio.run(main())

    Args:
        name: Optional identifier for this memory instance

    """
    pass

