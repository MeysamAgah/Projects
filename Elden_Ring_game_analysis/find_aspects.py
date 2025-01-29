# using hugging face pre-trained models
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# using instruct absa which is state of art model for Aspect Based Sentiment Analysis
tokenizer = AutoTokenizer.from_pretrained("kevinscaria/joint_tk-instruct-base-def-pos-neg-neut-combined")
model = AutoModelForSeq2SeqLM.from_pretrained("kevinscaria/joint_tk-instruct-base-def-pos-neg-neut-combined")

def find_aspects(text):
  """
  this function well read any text as input and output aspects inside text as a list
  """
  bos_instruction = """Definition: The output will be the aspects (both implicit and explicit) and the aspects sentiment polarity. In cases where there are no aspects the output should be noaspectterm:none.
      Positive example 1-
      input: I charge it at night and skip taking the cord with me because of the good battery life.
      output: battery life:positive,
      Positive example 2-
      input: I even got my teenage son one, because of the features that it offers, like, iChat, Photobooth, garage band and more!.
      output: features:positive, iChat:positive, Photobooth:positive, garage band:positive
      Negative example 1-
      input: Speaking of the browser, it too has problems.
      output: browser:negative
      Negative example 2-
      input: The keyboard is too slick.
      output: keyboard:negative
      Neutral example 1-
      input: I took it back for an Asus and same thing- blue screen which required me to remove the battery to reset.
      output: battery:neutral
      Neutral example 2-
      input: Nightly my computer defrags itself and runs a virus scan.
      output: virus scan:neutral
      Now complete the following example-
      input: """
  delim_instruct = ''
  eos_instruct = ' \noutput:'
  tokenized_text = tokenizer(bos_instruction + text + delim_instruct + eos_instruct, return_tensors="pt")
  output = model.generate(tokenized_text.input_ids)
  aspects_sentiment = tokenizer.decode(output[0], skip_special_tokens=True)
  aspects = []
  for a in aspects_sentiment.split(', '):
    aspects.append(a.split(':')[0])
  return aspects
