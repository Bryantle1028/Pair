import React, { Component } from 'react';
import logo from './logo.png';
import './login.css';

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1>
            It's sick as fuck
          </h1>
          <form>
            <label>
              Username:
              <input type="text" user="username" />
            </label>
            <br />
            <label>
              Password:
              <input type="text" pass="password" />
            </label>
            <br />
            <input type="submit" value="Login" />
          </form>
        </header>
      </div>
    );
  }
}

export default App;
