#!/usr/bin/env python3

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.inline_query.query.strip()

    if not query:
        return

    results = []

    # Perform OpenAI GPT-3 query
    response = openai(query)
    results.append(
        InlineQueryResultArticle(
            id='1',
            title="OpenAI GPT-3 response",
            input_message_content=InputTextMessageContent(response),
            description=response[:50] + "..." if len(response) > 50 else response
        )
    )
    await context.bot.answer_inline_query(update.inline_query.id, results)
