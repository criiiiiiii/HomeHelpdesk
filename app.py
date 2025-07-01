from flask import Flask, render_template, request, redirect
from datetime import datetime
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
DATA_FILE = "tickets.json"

# --- Email Config ---
SMTP_SERVER   = "smtp.mail.me.com"
SMTP_PORT     = 465
SMTP_USERNAME = "christian.sodeikat@icloud.com"
SMTP_PASSWORD = "attg-qxjb-jydg-twgq"
ADMIN_EMAIL   = "helpdesk@christiansodeikat.com"
CHRIS_EMAIL   = "christian.sodeikat@gmail.com"

def send_email(subject, body, to):
    msg = MIMEMultipart()
    msg['From']     = f"Your Home Helpdesk <{ADMIN_EMAIL}>"
    msg['To']       = to
    msg['Subject']  = subject
    msg['Reply-To'] = SMTP_USERNAME
    msg.attach(MIMEText(body, 'plain'))
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)

def load_tickets():
    if not os.path.exists(DATA_FILE):
        return {"active": [], "completed": [], "deleted": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_tickets(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def format_duration(created, closed):
    try:
        c = datetime.strptime(created, "%Y-%m-%d %H:%M")
        x = datetime.strptime(closed,  "%Y-%m-%d %H:%M")
        return (x - c).days
    except:
        return ""

@app.template_filter("duration")
def duration_filter(ticket):
    return format_duration(ticket.get("created",""), ticket.get("closed",""))

def get_priority_counts(tickets):
    counts = {"1":0,"2":0,"3":0,"4":0}
    for t in tickets:
        p = str(t.get("priority",""))
        if p in counts:
            counts[p] += 1
    return counts

def get_submitter_counts(tickets):
    counts = {
        "pmgialdi@gmail.com": 0,
        "christian.sodeikat@gmail.com": 0
    }
    for t in tickets:
        e = t.get("email")
        if e in counts:
            counts[e] += 1
    return counts

@app.route("/")
def index():
    data = load_tickets()
    return render_template("index.html",
                           active   = data["active"],
                           completed= data["completed"],
                           deleted  = data["deleted"])

@app.route("/dashboard")
def dashboard():
    data           = load_tickets()
    active_list    = data["active"]
    completed_list = data["completed"]
    deleted_list   = data["deleted"]
    total_list     = active_list + completed_list + deleted_list

    return render_template("dashboard.html",
        total            = len(total_list),
        active           = len(active_list),
        completed        = len(completed_list),
        deleted          = len(deleted_list),
        priority_counts  = {
          "total":     get_priority_counts(total_list),
          "active":    get_priority_counts(active_list),
          "completed": get_priority_counts(completed_list),
          "deleted":   get_priority_counts(deleted_list)
        },
        submitter_counts = {
          "total":     get_submitter_counts(total_list),
          "active":    get_submitter_counts(active_list),
          "completed": get_submitter_counts(completed_list),
          "deleted":   get_submitter_counts(deleted_list)
        }
    )

@app.route("/create", methods=["GET","POST"])
def create():
    if request.method=="POST":
        data = load_tickets()
        ticket_id = f"{len(data['active'])+len(data['completed'])+len(data['deleted'])+1:03}"
        user_email = request.form["email"]
        ticket = {
            "id": ticket_id,
            "name": request.form["name"],
            "description": request.form["description"],
            "priority": int(request.form["priority"]),
            "email": user_email,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "updated": "",
            "closed": ""
        }
        data["active"].append(ticket)
        save_tickets(data)

        subject = f"[Helpdesk] New Ticket #{ticket_id}: {ticket['name']}"
        body    = f"""Hello,

A new home helpdesk ticket has been created.

Ticket ID: {ticket['id']}
Name: {ticket['name']}
Description: {ticket['description']}
Priority: {ticket['priority']}
Created: {ticket['created']}

Thank you,
Your Home Helpdesk"""
        for recipient in (user_email, ADMIN_EMAIL, CHRIS_EMAIL):
            send_email(subject, body, recipient)

        return redirect("/")
    return render_template("create.html")

@app.route("/edit/<ticket_id>", methods=["GET","POST"])
def edit(ticket_id):
    data = load_tickets()
    for section in ("active","completed"):
        for ticket in data[section]:
            if ticket["id"]==ticket_id:
                if request.method=="POST":
                    ticket["name"]        = request.form["name"]
                    ticket["description"] = request.form["description"]
                    ticket["priority"]    = int(request.form["priority"])
                    ticket["updated"]     = datetime.now().strftime("%Y-%m-%d %H:%M")
                    save_tickets(data)

                    subject = f"[Helpdesk] Ticket #{ticket_id} Updated: {ticket['name']}"
                    body    = f"""Hello,

Your home helpdesk ticket has been updated.

Ticket ID: {ticket['id']}
Name: {ticket['name']}
Description: {ticket['description']}
Priority: {ticket['priority']}
Updated: {ticket['updated']}

Thank you,
Your Home Helpdesk"""
                    send_email(subject, body, ticket["email"])
                    return redirect("/")
                return render_template("edit.html", ticket=ticket)
    return redirect("/")

@app.route("/complete/<ticket_id>", methods=["POST"])
def complete(ticket_id):
    data = load_tickets()
    for i,ticket in enumerate(data["active"]):
        if ticket["id"]==ticket_id:
            ticket["closed"]=datetime.now().strftime("%Y-%m-%d %H:%M")
            data["completed"].append(ticket)
            del data["active"][i]
            save_tickets(data)
            return redirect("/")
    return redirect("/")

@app.route("/delete/<ticket_id>", methods=["POST"])
def delete(ticket_id):
    data = load_tickets()
    for section in ("active","completed"):
        for i,ticket in enumerate(data[section]):
            if ticket["id"]==ticket_id:
                data["deleted"].append(ticket)
                del data[section][i]
                save_tickets(data)
                return redirect("/")
    return redirect("/")

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5080)
