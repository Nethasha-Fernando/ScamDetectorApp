from flask import Flask, render_template, request
from scam_logic import detect_scam_keywords, ask_gpt_if_scam, scam_confidence_score,highlight_keywords


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/result", methods=["POST"])    
def result():
    message = request.form.get('message', '').strip()

    if not message:
        return render_template(
            'result.html',
            result="⚠️ You must enter a message to scan.",
            ai_result="Not available.",
            confidence_score=0,
            message=""
        )

    keywords_found = detect_scam_keywords(message)
    if keywords_found:
        result_text = f"⚠️ Potential Scam! Found keywords: {', '.join(keywords_found)}"
        highlighted_message = highlight_keywords(message, keywords_found)
    else:
        result_text = "✅ This message appears to be safe based on keywords."
        highlighted_message = message

    ai_result = ask_gpt_if_scam(message)

    confidence = scam_confidence_score(keywords_found)

    return render_template(
            'result.html',
            result=result_text,
            ai_result=ai_result,
            confidence_score=confidence ,
            message=highlighted_message
        )

if __name__ == '__main__':
    app.run(debug=True)











