
from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.message import EmailMessage
import os
import traceback

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "✅ Lawyer Appointment Server is Running."

@app.route("/submit-appointment", methods=["POST"])
def submit_appointment():
    try:
        data = request.get_json()
        name = data.get("name", "")
        phone = data.get("phone", "")
        email = data.get("email", "")
        message = data.get("message", "")

        content = f"""📮 新律師預約表單提交如下：

👤 姓名：{name}
📞 電話：{phone}
📧 Email：{email}
📝 留言內容：{message}
"""

        sender_email = os.getenv("GMAIL_ACCOUNT")
        sender_pass = os.getenv("GMAIL_PASSWORD")
        receiver_email = os.getenv("MAIL_RECEIVER")

        if not all([sender_email, sender_pass, receiver_email]):
            return jsonify({"success": False, "error": "缺少必要的環境變數"}), 500

        msg = EmailMessage()
        msg["Subject"] = "📮 LawAI 律師預約通知"
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg.set_content(content)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, sender_pass)
            smtp.send_message(msg)

        return jsonify({"success": True, "message": "預約已成功送出！"})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port)
