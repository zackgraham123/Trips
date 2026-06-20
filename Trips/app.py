from flask import Flask, render_template, request

app = Flask(__name__)

MILESTONES = {
    "Canada's Flights": 600,
    "Canada's AirBnB (Deposit)": 125,
    "Canada's AirBnB (Rest)": 175,
    "Canada's Transport (To & From Dublin Airport)": 20,
    "Canada's Hotel": 95,
    "Lithuania's Flights": 400,
    "Lithuania's Hotel": 185,
    "Canada's Spending Money": 450,
    "Lithuania's Spending Money": 100
}

TARGET = sum(MILESTONES.values())


def calculate_spent(paid):
    return sum(MILESTONES[name] for name in paid)


def total_progress(balance, paid):
    return balance + calculate_spent(paid)


def build_affordable(balance, paid):
    return [
        (name, cost)
        for name, cost in MILESTONES.items()
        if name not in paid and cost <= balance
    ]


def build_basket(balance, paid):
    options = sorted(
        [(n, c) for n, c in MILESTONES.items() if n not in paid],
        key=lambda x: x[1]
    )

    basket = []
    remaining = balance

    for name, cost in options:
        if cost <= remaining:
            basket.append((name, cost))
            remaining -= cost

    return basket, remaining


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        balance = float(request.form.get("balance", 0))
        paid = request.form.getlist("paid")

        spent = calculate_spent(paid)
        progress = balance + spent
        percentage = min(progress / TARGET * 100, 100)
        remaining = max(TARGET - progress, 0)

        affordable = build_affordable(balance, paid)
        basket, leftover = build_basket(balance, paid)

        next_milestone = None
        for name, cost in MILESTONES.items():
            if name not in paid:
                next_milestone = (name, cost)
                break

        return render_template(
            "index.html",
            milestones=MILESTONES,
            balance=balance,
            paid=paid,
            spent=spent,
            progress=progress,
            percentage=percentage,
            remaining=remaining,
            target=TARGET,
            affordable=affordable,
            basket=basket,
            leftover=leftover,
            next_milestone=next_milestone
        )

    return render_template(
        "index.html",
        milestones=MILESTONES
    )


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)