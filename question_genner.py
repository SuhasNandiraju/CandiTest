import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import numpy as np
from flask import Flask, request, redirect, jsonify

host = "0.0.0.0"

app = Flask(__name__)


def get_response(input_text,num_return_sequences,num_beams):
    batch = tokenizer.prepare_seq2seq_batch([input_text],truncation=True,padding='longest',max_length=60)
    batch['input_ids'] = torch.from_numpy(np.asarray(batch['input_ids']))
    batch['attention_mask'] = torch.from_numpy(np.asarray(batch['attention_mask']))

    batch = batch.to(torch_device)
    translated = model.generate(**batch,max_length=60,num_beams=num_beams, num_return_sequences=num_return_sequences, temperature=1.5)
    tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)
    return tgt_text

model_name = 'tuner007/pegasus_paraphrase'
torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name).to(torch_device)

print('Done Loading Model.')


resdict = {}

@app.route("/tests/get_test")
def get_tests():



    questions = request.args.getlist('questions') or ['what is 1+1?', 'who is john f. kenndy?', 'why is the sky blue?', 'why am i gay?']
    tests = request.args.get('tests') or 3
    tests = int(tests)

    print(questions)

    if tuple(questions)+tuple([tests]) in resdict:
        return resdict[tuple(questions)+tuple([tests])]


    qs = []
    for i in questions:
        qs.append(get_response(i, tests, 2*tests))


    rotated = list(zip(*qs[::-1]))
    rotated = [list(i) for i in rotated]

    resdict[tuple(questions)+tuple([tests])] = jsonify(rotated)

    return jsonify(rotated)


test = ['what is 1+1?', 'who is john f. kenndy?', 'why is the sky blue?', 'why am i gay?']
#print(get_tests())

if __name__ == "__main__":
    app.run(debug=True)



'''
while True:
    context = input('Enter the question: ')
    num_return_sequences=int(input('How many tests? '))
    num_beams=num_return_sequences*2
    print(get_response(context,num_return_sequences,num_beams))

'''
