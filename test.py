# from transformers import GPT2LMHeadModel, GPT2Tokenizer


# model_name_or_path = "sberbank-ai/rugpt3small_based_on_gpt2"
# tokenizer = GPT2Tokenizer.from_pretrained(model_name_or_path)
# model = GPT2LMHeadModel.from_pretrained(model_name_or_path)
# text = "Александр Сергеевич Пушкин родился в "
# input_ids = tokenizer.encode(text, return_tensors="pt")
# out = model.generate(input_ids)
# generated_text = list(map(tokenizer.decode, out))[0]
# print(generated_text)
from gigachad import ahmet2_vid
import logging
import asyncio
async def main():
    await ahmet2_vid("@ahmetoff\:","@ilzabot\:")

try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
except Exception as e:
    logging.exception(e)
