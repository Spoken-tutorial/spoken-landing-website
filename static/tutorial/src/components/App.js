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
      total_duration:0,
      is_authenticated:false
    };
    
  }
  
  componentDidMount() {
    fetch(`${process.env.SERVER_API_URL}`+"spoken/api/tutorial-search/"+window.location.search)
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
            total_duration:result['total_duration'],
            isLoaded: true,
            is_authenticated: result['is_authenticated'] ? result['is_authenticated'] : false
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
  getProgress(completed,total_duration){
    if (total_duration) {
      return completed/total_duration *100;
    }else{
      return 0;
    }
}

  
  
  render(){

    const divStyle = {
      color: 'green',
      backgroundImage: 'green',
      align: 'right'
    };

    const { error, isLoaded, foss_lang_list, current_foss, current_language, search_foss, search_language, languages, tutorials , tutorial, video_status, time_completed,total_duration, is_authenticated} = this.state;
    if (error) {
      return <div>Error: {error.message}</div>;
    } else if (!isLoaded) {
      return <div class="pageloader is-active"><span class="title"><strong><h1>Loading.... Spoken Tutorials</h1></strong></span></div>;
    } else {
      return (
    <div>
    
    <div>

    
      <div className=" video-description py-2 darkBg">

    <div className="container">
        <div className="column">
    <form method='get' action="/spoken/tutorial-search/"> 
      <div className="columns">
      <div className="column is-2 logoST">
      <img src="/static/spoken/images/logo.png" /> 
      <p><span className="mr-1 title1">Spoken</span> <span className="title2">Tutorial</span></p>
      </div>
          <div className="column is-9 is-centered">
          <div className="columns">
          <div  className="column is-5">
          <div class="field">
          <div class="control">
          <div className="select is-info is-fullwidth">
            <select name="search_foss" onChange={this.handleFoss.bind(this)} value={search_foss} className="selectStyle">
            {foss_lang_list.map(item => (
              <option value={item.foss}>{item.foss}</option>
              ))}
            </select>
          </div>
          </div>
          </div>
          </div>

          <div  className="column is-5">
          <div class="field">
          <div class="control">
          <div className="select is-info is-fullwidth" >
          <select name="search_language" onChange={this.handleChange.bind(this)} value={search_language} className="selectStyle">
          {languages.map(item => (
              <option value={item}>{item}</option>
              ))}
          </select>
        </div>
        </div>
        </div>
        </div>
        <div  className="column is-2">
        <div class="field">
          <div class="control">
            <button type="submit" class="button submitStyle">Search</button>
          </div>
        </div>
        </div>
        </div>
        </div>
        
      </div>

    </form>
    </div>
    </div>
    
    </div>
   
    
    
    
    {tutorial ? <Watch current_foss={current_foss} current_language={current_language} tutorial={tutorial} tutorials={tutorials} video_status={video_status} saveComplete={this.saveComplete} time_completed={time_completed} 
    progressValue={this.getProgress(time_completed,total_duration)} is_authenticated={is_authenticated}/> : 
    <div className="container mt-4 "><div className="columns tutorialListWrapper">
        <div className="column is-8">
            {            
            tutorials.map(item => (
            <>
            <div className="media media-border px-3">
                <div className="media-left is-hidden-mobile">
                  <div className="image is-110x110">
                    <img src={item.card[0]} alt="Image" />
                  </div>
                </div>
                <div className="media-content">
                  <div className="content">
                  <p><strong><a className="tutorialName" href={`${process.env.SERVER_API_URL}`+"spoken/tutorial-search/?search_foss="+current_foss+"&search_language="+current_language+"&search_tutorial="+item.title}>{item.title}</a></strong>
                    &nbsp;<span>
                    {item.status ? <i style={divStyle} class="fas fa-check"></i> : 
                    ( item.time_completed == 0) ? <i class="far fa-play-circle"></i> :
                    <i style={divStyle} class="far fa-play-circle"></i> }</span>
                    </p>
                    <p className="tutorialDesc">{item.description}</p>
                  </div>
                  <div className="columns floatBottom">
                    <div className="column is-one-quarter text-muted info progressWrap"><span>
                    {item.status ? 'Completed' : 
                    ( item.time_completed == 0) ? <span>Total time - {item.duration}</span> :
                    <progress className="progress is-info " value={this.getProgress(item.time_completed,item.total_duration)} max={100} style={{width: "150px",height:"5px"}}>
                    item.time_completed</progress> }</span></div>
                    <div className="column text-muted">
                    {(item.views == 0) ? '' : <span className="info">views - {item.views}</span>}
                    </div>
                  </div>
                </div>
              </div>
            </>
))}
      </div>
      <div className="column is-4 ">
      <div className="courseDetails px-4 py-4 box">
        <p className="has-text-weight-bold">Course Details</p>
        <p>Course : {current_foss}</p>
        <p>Language : {current_language}</p>
        <hr/>
        <p className="has-text-weight-bold">Course Progress : </p>
        <progress className="progress is-info " value={this.getTutorialProgress()} max={100} style={{width: "150px",height:"5px"}}>
                    {this.getTutorialProgress()} Complete</progress>{parseInt(this.getTutorialProgress())}% Complete
      </div>
      </div>
    </div>
  </div>}



    </div>
    </div>
  );
}
}
}

export default App;
