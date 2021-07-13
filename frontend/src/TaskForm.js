import React from 'react';

class TaskForm extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      description: '',
      priority: '1'
    };
  }

  handleTaskChange = (e) => {
    this.setState({description: e.target.value});
    console.log("State: " + this.state);
  }

  handlePriorityChange = (e) => {
    this.setState({priority: e.target.value});
    console.log("State: " + this.state);
  }

  // TODO: Check if I can use this for both:
  // handleChange = (event) => {
  //   this.setState({[event.target.name]: event.target.value});
  // }

  handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Data to send: " + JSON.stringify(this.state))
    const resp = await fetch('/tasks', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(this.state)
    });
    console.log(resp);
    const data = await resp.json();
    console.log(data);
    this.props.history.push('/tasks');
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <label>
          Task:
          <input type="text" value={this.state.taskValue} onChange={this.handleTaskChange} />
        </label>
        <label>
          Priority:
          <select value={this.state.priorityValue} onChange={this.handlePriorityChange}>
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
            <option value="4">4</option>
            <option value="5">5</option>
          </select>
        </label>
        <input type="submit" value="Submit" />
      </form>
    );
  }
}

export default TaskForm;
