import React, { Component }  from 'react';
import Header from './Components/Header';
import Navbar from './Components/Nav-bar';
import Filters from './Components/Filters';
import './App.css';

class App extends Component {  
  
  

render() {
  
      return (  
    
        <div>
          <Header  />
          <Navbar  />        
          <Filters />
        </div>        
  
  );
  
  }
}


export default App;
