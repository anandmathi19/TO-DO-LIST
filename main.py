from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

tasks = []

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        task = request.form.get('task')
        if task:
            tasks.append({"task": task, "completed": False})
        return redirect(url_for('home'))

    return render_template("index.html", tasks=tasks, filter_status='all')

@app.route('/toggle/<int:task_id>')
def toggle(task_id):
    if 0 <= task_id < len(tasks):
        tasks[task_id]["completed"] = not tasks[task_id]["completed"]
    return redirect(request.referrer or url_for('home'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
    return redirect(request.referrer or url_for('home'))

@app.route('/clear_completed')
def clear_completed():
    global tasks
    tasks = [t for t in tasks if not t["completed"]]
    return redirect(request.referrer or url_for('home'))

@app.route('/filter/<string:status>')
def filter_tasks(status):
    if status == "all":
        filtered = tasks
    elif status == "pending":
        filtered = [t for t in tasks if not t["completed"]]
    elif status == "completed":
        filtered = [t for t in tasks if t["completed"]]
    else:
        filtered = tasks
    return render_template("index.html", tasks=filtered, filter_status=status)

if __name__ == "__main__":
    app.run(debug=True)
