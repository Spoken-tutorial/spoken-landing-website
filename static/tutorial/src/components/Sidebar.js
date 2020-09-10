import React, { Component, useState } from "react";
import Accordion from './Accordion';

class Sidebar extends React.Component {


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
    const sidebarBtnStatus = this.state.isOpen ? "sidebarBtn" : "";
    console.log(this.props.tutorials);;
    return(
    <div id="sidebarWrapper">
    <div className="columns">
      <div className="column topBanner blueBg">
        <button className={`videoTitle ml-0 pl-0 blueBg ${sidebarBtnStatus}`}
         onClick={this.handleClick}>
          <span><i class="far fa-list-alt blueColor"></i> Contents</span>
        </button>
    </div>
    </div>
     <ul className="sidebarMenu" id="sidebar">

      {
        this.props.tutorials.map(tutorial =>
        <li>
       <Accordion title={tutorial.title} 
       content={`<a href="?search_foss=${this.props.current_foss}&search_language=${this.props.current_language}&search_tutorial=${tutorial.title}">${tutorial.description}</a> `}
        videoLink={`${process.env.SERVER_API_URL}?search_foss=${this.props.current_foss}&search_language=${this.props.current_language}&search_tutorial=${tutorial.title}`}/>
       </li>
       )
      }
      
        </ul>
      }
     </div>
    )
  }
}

export default Sidebar