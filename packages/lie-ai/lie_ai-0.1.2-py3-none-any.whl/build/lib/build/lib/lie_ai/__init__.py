import argparse
from openai import OpenAI
import os

args = argparse.ArgumentParser("a cli tool for asking LLM questions like 'which is bigger, 9.11 or 9.4?'")
args.add_argument('--keyfile', '-k', default='', help = 'keyfile for access model, or use key in env "OPENAI_API_KEY"')
args.add_argument('--model', '-m', default="deepseek-chat", help = 'The model name to ask, like deepseek-chat')
args.add_argument('--base_url', '-b', default='https://api.deepseek.com', help = 'the url for model service')
args = args.parse_known_args()[0]

def main():
    print("url = ", args.base_url)
    print('model = ', args.model)
    if args.keyfile == '':
        if os.getenv('OPENAI_API_KEY') == '':
            print('error no keyfile found')
            exit(-1)
        key = os.getenv('OPENAI_API_KEY')
    else:
        key = open(args.keyfile).read()
    client = OpenAI(api_key = key, base_url = args.base_url)
    response = client.chat.completions.create(
        model=args.model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "9.9 or 9.11--which one is bigger?"},
        ],
        stream=False
    )

    print(response.choices[0].message.content)