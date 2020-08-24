import React, { Component } from "react";


class Playlist extends Component {
    render(){
        const divStyle = {
            color: 'green',
            backgroundImage: 'green',
          };
        return (
        <div className="box related-list">
            {this.props.tutorials.map(item => (
                <a href= {`${process.env.SERVER_API_URL}`+"spoken/tutorial-search/?search_foss="+this.props.current_foss+"&search_language="+this.props.current_language+"&search_tutorial="+item.title}>
                <article className="media related-card" >
                    <div className="media-left">
                    <figure className="image">
                        <img src={item.card[0]} alt="Image"/>
                    </figure>
                    </div>
                    <div className="media-content">
                    <div className="content">
                        <p>
                        <span className="video-title" >{item.title}</span>
                        <span className="video-account">{item.studio} | {this.props.current_language}</span>
                        <span className="video-views">{item.duration}</span>
                        <span>{item.status? <i style={divStyle} class="fas fa-check"></i>: <i style={divStyle} class="fas fa-play"></i> }</span>
                        </p>
                    </div>
                    </div>
                </article>
                <br/>
                </a>
            ))}
        </div>
    );
        
    }
}
    
export default Playlist;