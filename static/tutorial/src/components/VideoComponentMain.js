import React, { Component, useState } from "react";
import VideoPlayer from './videoplayer';
import Tabs from './Tabs';
import Tab from './Tabs';
import axios from 'axios';
import moment from 'moment-timezone';

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

var r ;
class Main extends React.Component {
  constructor(props){
    super(props);
    this.state={
      isOpen: false,
      resource: null
    }
  
  }

  componentDidMount(){
    if (this.props.current_foss && this.props.tutorial && this.props.current_language) {
    axios.get("https://spoken-tutorial.org/api/st_video_resource/"+window.location.search)
          .then(res => {
            this.setState({
              resource: res.data
            });
          })
        }
  }
  
  

  render(){

   const mainStatus = this.state.isOpen ? "isopen" : "";
   const videoJsOptions = {
    autoplay: true,
    muted: true,
    controls: true,
    sources: [{
      src: this.props.tutorial.sources[0],
      type: 'video/ogg'
    }],
    tracks: [{
      src: this.state.resource ? this.state.resource.srt_file:"",
      label: this.props.current_language,
      kind: "captions"
    }]
  }

    return(
    <div className={this.props.mainStatus} id="main" >
        <div className="columns topBanner blueBg">
        <div className="column is-one-third toggleWrapper">
          <button onClick={this.props.handleClick} className="playlistToggle">
          <i class="fas fa-list"></i>  <span>Tutorial List</span>
        </button>
          
        </div>
        <div className="column">
          <button className="videoTitle blueBg">
          <span className="is-size-6 mb-2">{this.props.tutorial.title}</span>
          <span className="tutorialProgress"><progress className="progress is-info mr-3" value={this.props.progressValue} max="100" ></progress></span>
        </button>
        </div>
        </div>
        
      <div className="main">
        <div>
          <VideoPlayer isOpen={mainStatus} current_foss={this.props.current_foss} current_language={this.props.current_language} tutorial_title={this.props.tutorial.title} time_completed={this.props.time_completed} is_authenticated ={this.props.is_authenticated} { ...videoJsOptions } />
          <div className="tabsWrapper">
        
       <Tabs>
         <Tab label="Course Details">
           <div>
             <p className="has-text-weight-bold is-size-5 highlight">Tutorial Details : </p>
             <p>{this.props.current_foss}  : {this.props.tutorial.title}</p>
             <p className="has-text-grey">Time : {this.props.tutorial.duration} </p>
             <hr/>
             <p className="has-text-weight-bold highlight">Description : </p>
             <p>{this.props.tutorial.description} </p>
             
           </div>
         </Tab>
         <Tab label="Resources">
         {this.state.resource ? <div>
             <p className="has-text-weight-bold is-size-5 mb-3 highlight">Tutorial Resources : </p>
            {this.state.resource.prerequisite ?<div class="tags has-addons res">
              <a href={this.state.resource.prerequisite} target="_blank">
              <i class="far fa-file-video mr-3 resIcon"></i> 
              <span>Watch Prerequisite Video</span></a>
            </div>:""}
            {this.state.resource.instruction_sheet ?
            <div class="tags has-addons res">
                <a href={this.state.resource.instruction_sheet} target="_blank">
                <i class="fas fa-file-download resIcon"></i>
                <span >Instruction Sheet</span>
                </a>
            </div>:""}
            {this.state.resource.installation_sheet ?
             <div class="tags has-addons res">
                <a href={this.state.resource.installation_sheet} target="_blank">
                <i class="fas fa-file-download resIcon"></i>
                <span >Installation Sheet</span>
                </a>
            </div>:""}
            {this.state.resource.code_file ?
             <div class="tags has-addons res">
                <a href={this.state.resource.code_file} target="_blank">
                <i class="fas fa-file-download resIcon"></i>
                <span >Code Files</span>
                </a>
            </div>:""}
            {this.state.resource.assignment ?
             <div class="tags has-addons res">
                <a href={this.state.resource.assignment} target="_blank">
                <i class="fas fa-file-download resIcon"></i>
                <span >Assignments</span>
                </a>
            </div>:""}
            {this.state.resource.timed_script ?
             <div class="tags has-addons res">
                <a href={this.state.resource.timed_script} target="_blank">
                <i class="fas fa-external-link-alt resIcon"></i>
                <span >Timed Script</span>
                </a>
            </div>:""}
            {this.state.resource.additional_resource ?
            <div class="tags has-addons res">
                <a href={this.state.resource.additional_resource} target="_blank">
                <i class="fas fa-file-download resIcon"></i>
                <span >Additional Resource Material</span>
                </a>
            </div> :""}
          </div>:"Loading Resources....."}
         </Tab>
         <Tab label="Forums">
         {this.state.resource ? this.state.resource.questions.map(item => (
         <article class="media">
              <div class="media-content forumQues">
                <div class="content">
                  <p className="forumInfo">
                  <i class="fas fa-link"></i>
                    <a target="_blank" className="forumTitle" href={"https://forums.spoken-tutorial.org/question/"+item.id}>{item.question}</a></p>
                    <p className="forumInfo"><i class="far fa-clock"></i><span>{item.minute_range}</span> : <span>{item.second_range}</span></p>
                  
                </div>
                <div className="columns">
                  <div className="column px-0">
                    <p class="forumInfo">
                  <i class="far fa-calendar-alt"></i><span>{moment(item.date).tz(moment.tz.guess()).format('MMMM Do YYYY, h:mm:ss a')}</span>
                  </p>
                  </div>
                  <div className="column px-0">
                <p class="forumInfo">
                  <i class="far fa-user"></i><span>{item.user}</span>
                  </p>
                  </div>
                </div>
                
            </div>
          </article>
         )): ""}
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