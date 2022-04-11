import React from "react";

class Playlist extends React.Component {
    render() {
        return (
            <ul>
                {this.props.Playlists}
            </ul>
        )
    }
}

/* {this.props.Playlists.map(pl => {return <li>{pl.name}</li>})} */
export default Playlist