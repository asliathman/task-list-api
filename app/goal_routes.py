from app import db
from app.models.task import Task
from app.models.goal import Goal
import requests
from flask import Blueprint, jsonify, request
from sqlalchemy import desc
from datetime import date
import os

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["GET"])
def read_goals():
    goals = Goal.query.all()
    goals_response = [{"id": goal.id, "title": goal.title} for goal in goals]

    return jsonify(goals_response), 200


@goals_bp.route("", methods=["POST"])
def add_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal(title=request_body["title"])

        db.session.add(new_goal)
        db.session.commit()

        response = {
            "goal": {
                "id": new_goal.id,
                "title": new_goal.title,
            }
        }
        return jsonify(response), 201

    except KeyError:
        return jsonify({"details": "Invalid data"}), 400


@goals_bp.route("/<id>", methods=["GET"])
def read_one_goal(id):
    goal = Goal.query.get(id)
    if goal is None:
        return jsonify(None), 404

    return {
        "goal": {
            "id": goal.id,
            "title": goal.title
        }
    }


@goals_bp.route("/<id>", methods=["DELETE"])
def delete_one_goal(id):
    goal = Goal.query.get(id)
    if goal is None:
        return jsonify(None), 404

    db.session.delete(goal)
    db.session.commit()

    response = {
        'details': f'Goal {goal.id} "{goal.title}" successfully deleted'
    }
    return jsonify(response), 200


@goals_bp.route("/<id>", methods=["PUT"])
def update_a_goal(id):
    goal = Goal.query.get(id)
    if goal is None:
        return jsonify(None), 404

    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()

    response = {
        "goal": {
            "id": goal.id,
            "title": goal.title
        }
    }
    return jsonify(response), 200


@goals_bp.route("/<id>/tasks", methods=["POST"])
def link_task_to_goal(id):
    request_body = request.get_json()

    task_ids = request_body["task_ids"]
    tasks = [Task.query.get(task_id) for task_id in task_ids]

    goal = Goal.query.get(id)
    goal.tasks = tasks

    db.session.commit()

    response = {
        "id": goal.id,
        "task_ids": task_ids
    }
    return jsonify(response)


@goals_bp.route("/<id>/tasks", methods=["GET"])
def read_tasks_from_goal(id):
    goal = Goal.query.get(id)
    if goal is None:
        return jsonify(None), 404

    tasks_response = [task.to_dict() for task in goal.tasks]

    response_body = {
        "id": goal.id,
        "title": goal.title,
        "tasks": tasks_response
    }
    return jsonify(response_body)