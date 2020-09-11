import React, {useState, useRef} from "react";
import './Accordion.css';
import PropTypes from 'prop-types';

function Accordion(props){

  const [setActive, setActiveState] = useState("");
  const [setHeight, setHeightState] = useState("0px");

  const content = useRef(null);

  function toggleAccordion(){
    setActiveState(setActive=="" ? "active" : "");
    setHeightState(setActive === "active" ? "0px" : `${content.current.scrollHeight}px`);
  }

  return (
    <div className="accordion_section">
      <button className={`accordion px-3 py-3 ${setActive}`} onClick={toggleAccordion}>
        <p className="accordion_title">{props.title} <span className="chevron"><i class="fas fa-chevron-down"></i></span></p>
      </button>
      <div ref={content} style={{maxHeight: `${setHeight}`}} className="accordion_content px-3 ">
      <div className="my-4">
      <a href={props.videoLink}><i class="far fa-play-circle"></i></a><div className="accordion_text py-3 ml-3" dangerouslySetInnerHTML={{ __html: props.content}}>
      </div>
        

        </div>
      </div>


    </div>

    )

}

export default Accordion