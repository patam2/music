import {useState, useEffect, useContext} from 'react';
import React from 'react';
import Accordion from 'react-bootstrap/Accordion'
import NavBar from '../elements/navbar';
import { SessionContext } from '../sessions/sessions';
import SpotifySonglist, {ClickButton} from '../elements/spotifySongList';
import ShowModal from '../elements/playlistCreationModal';

const Transfer = () => {
    const [playlists, setPlaylists] = useState([]);
    const [liked_tracks, setLikedTracks] = useState({"tracks": [], "total": 0});
    const [url, setUrl] = useState('')
    const session = useContext(SessionContext);
    const [active, SetActive] = useState(false)

    useEffect(() => {
        fetch('/api/spotify/get_playlists').then(res => res.json()).then(data => {
            setPlaylists(data.playlists);
        });
        fetch('api/spotify/get_liked_songs').then(res => res.json()).then(data => {
            setLikedTracks(data)
        });
    }, []);

    useEffect(() => {
        console.log(url)
        if (url) {            
            SetActive(true);
        }
    }, [url]);

    if (session.email === undefined) {
        return (
            'L + log in + ratio'
        )
    } 

    return (
        <div className='bg-dark'>
            {active ? <ShowModal url={url} closeFunc = {SetActive}/>: <></>}
            <NavBar page='transfer'></NavBar>
            <h1 className="text-center text-white">Transfer page</h1>
            <h3 className="text-center text-white">Liked songs</h3>
            <div className="container">
                <Accordion>
                    <Accordion.Item>
                        <Accordion.Header eventKey="likedTracksKey">{liked_tracks.total} Tracks</Accordion.Header>
                        <Accordion.Body className='bg-dark text-white'>
                            <h3>First 10 tracks:</h3>
                            <ul>
                                {liked_tracks.tracks.map(song => {
                                    return <li>{song.track.artists.map(artist => {return artist.name}).join(', ')} - {song.track.name}</li>
                                })}
                            </ul>
                            <ClickButton urlSetterFunction={setUrl} name='Liked tracks' rkey='LIKED'></ClickButton>
                        </Accordion.Body>
                    </Accordion.Item>
                </Accordion>

                <h3 className="text-center text-white m-2">Playlists:</h3>
                
                <Accordion> 
                    {playlists.map((playlist, index) => {
                        return <SpotifySonglist 
                            rkey={playlist.id} 
                            name={playlist.name} 
                            trackcount={playlist.tracks.total} 
                            key={playlist.id} 
                            link={playlist.external_urls.spotify}
                            urlSetterFunction={setUrl}
                        />
                    })}
                </Accordion>
            </div>
        </div>
    )
}

export default Transfer