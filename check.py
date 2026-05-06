import google.generativeai as genai

genai.configure(api_key="AIzaSyBSxmrdZT0-pfBSPH2OIi1Yy63Jq2P4kU0")

for m in genai.list_models():
    print(m.name)