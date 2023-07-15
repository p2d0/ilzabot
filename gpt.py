#!/usr/bin/env python3

async def openai_gpt3_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    response = openai(update.message.text)
    await update.message.reply_text(response)
    if "нет" in response.lower():
        response = re.sub(r"[.,;:]", "", response);
        await gigachad_vid(f"{update.effective_user.first_name}\: {update.message.text}",f"iLzabot \: {response}")
        await update.message.reply_video("./output_final.mp4")

async def openai_trueilza_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    response = openai(update.message.text,"davinci:ft-personal-2022-12-26-20-48-26",max_tokens=128,prompt_ending=" ->",stop="\n",best_of=3)
    await update.message.reply_text(response)
    if "нет" in response.lower():
        response = re.sub(r"[.,;:]", "", response);
        await gigachad_vid(f"{update.effective_user.first_name}\: {update.message.text}",f"iLzabot \: {response}")
        await update.message.reply_video("./output_final.mp4")

async def openai_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # global previous_message;
    response = chatgpt(update.message.text);
    await update.message.reply_text(text=response
                                    # .replace("_", '\_')
                                    #   .replace("*", '\*')
                                    #   .replace("[", '\[')
                                    #   .replace("]", '\]')
                                    #   .replace("(", '\(')
                                    #   .replace(")", '\)')
                                    #   .replace("~", '\~')
                                    #   .replace("`", '\`')
                                    #   .replace(">", '\>')
                                    #   .replace("#", '\#')
                                    #   .replace("+", '\+')
                                    #   .replace("-", '\-')
                                    #   .replace("=", '\=')
                                    #   .replace("|", '\|')
                                    #   .replace("{", '\{')
                                    #   .replace("}", '\}')
                                    #   .replace(".", '\.')
                                    #   .replace("!", '\!')
                                    # .replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`").replace("+", "\\+").replace(".", "\\.").replace("=", "\\=").replace("]", "\\]")
                                    )
    if "нет" in response.lower() or "ильза" in update.message.text:
        response = re.sub(r"[.,;:]", "", response);
        await gigachad_vid(f"{update.effective_user.first_name}\: {update.message.text}",f"iLzabot \: {response}")
        await update.message.reply_video("./output_final.mp4")

def openai(text,model="text-davinci-003",max_tokens=512,prompt_ending="",stop=None,best_of=None):
    api_endpoint = "https://api.openai.com/v1/completions"
    api_key = "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"

    # Set the model and prompt for the generation request
    prompt = text.replace("@iLza_bot","").replace("/trueilza","").replace("/ilzapolite","").strip() + prompt_ending
    print(prompt)
    # Set the headers for the request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    # Set the payload for the request
    payload = {
        "model": model,
        "prompt": prompt,
        "max_tokens": max_tokens
    }

    if(stop):
        payload["stop"] = stop
    if(best_of):
        payload["best_of"] = best_of

    # Send the request to the API and get the response
    response = requests.post(api_endpoint, json=payload, headers=headers)

    # Check the status code of the response
    if response.status_code == 200:
        # Process the response
        response_data = response.json()
        # Do something with the response data
        print(response_data);
        return response_data['choices'][0]['text']
    else:
        # Handle the error
        raise Exception(response);
        # print(response)
        # # print(f"Error: {response.message}")
        # print(f"Error: {response.status_code}")

def chatgpt(text):
    global messages;
    api_endpoint = "https://api.openai.com/v1/chat/completions"
    api_key = "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"

    # Set the model and prompt for the generation request
    prompt = text.replace("@iLza_bot","").replace("/trueilza","").replace("/ilzapolite","").strip()
    print(prompt)
    # Set the headers for the request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    # Set the payload for the request
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": messages + [{"role": "user", "content": prompt}],
    }
    print(payload)

    # Send the request to the API and get the response
    response = requests.post(api_endpoint, json=payload, headers=headers)

    # Check the status code of the response
    if response.status_code == 200:
        # Process the response
        response_data = response.json()
        # Do something with the response data
        print(response_data);
        messages.append(response_data['choices'][0]['message']);
        return response_data['choices'][0]['message']["content"]
    else:
        # Handle the error
        raise Exception(response);
        # print(response)
        # print(f"Error: {response.message}")
        # print(f"Error: {response.status_code}")

async def openai_ilzapolite_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(openai(update.message.text,"curie:ft-personal-2022-12-28-11-57-22",max_tokens=64,prompt_ending=" ->",stop="\n",best_of=3))
