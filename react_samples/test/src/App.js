import React, { Component } from 'react';
import Population from './population';
import './App.css';

class App extends Component {
  constructor() {
      super();
      this.state = {
          isLoading: false,
          hasError: false,
          data: []
      }
  }

  componentDidMount() {
    // this.fecthData('https://vw9d3y3k55.execute-api.ap-northeast-1.amazonaws.com/test2');
    this.fecthData('https://d3anifybrnto0.cloudfront.net/test2/');
  }

  fecthData(url) {
    this.setState({ isLoading: true});
    fetch(url, {
      // mode: 'no-cors',
      headers: {
       'Access-Control-Allow-Origin': '*'
      }
    })
    .then((response) => {
        this.setState({ isLoading: false });
        console.log(response);
        if (!response.ok) {
          throw Error(response.statusText);
        }
        return response
    })
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
        this.setState({ data: data });
    })
    .catch(() => this.setState({ hasError: true }));
  }

  render() {
    return (
      <div className="App">
        <h1>愛知県の人口</h1>
        <Population
          isLoading={this.state.isLoading}        
          hasError={this.state.hasError}
          data={this.state.data}
          />
      </div>
    );
  }
}

export default App;
