import React, { Component, useState } from "react";
import VideoPlayer from './videoplayer';
import axios from 'axios';
import Accordion from './Accordion';
import Main from './VideoComponentMain';
import Sidebar from './Sidebar';



axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

class VideoDetail extends Component {

  constructor(props){
    super(props);
    this.state={
      isOpen: false
    }
  this.handleClick = this.handleClick.bind(this)
  }
  
  handleClick(){
    this.setState({ isOpen : !this.state.isOpen})
  }

  render(){
    const mainStatus = this.state.isOpen ? "isopen" : "";
    const hideSidebar = this.state.isOpen ? "hideSidebar" : "";

      return (
      <div>
      <div className="wrapper">
        <Sidebar id="sidebar" className={hideSidebar} tutorials={this.props.tutorials} current_foss={this.props.current_foss} current_language={this.props.current_language}/>
        <Main className={mainStatus} current_foss={this.props.current_foss} current_language={this.props.current_language} tutorial= {this.props.tutorial} video_status={this.props.video_status} saveComplete={this.props.saveComplete} time_completed={this.props.time_completed} progressValue={this.props.progressValue}/>       
    </div>
    </div>
 

        
);
}
}

export default VideoDetail;

