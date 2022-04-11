import React, {useContext} from "react"
import { SessionContext } from '../sessions/sessions';


var settings = require('../settings.json');

class SpotifyLogin extends React.Component {
    render() {
      return (
        <li className="nav-item mx-xl-1">
          <a className='' href={`https://accounts.spotify.com/authorize?response_type=code&client_id=a3b15a18c0a445d7b0a8454bea35e47e&scope=user-read-playback-state+user-read-email+playlist-modify-private+playlist-read-private+playlist-read-collaborative+playlist-modify-public+user-library-modify+user-library-read&redirect_uri=${settings.host.hostname}/api/login/spotify`}>
            <button className="btn btn-primary">Sign in with Spotify</button>
          </a>
        </li>
      )
    }
  }

class GoogleLogin extends React.Component {
  render () {
    return (
      <li className="nav-item mx-xl-1">
        <a className='' href='/api/login/google'>
        <button className="btn btn-primary">Sign in with Google</button>
        </a>
      </li>
    )
  }
}

const NavBar = (props) => {
    const session = useContext(SessionContext);
      return (
        <>
          <nav className="fixed-top navbar navbar-expand-lg navbar-light bg-light">
            <div className="container-fluid justify">
              <a className="navbar-brand" href="../">Music</a>
              <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span className="navbar-toggler-icon"></span>
              </button>
              <div className="collapse navbar-collapse" id="navbarSupportedContent">
                <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                  <li className="nav-item">
                    <a className={props.page == 'home' ? 'nav-link active' : 'nav-link'} aria-current="page" href="../">Home</a>
                  </li>
                  <li className="nav-item">
                    <a className={props.page == 'transfer' ? 'nav-link active' : 'nav-link'} href="transfer">Transfer</a>
                  </li>
                </ul>
                <ul className='navbar-nav'>
                  {session.spotify_access_token ? <></> : <SpotifyLogin />}
                  {session.google_access_token ? <></> : <GoogleLogin />}
                  {(props.page == 'home') ? (!session.spotify_access_token && !session.google_access_token ? <></> :<><a href="/transfer"><button className='btn btn-primary'>Transfer your Music</button></a></>) : <></>}
                </ul>
              </div>
            </div>
          </nav>
        </>
      )
  }

export default NavBar
