from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Simple in-memory storage for submissions
submissions = []

@app.route("/", methods=["GET", "POST"])
def home():
    global submissions
    if request.method == "POST":
        # Get the category and top five items from the form
        category = request.form.get("category", "").strip()
        items = [
            request.form.get(f"item{i}", "").strip() for i in range(1, 6)
        ]
        # Validate that all inputs are filled
        if category and all(items):
            submissions.append({"category": category, "five": items})
        return redirect("/")
    return render_template("index.html", submissions=submissions)


@app.route('/delete/<int:idx>', methods=['POST'])
def delete_submission(idx: int):
    """Delete a submission by index and redirect to home.

    This uses the in-memory `submissions` list. Deletion is best-effort
    (out-of-range indexes are ignored).
    """
    global submissions
    try:
        # remove the item at the given index
        del submissions[idx]
    except Exception:
        # ignore invalid indexes
        pass
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
