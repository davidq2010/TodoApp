import React, {useState, useEffect} from 'react';
import {Link} from 'react-router-dom';

function Tasks() {

  const [tasks, setTasks] = useState([]);

  const fetchTasks = async () => {
    const resp = await fetch('/tasks');
    const data = await resp.json();
    console.log('Fetched data type: ' + typeof(data));
    setTasks(data);
  }

  // When I put tasks in the dep array here I get inf loop.
  // Must be b/c tasks has "changed" even though contents may be the same.
  useEffect(() => {
    fetchTasks();
  }, []);

  const deleteTask = async (taskID) => {
    console.log("Deleting task " + taskID);
    const resp = await fetch(`/tasks/${taskID}`, {
      method: 'DELETE',
    });
    const data = await resp.json();
    console.log(data);
    // Also look into simply deleting task from tasks state variable (using
    // filter).
    fetchTasks();
  }

  // TODO: Sort the tasks by priority and then by creation time.
  // TODO: Display days since creation.
  // TODO: In Link pass prop containing deleteTask function
  // TODO: At end here, render createTask component instead of sep page
  return (
    <>
      {tasks.map((task) => {
        return (
          <div key={task._id}>
            <li>{task.description} | {task.priority}</li>
            <button onClick={() => deleteTask(task._id)}>Delete</button>
            <Link to={`/tasks/${task._id}`}>Update Task</Link>
          </div>
        );
      })}
    </>
  );
}

export default Tasks;
