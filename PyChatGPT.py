import openai
openai.api_key = "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"
model_engine = "text-davinci-003"
# 限制1024字节   512汉字
prompt = "用java写二叉树"
res = openai.Completion.create(
    engine=model_engine,
    prompt=prompt,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.5,
)
message = res.choices[0].text
print(message)