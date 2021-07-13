import React from 'react';
import {BrowserRouter, Switch, Route} from 'react-router-dom';
import logo from './logo.svg';
import './App.css';

import Nav from './Nav';
import Tasks from './Tasks';
import TaskForm from './TaskForm';
import TaskDetail from './TaskDetail';

function App() {
  // Have a Link to /tasks/id to view and edit a task.
  return (
    <div className="App">
      <header className="App-header">
        <BrowserRouter>
          <Nav />
          <Switch>
            <Route exact path="/">
              <img src={logo} className="App-logo" alt="logo" />
              <p>
                Edit <code>src/App.js</code> and save to reload.
              </p>
              <a
                className="App-link"
                href="https://reactjs.org"
                target="_blank"
                rel="noopener noreferrer"
              >
                Learn React
              </a>
            </Route>
            <Route exact path="/tasks" component={Tasks} />
            <Route path="/create" component={TaskForm} />
            <Route path="/tasks/:id" component={TaskDetail} />
          </Switch>
        </BrowserRouter>
      </header>
    </div>
  );
}

export default App;
