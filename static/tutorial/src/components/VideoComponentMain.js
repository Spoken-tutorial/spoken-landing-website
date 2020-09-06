import React, { Component, useState } from "react";
import VideoPlayer from './videoplayer';
import Tabs from './Tabs';
import Tab from './Tabs';

class Main extends React.Component {
  constructor(props){
    super(props);
    this.state={
      isOpen: false
    }
  this.handleClick = this.handleClick.bind(this)
  }
  
  handleClick(){
    this.setState({ isOpen : !this.state.isOpen})
    console.log(!this.state.isOpen)
  }
  render(){
   const mainStatus = this.state.isOpen ? "isopen" : "";
   const videoJsOptions = {
      autoplay: true,
      muted: true,
      controls: true,
      sources: [{
        src: "https://spoken-tutorial.org/media/videos/44/448/Classes-And-Objects-English.ogv",
        type: 'video/ogg'
      }]
    }
    return(
    <div className={mainStatus} id="main" >
        <div className="columns topBanner">
        <div className="column is-one-third toggleWrapper">
          <button onClick={this.handleClick} className="playlistToggle">
          <i class="fas fa-list"></i>  <span>Tutorial List</span>
        </button>
        </div>
        <div className="column">
          <button className="videoTitle">
          <span className="subtitle">Tutorial Name</span>
        </button>
        </div>
        </div>
        
      <div className="main">
        <div>
          <VideoPlayer isOpen={mainStatus} current_foss="Bash" current_language="English" tutorial_title="Introduction" time_completed="2" { ...videoJsOptions } />
          <div className="tabsWrapper">
        
       <Tabs>
         <Tab label="Tab 1">
           <div>
             <p className="has-text-weight-bold is-size-5">Course Details : </p>
             <p>Tutorial Name </p>
             <p className="has-text-grey">Time : 10 min 20 sec </p>
           </div>
         </Tab>
         <Tab label="Tab 2">
           <div>
             <p>
              Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
              sed do eiusmod tempor incididunt ut labore et dolore magna aliqua
              . Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris
               nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor
                in reprehenderit in voluptate velit esse cillum dolore 
             </p>
           </div>
         </Tab>
         <Tab label="Tab 3">
           <div>
            <p>
              Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
              sed do eiusmod tempor incididunt ut labore et dolore magna aliqua
              . Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris
               nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor
                in reprehenderit in voluptate velit esse cillum dolore 
             </p>
           </div>
         </Tab>
         <Tab label="Tab 4">
           <div>
             <p>Tab 4 content</p>
           </div>
         </Tab>
         <Tab label="Tab 5">
           <div>
             
             <p>Tab 5 content</p>
           </div>
         </Tab>
       </Tabs>
      </div>
        </div>
      </div>
    </div>
    )
  }
}

export default Main