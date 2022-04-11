import React, { useState, useEffect } from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.js';
import Transfer from './pages/transfer';
import NavBar from './elements/navbar';
import getSessionCookie, {SessionContext} from './sessions/sessions';
 

function Home() {
  return (
    <body className='bg-dark h-100' style={{'minHeight': '100vh'}}>
      <NavBar page='home'></NavBar>
      <h1 className='mb-3 text-center text-light p-2'>Transfer your music from <div className='d-inline' style={{'color': 'green'}}>Spotify</div> to <div className='d-inline' style={{'color': 'red'}}>Youtube</div></h1>
      <div className='container'>
        <div className='row-eq-height row bg-light rounded'>
            <div className='col p-5'>
              <iframe src="https://open.spotify.com/embed/playlist/3iZwKo7GZfiJ1dzHqXt9gl" width="100%" height="315" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>
            </div>
            <div className='col-1 d-flex p-0 my-auto justify-content-center'><h1>To</h1></div>
            <div className='rounded p-5 col'>
              <iframe width="100%" height="315" src="https://www.youtube.com/embed/videoseries?list=PLmNwLlfxZxG3VA5Vi1U0phKRfnno0klVL" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
            </div>

        </div>
        <br/><br/><br/>
        <h2 className='text-center text-light'>3 easy steps</h2>
        <div className='text-center text-dark row-eq-height row bg-light rounded'>
          <div className='col p-2'>
            <h4>Sign up</h4><hr/>
            <p>Sign in with your Spotify account & Youtube account you want the playlists to be transfered on</p>
          </div>
          <div className='col p-2'>
            <h4>Choose your playlist</h4><hr/>
            <p>Navigate between your playlists and choose the one you want on youtube!</p>
          </div>
          <div className='col p-2'>
            <h4>Click and listen</h4><hr/>
            <p>Click "transfer this" and soon you'll be able to listen to it!</p>
          </div>
        </div>
      </div>
      <br></br>
    </body>
  )
}

const RouteList = () => {
  const [session, setSession] = useState(getSessionCookie());
  useEffect(
    () => {
      setSession(getSessionCookie());
    },
    []
  );
  return (
    <SessionContext.Provider value={session}>
      <BrowserRouter>
        <Routes>
          <Route path="/">
            <Route index element={<Home />} />
            <Route path="/transfer" element={<Transfer />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </SessionContext.Provider>
  );
}


const App = () => {
  return (<><RouteList/></>)
}
export default App;

