from crypt import methods
import datetime
import uuid

from flask import Blueprint, render_template, request, redirect, url_for, current_app
from commonLibs.initialiseLogging import InitialiseLogging
from commonLibs.globalVariables import GlobalVariables
from commonLibs.commonConfigs import CommonConfigs

pages = Blueprint("habits",__name__,template_folder="templates")

InitialiseLogging().setupLogging()
GlobalVariables.LOGGER.info("Habit Tracker")

@pages.context_processor
def calcDateRange():
    def getDateRange(startDate: datetime.datetime):
        dates = [(startDate + datetime.timedelta(days=diff)).date() for diff in range(-3,4)]
        GlobalVariables.LOGGER.info("Date range : {}".format(dates))
        return dates
    return {"dateRange":getDateRange}

@pages.route("/habit-tracker",methods=["GET"])
def homePage():
    dateStr = request.args.get("date")
    GlobalVariables.LOGGER.info("Home page selected date : {}".format(dateStr))
    if dateStr:
        selectedDate = datetime.datetime.strptime(dateStr,"%Y-%m-%d")
    else:
        selectedDate = CommonConfigs().getTodayDate()
    
    GlobalVariables.LOGGER.info("Inside home page...")

    completions = [
        habit["habitID"]
        for habit in current_app.db.completions.find({"date":selectedDate})
    ]

    habits = current_app.db.habits.find({"addedDate":{"$lte":str(selectedDate)}})

    GlobalVariables.LOGGER.info("Habits on date {} : {}".format(selectedDate,habits))

    return render_template(
        "index.html",
        habits=habits,
        title="Habit Tracker - Home",
        selectedDate=selectedDate,
        completions=completions
        ), 200

@pages.route("/habit-tracker/add",methods=["GET","POST"])
def addHabit():
    GlobalVariables.LOGGER.info("Inside add habit page...")
    todayDate = CommonConfigs().getTodayDate()
    if request.method == "POST":
        habit = request.form.get("habit")
        GlobalVariables.LOGGER.info("Habit : {}".format(habit))
        current_app.db.habits.insert_one({"_id":uuid.uuid4().hex,"name":habit,"addedDate":str(todayDate)})
    
    return render_template("addHabit.html",title="Habit Tracker - Add Habit",selectedDate=todayDate), 201

@pages.route("/complete",methods=["POST"])
def complete():
    habitID = request.form.get("habitID")
    dateString = request.form.get("date")
    GlobalVariables.LOGGER.info("Date of completion type {} : {}".format(type(dateString),dateString))
    date = datetime.datetime.strptime(dateString.split()[0],"%Y-%m-%d")
    current_app.db.completions.insert_one({"habitID":habitID,"date":date})

    return redirect(url_for("habits.homePage",date=dateString.split()[0]))