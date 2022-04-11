import React from 'react';
import Accordion from 'react-bootstrap/Accordion'

function getPlayListTracks(playlist_id) {
    var tracks = []
    return new Promise(function(resolve, reject){
        fetch(`/api/spotify/get_tracks_from_playlist?playlist_id=${playlist_id}`).then(res => res.json()).then(data => {
            data.tracks.forEach(elm => {tracks.push(elm.track)})
            resolve(tracks)
        })
    })
}


export const ClickButton = (props) => {
    function clicked(name, key) {
        fetch("/api/youtube/transfer", {
            'method': "POST",
            'headers': {'Content-Type': 'application/json'},
            'body': JSON.stringify({'playlist_name': name, 'playlist_id': key})
        }).then(resp => resp.json())
            .then(resp => props.urlSetterFunction(resp.url))
            //.then(resp => window.location = resp.url)
    }
    return (
        <button className='btn btn-primary' onClick={() => clicked(props.name, props.rkey)}>Transfer this!</button>
    )
}

class SpotifySonglist extends React.Component {
    constructor (props) {
        super(props)
        this.state = {
            tracks: [],
            isActive: false
        };
    }

    click(playlist_id) {
        if (!this.state.isActive) {
            getPlayListTracks(playlist_id).then(tracklist => this.setState({tracks: tracklist, isActive: !this.state.isActive}))
        }
    }

    render() {return (
        <Accordion.Item eventKey={this.props.rkey}>
            <Accordion.Header onClick={() => this.click(this.props.rkey)}>{this.props.name} | {this.props.trackcount} Tracks</Accordion.Header>
            <Accordion.Body className='bg-dark text-white' id={this.props.rkey}>
                <a className="link-light" href={this.props.link}>Link to playlist</a>
                <h3>First 10 playlist tracks:</h3>
                <ul>
                    {this.state.tracks.map(data => 
                        {return <li>{data.artists.map(artist => artist.name).join(', ')} - {data.name}</li>}
                    )}
                </ul>
                <ClickButton urlSetterFunction={this.props.urlSetterFunction} name={this.props.name} rkey={this.props.rkey}/>
            </Accordion.Body>
        </Accordion.Item>
    )
    }
}


export default SpotifySonglist;
