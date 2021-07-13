import React from 'react';
import {Link} from 'react-router-dom';

function Nav() {
  return (
    <nav>
      <Link className="App-link" to="/">Home</Link>
      &nbsp;|&nbsp;
      <Link className="App-link" to="/tasks">Tasks</Link>
      &nbsp;|&nbsp;
      <Link className="App-link" to="/create">Create Task</Link>
    </nav>
  );
}

export default Nav;
