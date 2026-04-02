import google.generativeai as genai

genai.configure(api_key="AIzaSyAhpLODE-P8UxU6UxQtb361SFuN5yiky_I")

for m in genai.list_models():
    print(m.name, m.supported_generation_methods)