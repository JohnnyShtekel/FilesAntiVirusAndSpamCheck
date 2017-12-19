import React from 'react'
import Dropzone  from 'react-dropzone'


let style = {
  width: '100px',
  height: '100px'
};


export default class MainWindow extends React.Component {
    
  constructor() {
    super()
    this.state = {
      accepted: [],
      rejected: []
    }
  }

  render() {
    return (

        <div className="card">
              <div className="card-header">
                Featured
              </div>
              <div className="card-block">
                <section>
                        <div className="dropzone">
                          <Dropzone
                            accept="image/jpeg, image/png"
                            onDrop={(accepted, rejected) => { this.setState({ accepted, rejected }); }}
                          >
                            <p>Try dropping some files here, or click to select files to upload.</p>
                            <p>Only *.jpeg and *.png images will be accepted</p>
                          </Dropzone>
                        </div>
                        <aside>
                          <h2>Accepted files</h2>
                          <ul>
                            {
                              this.state.accepted.map(f => <li key={f.name}>{f.name} - {f.size} bytes</li>)
                            }
                          </ul>
                          <h2>Rejected files</h2>
                          <ul>
                            {
                              this.state.rejected.map(f => <li key={f.name}>{f.name} - {f.size} bytes</li>)
                            }
                          </ul>
                        </aside>
                      </section>
              </div>
</div>




    );
  }
}