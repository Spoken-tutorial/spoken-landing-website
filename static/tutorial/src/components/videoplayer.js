import React from 'react';
import videojs from 'video.js'
import 'video.js/dist/video-js.css';
import '@videojs/themes/dist/fantasy/index.css';
import axios from 'axios';

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

export default class VideoPlayer extends React.Component {
  constructor(props) {
    super(props);
    this.saveTutorialCompletion = this.saveTutorialCompletion.bind(this);
    this.formatTime = this.formatTime.bind(this);

  }
  componentDidMount() {
    // instantiate Video.js
    this.player = videojs(this.videoNode, this.props, function onPlayerReady() {
      console.log('onPlayerReady', this)
      
    });
    this.player.currentTime(this.props.time_completed*60)
    var intervalId = setInterval(this.saveTutorialCompletion, 1000);
    this.setState({
      intervalId: intervalId,
      logTime: Math.abs(parseInt(this.player.currentTime() / 60)),
      currentTime: Math.abs(parseInt(this.player.currentTime()))
    });
  }

  saveTutorialCompletion(){
    //log time
    var currentLogTime = Math.abs(parseInt(this.player.currentTime() / 60))
    if (this.state.logTime < currentLogTime){
      this.setState({
        logTime: currentLogTime
      });

      console.log('Log Time', this.state.logTime)
      axios.post(`${process.env.SERVER_API_URL}`+"logs/save_tutorial_progress/", 
          {
            tutorial: this.props.tutorial_title,
            foss: this.props.current_foss,
            language: this.props.current_language,
            time_completed: this.state.logTime,
            total_duration: Math.abs(parseInt(this.player.duration() / 60))
          }
          )
          .then(res => {
            console.log(res)
          })
    }

    //current time
    this.setState({
      currentTime: Math.abs(parseInt(this.player.currentTime()))
    });
  }

  formatTime(time){
    time = Math.round(time);
    var minutes = Math.floor(time / 60),
    seconds = time - minutes * 60;
    seconds = seconds < 10 ? '0' + seconds : seconds;
    return minutes + "." + seconds;
    }

  // destroy player on unmount
  componentWillUnmount() {
    if (this.player) {
      this.player.dispose()
    }
  }

  // wrap the player in a div with a `data-vjs-player` attribute
  // so videojs won't create additional wrapper in the DOM
  // see https://github.com/videojs/video.js/pull/3856
  render() {
    return (
      <div>	
        <div data-vjs-player>
          <video ref={ node => this.videoNode = node } className="video-js vjs-theme-fantasy video-js-responsive-container vjs-hd" width="100%" height="auto"></video>
        </div>
      </div>
    )
  }
}
