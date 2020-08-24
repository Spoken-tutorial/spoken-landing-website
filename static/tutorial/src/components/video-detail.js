import React, { Component } from "react";
import VideoPlayer from './videoplayer';
import axios from 'axios';

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

class VideoDetail extends Component {
  render(){
    const videoJsOptions = {
      autoplay: true,
      muted: true,
      controls: true,
      sources: [{
        src: this.props.tutorial.sources[0],
        type: 'video/ogg'
      }]
    }
      return (
      <div>
          <div className="box">
              <VideoPlayer current_foss={this.props.current_foss} current_language={this.props.current_language} tutorial_title={this.props.tutorial.title} time_completed={this.props.time_completed} { ...videoJsOptions } />
          </div>
        <div className="box video-meta">
        <div className="video-title">{this.props.tutorial.title}</div>
                  <br/>
                  <article className="media">
                    <div className="media-left">
                      <figure className="image is-64x64">
                            <img src="http://placehold.it/128x128" alt="Image" />
                      </figure>
                    </div>

                    <div className="media-content">
                      <div className="content">
                        <div className="columns">
                          <div className="column is-6">
                            <p>
                              <br/>
                              <a href="#" class="button is-danger">{this.props.tutorial.studio}</a>
                            </p>
                          </div>
                          <div className="column is-6">
                            <nav className="nav">
                              <div className="container">
                                <div className="nav-right">
                                  <a className="nav-item is-tab is-active">
                                    <span className="title is-4">{this.props.tutorial.duration}</span>
                                  </a>
                                </div>
                              </div>
                            </nav>
                          </div>

                        </div>
                        <nav className="level">
                          <p className="level-item has-text-left">
                            {this.props.video_status ?
                                <button class="button is-success" onClick={this.props.saveComplete}>
                                            <span class="icon is-small">
                                              <i class="fas fa-check"></i>
                                            </span>
                                            <span>Completed</span>
                                </button> : 
                                <button class="button is-success" onClick={this.props.saveComplete}>Mark Complete</button>
                                }
                          </p>
                        </nav>
                      </div>
                    </div>
                  </article>
        </div>
        <div className="box video-description">
            <p><strong>{this.props.tutorial.production}</strong></p>
            <p>{this.props.tutorial.description}</p>
            <hr/>
            <p className="has-text-centered has-text-muted video-description-more">Show More</p>
        </div>
        </div>
);
}
}

export default VideoDetail;