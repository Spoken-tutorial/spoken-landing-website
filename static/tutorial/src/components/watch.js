import React, { Component } from "react";
import VideoDetail from './video-detail';
import Playlist from './playlist';

class Watch extends Component {
    render(){
        return (
            <div>
                <div className="columns">
                    <div className="column is-12">
                        <div className="">
                        <VideoDetail current_foss={this.props.current_foss} current_language={this.props.current_language} tutorial= {this.props.tutorial} video_status={this.props.video_status} saveComplete={this.props.saveComplete} time_completed={this.props.time_completed}/>
                        </div>
                    <br/>
                    </div>
                </div>
                </div>
            );
        
        }
    }

export default Watch;