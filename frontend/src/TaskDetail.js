import React, {useState, useEffect} from 'react';
import {useParams} from 'react-router-dom';

function TaskDetail(props) {
  const {id} = useParams();

  const [details, setDetails] = useState({
    description: '',
    priority: '',
    created_at: '',
    _id: '',
    detail: '',
    work_hr_est: ''
  });

  // Use useEffect to set value for all states
  useEffect(() => {
    const fetchTasks = async () => {
      console.log("Task id: " + id);
      const resp = await fetch(`/tasks/${id}`);
      const data = await resp.json();
      setDetails(data);
    }

    fetchTasks();
  }, []);

  const handleTaskChange = (e) => {
    setDetails({...details, description: e.target.value});
    console.log("Details: " + details);
  }

  const handleDetailChange = (e) => {
    setDetails({...details, detail: e.target.value});
    console.log("Details: " + details);
  }

  const handlePriorityChange = (e) => {
    setDetails({...details, priority: e.target.value});
    console.log("Details: " + details);
  }

  // TODO: Check if I can use this for both:
  // handleChange = (event) => {
  //   this.setState({[event.target.name]: event.target.value});
  // }

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Data to send: " + JSON.stringify(details))
    const resp = await fetch(`/tasks/${details['_id']}`, {
      method: 'PATCH',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(details)
    });
    console.log(resp);
    const data = await resp.json();
    console.log(data);
    props.history.push('/tasks');
  }

  const handleHourChange = async (e) => {
    // Positive number input only; JS regex: /pattern/modifiers (like g for
    // global)
    setDetails({...details, work_hr_est: e.target.value.replace(/\D/, '')});
    console.log("Details: " + details);
  }

  // TODO: Display days_since_creation
  // TODO: Delete button
  return (
    <form onSubmit={handleSubmit}>
      <label>
        Task:
        <input type="text" value={details.description}
          onChange={handleTaskChange} />
      </label>
      <label>
        Priority:
        <select value={details.priority} onChange={handlePriorityChange}>
          <option value="1">1</option>
          <option value="2">2</option>
          <option value="3">3</option>
          <option value="4">4</option>
          <option value="5">5</option>
        </select>
      </label>
      <label>
        Details:
        <input type="text" value={details.detail} onChange={handleDetailChange} />
      </label>
      <label>
        Days since creation: {details.created_at}
      </label>
      <label>
        Work hr est:
        <input type="text" value={details.work_hr_est} onChange={handleHourChange} />
      </label>
      <input type="submit" value="Update" />
    </form>
  );
}

export default TaskDetail;
