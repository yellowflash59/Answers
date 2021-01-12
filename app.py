from flask import Flask, jsonify,request

app = Flask(__name__)


@app.route("/this",methods = ['POST'])
def trial_api():
    req_data = request.get_json()
    myList = req_data['myList']
    myIntList = [x for x in myList if isinstance(x, int)]
    myStrList = [x for x in myList if isinstance(x, str)]
    valid_entries, invalid_entries = 0, 0
    myList2 = []
    for nums in myIntList:
        if nums > 0:
            valid_entries += 1
            myList2.append(nums)
        else:
            invalid_entries += 1
    for i in myStrList:
        invalid_entries += 1
    max_value = max(myIntList)
    min_value = min(myList2)
    avg = sum(myList2) / len(myList2)
    round_avg = round(avg,2)

    return jsonify(valid_entries=valid_entries,
                   invalid_entries=invalid_entries,
                   min=min_value, max=max_value,
                   average = round_avg)


if __name__ == "__main__":
    app.run(debug = True)
