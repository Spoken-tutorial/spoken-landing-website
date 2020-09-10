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
    const courseProgress = {
      color: "white",
      backgroundColor: "DodgerBlue",
      width: "150px",
      height: "5px",
      fontFamily: "Arial"
    }
   const mainStatus = this.state.isOpen ? "isopen" : "";
   const videoJsOptions = {
    autoplay: true,
    muted: true,
    controls: true,
    sources: [{
      src: this.props.tutorial.sources[0],
      type: 'video/ogg'
    }]
  }
    return(
    <div className={mainStatus} id="main" >
        <div className="columns topBanner blueBg">
        <div className="column is-one-third toggleWrapper">
          <button onClick={this.handleClick} className="playlistToggle">
          <i class="fas fa-list"></i>  <span>Tutorial List</span>
        </button>
          
        </div>
        <div className="column">
          <button className="videoTitle blueBg">
          <span className="is-size-6 mb-2">{this.props.tutorial.title}</span>
          <span className="tutorialProgress"><progress className="progress is-info mr-3" value="20" max="100" ></progress>20%</span>
        </button>
        </div>
        </div>
        
      <div className="main">
        <div>
          <VideoPlayer isOpen={mainStatus} current_foss={this.props.current_foss} current_language={this.props.current_language} tutorial_title={this.props.tutorial.title} time_completed={this.props.time_completed} { ...videoJsOptions } />
          <div className="tabsWrapper">
        
       <Tabs>
         <Tab label="Details">
           <div>
             <p className="has-text-weight-bold is-size-5">Tutorial Details : </p>
             <p>{this.props.current_foss}  : {this.props.tutorial.title}</p>
             <p className="has-text-grey">Time : {this.props.tutorial.duration} </p>
             <hr/>
             <p className="has-text-weight-bold">Description : </p>
             <p>{this.props.tutorial.description} </p>
             
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