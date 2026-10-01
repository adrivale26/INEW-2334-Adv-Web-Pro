
from flask import Flask 
from flask import jsonify
from flask import request

app = Flask(__name__)

#custom error handlers
@app.errorhandler(400)
def bad_request_error(e):
   return jsonify({"Error": f"Bad request", "Status": 400}), 400


@app.errorhandler(404)
def page_not_found(e):
   return jsonify({"Error": f"Page not found", "Status": 404}), 404

tasks = [
    {"id": 1, "title": "Go to the doctor for physical" ,"priority": "high", "completed": False , "due_date": "2026-10-01"},
    {"id": 2, "title": "Pickup dry cleaning" ,"priority": "low"  ,"completed": True, "due_date": "2026-09-24" },
    {"id": 3, "title": "Take dog to the vet" ,"priority": "medium"  ,"completed": False , "due_date": "2026-10-05" },
    {"id": 4, "title": "Buy groceries" ,"priority": "low"  ,"completed": True , "due_date": "2026-09-30" }
]

priorities = {"low", "medium", "high"}

#return all tasks + priority filtering
@app.route("/api/tasks", methods=["GET"])
def get_tasks():
   filter_priority = request.args.get("priority") 
   if filter_priority: #filter priority
      filtered = [t for t in tasks if t["priority"].lower() == filter_priority.lower()] #if priority = priority_filter then return
      return jsonify({"count": len(filtered), "data": filtered}), 200 
   return jsonify({"count": len(tasks), "data": tasks}), 200 # return the tasks with 200 status code



#return single task or 404 error
@app.route("/api/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id): #get task by id
   task = next((t for t in tasks if t["id"] == task_id), None) #if task_id matches then set to task_id
   if not task:
      return jsonify({"Error Msg": f"Task {task_id} was not found.", "Status": 404}), 404
   return jsonify({"data": task}), 200

#create task and return error message 
@app.route("/api/tasks", methods=["POST"]) 
def create_task():
   data = request.get_json()
   if not data: 
      return jsonify({"Error Msg": "Missing JSON request body", "Status": 400}), 400 #400:Bad request

#check if title/priority fields are valid
   if "title" not in data or "priority" not in data:
      return jsonify({"Error Msg": "title and priority are required", "Status": 400}), 400

#validate if title is a string and if priority is valid
#get title instead of whole data object
   if not isinstance(data.get("title"), str) or not data["title"]:
      return jsonify({"Error Msg": f" 'title' must be a string and cannot be empty", "Status": 422}), 422
   if data["priority"].lower() not in priorities:
         return jsonify({"Error Msg": f"Invalid priority: must be one of the following {priorities}", "Status": 422}), 422 #422:Unprocessable Content


#create task with 201 status code 
   new_task_id = max([t["id"] for t in tasks], default=0) + 1
   new_task = {
   "id": new_task_id,
   "title": data["title"],
   "priority": data["priority"].lower(),
   "completed": bool(data.get("completed", False)),
   "due_date": data.get("due_date", "N/A")
}
   tasks.append(new_task)
   return jsonify({"Message": "Task successfully created", "data": new_task}), 201

#update task
@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id): #get task id 
   task = next((t for t in tasks if t["id"] == task_id), None) #if task_id matches then set to task_id
   if not task: 
      return jsonify({"Error Msg": f"Task {task_id} was not found. Unable to update", "Status": 404}), 404

   #validate again and set fields to empty fields
   data = request.get_json()
   if not data: 
      return jsonify({"Error Msg": "Missing JSON request body", "Status": 400}), 400

   #check if title is valid
   if "title" in data:
      if not isinstance(data.get("title"), str) or not data["title"]:
         return jsonify({"Error Msg": f" 'title' must be a string and cannot be empty", "Status": 422}), 422
      task["title"] = data["title"] #update title


   #check if priority is valid
   if "priority" in data:
      if data["priority"].lower() not in priorities:
            return jsonify({"Error Msg": f"Invalid priority: must be one of the following {priorities}", "Status": 422}), 422 
      task["priority"] = data["priority"] #update priority

   #update task + message
   if "completed" in data:
      task["completed"] = bool(data["completed"]) 
   return jsonify({"Message": "Task successfully updated", "Status": 200}), 200

#delete task and check display message
@app.route("/api/tasks/<int:task_id>", methods=['DELETE'])
def delete_task_id(task_id):
   task = next((t for t in tasks if t["id"] == task_id), None) #if task_id matches then set to task_id
   if not task: 
       return jsonify({"Error Msg": f"Task {task_id} was not found. Unable to delete.", "Status": 404}), 404
   task = [t for t in tasks if t["id"] != task_id]
   return jsonify({"Message": f"Task {task_id} was successfully deleted.", "Status": 200 }), 200
   

#starts flask dev server on port 5003 since port 5000 is in use, debug mode on
if __name__ == "__main__":
   app.run(debug=True, port=5003)


