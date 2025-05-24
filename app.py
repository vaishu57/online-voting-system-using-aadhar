from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Sample user and candidate data
users = {
    "123456789012": {
        "name": "Rahul Sharma",
        "aadhar": "123456789012",
        "address": "Guntur",
        "hasVoted": False,
        "image": "https://upload.wikimedia.org/wikipedia/commons/1/1e/Prime_Minister_Of_Bharat_Shri_Narendra_Damodardas_Modi_with_Shri_Rohit_Gurunath_Sharma_%28Cropped%29.jpg"
    },
    "987654321098": {
        "name": "Priya Singh",
        "aadhar": "987654321098",
        "address": "Vijayawada",
        "hasVoted": False,
        "image": "https://upload.wikimedia.org/wikipedia/commons/7/73/PV_Sindhu_headshot.jpg"
    },
    "22FE1A423742": {
        "name": "Pathan Ruksana Khathun",
        "aadhar": "22FE1A423742",
        "address": "Tenali",
        "hasVoted": False,
        "image": "https://cdn.britannica.com/25/222725-050-170F622A/Indian-cricketer-Mahendra-Singh-Dhoni-2011.jpg"
    },
    "556677889900": {
        "name": "Ajay Kumar",
        "aadhar": "556677889900",
        "address": "Hyderabad",
        "hasVoted": False,
        "image": "https://www.hindustantimes.com/static-content/1y/cricket-logos/players/virat-kohli.png"
    }
}

candidates = [
    {"id": 0, "name": "Janasena", "symbol": "🥛", "votes": 0},
    {"id": 1, "name": "YSRCP", "symbol": "🏴", "votes": 0},
    {"id": 2, "name": "Congress", "symbol": "✋", "votes": 0}
]

correct_password = "admin123"
serial_number = 1
vote_count = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_voter', methods=['POST'])
def check_voter():
    global users
    data = request.json
    aadhar_number = data.get("aadhar")
    if aadhar_number in users:
        user = users[aadhar_number]
        if not user["hasVoted"]:
            return jsonify({"status": "success", "user": user})
        else:
            return jsonify({"status": "error", "message": "You have already voted!"})
    else:
        return jsonify({"status": "error", "message": "Aadhaar number not found."})

@app.route('/cast_vote', methods=['POST'])
def cast_vote():
    global users, candidates, serial_number, vote_count
    data = request.json
    aadhar_number = data.get("aadhar")
    candidate_id = data.get("candidate_id")
    user = users.get(aadhar_number)

    if user and not user["hasVoted"]:
        user["hasVoted"] = True
        candidates[candidate_id]["votes"] += 1
        vote_count += 1
        serial_number += 1
        return jsonify({"status": "success", "message": f"You have successfully voted for {candidates[candidate_id]['name']}!"})
    return jsonify({"status": "error", "message": "Voting failed."})

@app.route('/check_password', methods=['POST'])
def check_password():
    data = request.json
    password = data.get("password")
    if password == correct_password:
        return jsonify({"status": "success", "candidates": candidates, "users": users})
    return jsonify({"status": "error", "message": "Incorrect password."})

if __name__ == '__main__':
    app.run(debug=True)
