from flask import Flask
app = Flask(__name__)
import requests

colors = ["red", "blue", "yellow", "green"]

def get_answers(json):
    answer_data = {
        'title': json['title'],
        'creator_username': json['creator_username']
    }
    answers = []
    for question in json['questions']:
        if question['type'] == 'quiz':
            correct_answers = []
            for i, choice in enumerate(question['choices']):
                if choice['correct']:
                    correct_answers.append(colors[i])
            answers.append(correct_answers)
        elif question['type'] == 'content':
            answers.append(None)
        elif question['type'] == 'open_ended':
            correct_answers = []
            for choice in question['choices']:
                if choice['correct']:
                    correct_answers.append(choice['answer'])
            answers.append(correct_answers)

    answer_data['answers'] = answers
    print(answers)
    return answer_data


@app.route("/getAnswers/<quizId>")
def kahoot_request(quizId):
    print(quizId)
    response = requests.get("https://play.kahoot.it/rest/kahoots/" + quizId)
    return get_answers(response.json())

@app.route('/')
def index():
    with open('index.html') as f:
        return f.read()

if __name__ == '__main__':
    app.run(port=80, debug=True, host="0.0.0.0")
