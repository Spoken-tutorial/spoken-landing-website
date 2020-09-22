import React, { Component, useState } from "react";
import VideoPlayer from './videoplayer';
import Tabs from './Tabs';
import Tab from './Tabs';
import axios from 'axios';
import moment from 'moment-timezone';

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

class Main extends React.Component {
  constructor(props){
    super(props);
    this.state={
      isOpen: false,
      resource: null
    }
  this.handleClick = this.handleClick.bind(this)
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
  
  handleClick(){
    this.setState({ isOpen : !this.state.isOpen})
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
             <p className="has-text-weight-bold is-size-5">Tutorial Details : </p>
             <p>{this.props.current_foss}  : {this.props.tutorial.title}</p>
             <p className="has-text-grey">Time : {this.props.tutorial.duration} </p>
             <hr/>
             <p className="has-text-weight-bold">Description : </p>
             <p>{this.props.tutorial.description} </p>
             
           </div>
         </Tab>
         <Tab label="Resources">
         <div>
             <p className="has-text-weight-bold is-size-5">Tutorial Resources : </p>
             <div class="tags has-addons">
                <span class="tag">Prerequisite</span>
                <a href={this.state.resource ? this.state.resource.prerequisite : "#"} target="_blank"><span class="tag is-primary">Watch</span></a>
            </div>
             <div class="tags has-addons">
                <span class="tag">Instruction Sheet</span>
                <a href={ this.state.resource ? this.state.resource.instruction_sheet : "#"} target="_blank"><span class="tag is-success">Download</span></a>
            </div>
             <div class="tags has-addons">
                <span class="tag">Installation Sheet</span>
                <a href={this.state.resource ? this.state.resource.installation_sheet : "#"} target="_blank"><span class="tag is-success">Download</span></a>
            </div>
             <div class="tags has-addons">
                <span class="tag">Code Files</span>
                <a href={this.state.resource ? this.state.resource.code_file : "#"} target="_blank"><span class="tag is-success">Download</span></a>
            </div>
             <div class="tags has-addons">
                <span class="tag">Assignments</span>
                <a href={this.state.resource ? this.state.resource.assignment : "#"} target="_blank"><span class="tag is-success">Download</span></a>
            </div>
             <div class="tags has-addons">
                <span class="tag">Slides</span>
                <a href={this.state.resource ? this.state.resource.slide : "#"} target="_blank"><span class="tag is-success">Download</span></a>
            </div>
             <div class="tags has-addons">
                <span class="tag">Script</span>
                <a href={this.state.resource ? this.state.resource.script : "#"} target="_blank"><span class="tag is-warning">View</span></a>
            </div>
             <div class="tags has-addons">
                <span class="tag">Timed Script</span>
                <a href={this.state.resource ? this.state.resource.timed_script : ""} target="_blank"><span class="tag is-warning">View</span></a>
            </div>
          </div>
         </Tab>
         <Tab label="Forums">
         {this.state.resource ? this.state.resource.questions.map(item => (
         <article class="media">
              <figure class="media-left">
                <p class="image is-64x64">
                  
                </p>
              </figure>
              <div class="media-content">
                <div class="content">
                  <p>
                    <a href={"https://forums.spoken-tutorial.org/question/"+item.id}>{item.question}</a>
                  </p>
                </div>
                <nav class="level is-mobile">
                <div class="level-left">
                  <a class="level-item">
                  <span class="tag is-primary">{item.minute_range}</span>
                  </a>
                  <a class="level-item">
                  <span class="tag is-link">{item.second_range}</span>
                  </a>
                  <a class="level-item">
                  <span class="tag is-warning">{moment(item.date).tz(moment.tz.guess()).format('MMMM Do YYYY, h:mm:ss a')}</span>
                  </a>
                  <a class="level-item">
                  <span class="tag is-danger">{item.user}</span>
                  </a>
                </div>
              </nav>
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