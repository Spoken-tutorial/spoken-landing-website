import React, { Component } from "react";
import VideoDetail from './video-detail';
import Playlist from './playlist';

class Watch extends Component {

    constructor(props){
    super(props);
    
  }
    render(){
        return (
            <div>
                <div className="columns">
                    <div className="column is-12">
                        <div className="">
                        <VideoDetail tutorials={this.props.tutorials} current_foss={this.props.current_foss} current_language={this.props.current_language} tutorial= {this.props.tutorial} video_status={this.props.video_status} saveComplete={this.props.saveComplete} time_completed={this.props.time_completed} progressValue={this.props.progressValue}/>
                        </div>
                    <br/>
                    </div>
                </div>
                </div>
            );
        
        }
    }

export default Watch;