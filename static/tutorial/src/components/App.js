import React, { Component } from "react";
import './App.css';
import Watch from './watch';
import axios from 'axios';

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

class App extends Component {
  constructor(props) {
    super(props);
    this.handleFoss = this.handleFoss.bind(this);
    this.handleSubmit = this.handleChange.bind(this);
    this.saveComplete = this.saveComplete.bind(this);
    this.getTutorialProgress = this.getTutorialProgress.bind(this);
    this.state = {
      error: null,
      isLoaded: false,
      foss_lang_list: null,
      search_foss: '',
      search_language: '',
      search_tutorial: '',
      languages:null,
      tutorials: null,
      tutorial: null,
      current_foss: '',
      current_language: '',
      video_status:false,
      time_completed:0,
    };
  }
  
  componentDidMount() {
    fetch(`${process.env.SERVER_API_URL}`+"spoken/api/tutorial-search/"+location.search)
      .then(res =>{
        return res.json()
      })
      .then(
        (result) => {
          this.setState({
            foss_lang_list: result['foss_lang_list'],
            search_foss: result['foss'] ? result['foss']: result['foss_lang_list'][0].foss,
            search_language: result['language'],
            languages: result['foss'] ? result['foss_languages'] : result['foss_lang_list'][0].languages,
            tutorials: result['tutorials'],
            tutorial: result['tutorial'],
            current_foss: result['foss'],
            current_language: result['language'],
            video_status:result['video_status'],
            time_completed:result['time_completed'],
            isLoaded: true
          });
        },
        // Note: it's important to handle errors here
        // instead of a catch() block so that we don't swallow
        // exceptions from actual bugs in components.
        (error) => {
          this.setState({
            isLoaded: true,
            error
          });
        }
      )

  
  }

  handleFoss(event) {
    let {name: fieldName, value} = event.target;
    this.setState({
      [fieldName]: value,
      languages: this.getLanguages(value)
    });
  };

  getLanguages(foss){
    for (var key in this.state.foss_lang_list) {
      if (this.state.foss_lang_list[key].foss == foss){
        return this.state.foss_lang_list[key].languages
      }
    }
  }

  handleChange(event){
    let {name: fieldName, value} = event.target;
    this.setState({
      [fieldName]: value,
    });
  }

  saveComplete(event){
    axios.post(`${process.env.SERVER_API_URL}`+"logs/get_set_progress/", 
    {
      tutorial: this.state.tutorial.title,
      foss: this.state.current_foss,
      language: this.state.current_language,
    })
    .then(res => {
      this.setState({
        video_status: res.data.status
      })
    })
  }
  getTutorialProgress(){
    var count=0
    var total=this.state.tutorials.length
    this.state.tutorials.map(item => (
      item.status? count++ : null
    ))
    return count/total *100
  }

  render(){
    const divStyle = {
      color: 'green',
      backgroundImage: 'green',
      align: 'right'
    };
    const { error, isLoaded, foss_lang_list, current_foss, current_language, search_foss, search_language, languages, tutorials , tutorial, video_status, time_completed} = this.state;
    if (error) {
      return <div>Error: {error.message}</div>;
    } else if (!isLoaded) {
      return <div class="pageloader is-active"><span class="title"><strong><h1>Loading.... Spoken Tutorials</h1></strong></span></div>;
    } else {
      return (
    <div>
    <div className="spacer"></div>
    <div className="container">

    <div className="box video-description">
    <div className="columns">
        <div className="column is-8">
    <form method='get' action="/spoken/tutorial-search/"> 
      <div className="columns">
          <div className="column is-10">
          <div className="columns">

          <div  className="column is-4">
          <div class="field">
          <div class="control">
          <div className="select is-primary">
            <select name="search_foss" onChange={this.handleFoss.bind(this)} value={search_foss}>
            {foss_lang_list.map(item => (
              <option value={item.foss}>{item.foss}</option>
              ))}
            </select>
          </div>
          </div>
          </div>
          </div>

          <div  className="column is-3">
          <div class="field is-grouped">
          <div class="control">
          <div className="select is-primary" >
          <select name="search_language" onChange={this.handleChange.bind(this)} value={search_language}>
          {languages.map(item => (
              <option value={item}>{item}</option>
              ))}
          </select>
        </div>
        </div>
        </div>
        </div>

        <div  className="column is-3">
        <div class="field is-grouped">
          <div class="control">
            <button type="submit" class="button is-primary is-outlined">Search</button>
          </div>
        </div>
        </div>
        </div>
        </div>
      </div>
    </form>
    <div className="spacer"></div>
    </div>
    </div>
    </div>
    <progress class="progress is-success" value={this.getTutorialProgress()} max="100">{this.getTutorialProgress()}% Completed</progress>
    <div className="spacer"></div>
    {tutorial ? <Watch current_foss={current_foss} current_language={current_language} tutorial={tutorial} tutorials={tutorials} video_status={video_status} saveComplete={this.saveComplete} time_completed={time_completed}/> : 
    <div className="columns">
        <div className="column is-8">
            {            
            tutorials.map(item => (
            <div className="box video-description">
                    <p><strong><a href={`${process.env.SERVER_API_URL}`+"spoken/tutorial-search/?search_foss="+current_foss+"&search_language="+current_language+"&search_tutorial="+item.title}>{item.title}</a></strong>
                    &nbsp;<span>{item.status? <i style={divStyle} class="fas fa-check"></i>: <i style={divStyle} class="fas fa-play"></i> }</span>
                    </p>
                    <p>{item.description}</p>
                    <hr/>
                    <p className="has-text-centered has-text-muted video-description-more">Show More</p>
                </div>
              ))}
      </div>
    </div>}

    </div>
    </div>
  );
}
}
}

export default App;
