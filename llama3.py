from openai import OpenAI
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['long-chat'] = []
app.config['total'] = []


@app.route('/',methods = ['POST', 'GET'])
def index():
  if request.method == 'POST':
  # 渲染模板，并将内容传递给模板
    return render_template('h1.html')
  else:
    return render_template('h1.html')


@app.route('/h1',methods = ['POST', 'GET'])
def h1():
  if request.method == 'POST':
    app.config['total'].append(request.form['name'])
    user = '用中文回答以下问题：' + request.form['name']
    ctext = {"role": "user", "content":user}

    app.config['long-chat'].append(ctext)
    text = ""
    client = OpenAI(
      base_url="https://integrate.api.nvidia.com/v1",
      api_key="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"
    )
    completion = client.chat.completions.create(
      model="meta/llama3-70b-instruct",
      messages=app.config['long-chat'],
      temperature=0.5,
      top_p=1,
      max_tokens=1024,
      stream=True
    )

    for chunk in completion:
      if chunk.choices[0].delta.content is not None:
        text += chunk.choices[0].delta.content

    stext = {"role": "assistant", "content":text}
    app.config['long-chat'].append(stext)
    app.config['total'].append(text)

    return render_template('h1.html', content=text, total=app.config['total'])


if __name__ == '__main__':
  app.run(debug=True)

